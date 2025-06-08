import streamlit as st
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
import json
import hashlib
from datetime import datetime
import openai
from sqlalchemy import text

class VectorDatabase:
    """Vector database integration using pgvector for semantic search and analysis"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.openai_client = openai.OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
        self._ensure_vector_extension()
        self._create_vector_tables()
    
    def _ensure_vector_extension(self):
        """Ensure pgvector extension is available"""
        try:
            with self.db.engine.connect() as conn:
                # Check if pgvector extension exists
                result = conn.execute(text("SELECT 1 FROM pg_extension WHERE extname = 'vector';"))
                if not result.fetchone():
                    # Try to create extension (requires superuser privileges)
                    try:
                        conn.execute(text("CREATE EXTENSION vector;"))
                        conn.commit()
                    except Exception:
                        # If we can't create extension, use fallback similarity
                        st.warning("Vector extension not available. Using fallback similarity matching.")
                        self.vector_enabled = False
                        return
                
                self.vector_enabled = True
                
        except Exception as e:
            st.warning(f"Vector database setup issue: {e}. Using fallback similarity.")
            self.vector_enabled = False
    
    def _create_vector_tables(self):
        """Create vector storage tables"""
        if not self.vector_enabled:
            return
            
        try:
            with self.db.engine.connect() as conn:
                # Create embeddings table for AI initiatives
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS ai_initiative_embeddings (
                        id SERIAL PRIMARY KEY,
                        function_name VARCHAR(100),
                        initiative_id VARCHAR(100),
                        initiative_name VARCHAR(200),
                        content_text TEXT,
                        embedding vector(1536),
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(function_name, initiative_id)
                    );
                """))
                
                # Create embeddings table for industry patterns
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS industry_pattern_embeddings (
                        id SERIAL PRIMARY KEY,
                        industry VARCHAR(100),
                        pattern_type VARCHAR(100),
                        pattern_name VARCHAR(200),
                        content_text TEXT,
                        embedding vector(1536),
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """))
                
                # Create index for vector similarity search
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS ai_initiative_embedding_idx 
                    ON ai_initiative_embeddings USING ivfflat (embedding vector_cosine_ops);
                """))
                
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS industry_pattern_embedding_idx 
                    ON industry_pattern_embeddings USING ivfflat (embedding vector_cosine_ops);
                """))
                
                conn.commit()
                
        except Exception as e:
            st.warning(f"Could not create vector tables: {e}")
            self.vector_enabled = False
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text using OpenAI API"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            st.error(f"Error generating embedding: {e}")
            return None
    
    def store_initiative_embedding(self, function_name: str, initiative_id: str, 
                                 initiative_data: Dict[str, Any]) -> bool:
        """Store AI initiative embedding for semantic search"""
        if not self.vector_enabled:
            return False
        
        try:
            # Create content text for embedding
            content_parts = [
                f"Function: {function_name}",
                f"Name: {initiative_data.get('name', '')}",
                f"AI Type: {initiative_data.get('ai_type', '')}",
                f"Description: {initiative_data.get('description', '')}",
                f"Benefits: {', '.join(initiative_data.get('key_benefits', []))}"
            ]
            content_text = " | ".join(content_parts)
            
            # Generate embedding
            embedding = self.generate_embedding(content_text)
            if not embedding:
                return False
            
            # Store in database
            with self.db.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO ai_initiative_embeddings 
                    (function_name, initiative_id, initiative_name, content_text, embedding, metadata)
                    VALUES (:function_name, :initiative_id, :initiative_name, :content_text, :embedding, :metadata)
                    ON CONFLICT (function_name, initiative_id) 
                    DO UPDATE SET 
                        initiative_name = EXCLUDED.initiative_name,
                        content_text = EXCLUDED.content_text,
                        embedding = EXCLUDED.embedding,
                        metadata = EXCLUDED.metadata;
                """), {
                    'function_name': function_name,
                    'initiative_id': initiative_id,
                    'initiative_name': initiative_data.get('name', ''),
                    'content_text': content_text,
                    'embedding': embedding,
                    'metadata': json.dumps(initiative_data)
                })
                conn.commit()
            
            return True
            
        except Exception as e:
            st.error(f"Error storing initiative embedding: {e}")
            return False
    
    def find_similar_initiatives(self, query_text: str, industry: str = None, 
                               limit: int = 5) -> List[Dict[str, Any]]:
        """Find similar AI initiatives using semantic search"""
        if not self.vector_enabled:
            return self._fallback_text_search(query_text, limit)
        
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query_text)
            if not query_embedding:
                return []
            
            # Search for similar initiatives
            with self.db.engine.connect() as conn:
                query_sql = """
                    SELECT 
                        function_name,
                        initiative_id,
                        initiative_name,
                        content_text,
                        metadata,
                        1 - (embedding <=> :query_embedding) as similarity
                    FROM ai_initiative_embeddings
                    WHERE 1 - (embedding <=> :query_embedding) > 0.7
                    ORDER BY embedding <=> :query_embedding
                    LIMIT :limit;
                """
                
                result = conn.execute(text(query_sql), {
                    'query_embedding': query_embedding,
                    'limit': limit
                })
                
                similar_initiatives = []
                for row in result:
                    similar_initiatives.append({
                        'function_name': row.function_name,
                        'initiative_id': row.initiative_id,
                        'initiative_name': row.initiative_name,
                        'similarity_score': row.similarity,
                        'metadata': json.loads(row.metadata) if row.metadata else {}
                    })
                
                return similar_initiatives
                
        except Exception as e:
            st.error(f"Error in semantic search: {e}")
            return []
    
    def _fallback_text_search(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Fallback text-based similarity when vector search is unavailable"""
        # Use session state data for text matching
        similar_initiatives = []
        query_words = set(query_text.lower().split())
        
        for function_name in st.session_state.baseline_data.keys():
            if f'categories_{function_name}' in st.session_state:
                categories = st.session_state[f'categories_{function_name}']
                
                for category_name, category_data in categories.items():
                    initiatives = category_data.get('ai_initiatives', {})
                    
                    for init_id, init_data in initiatives.items():
                        # Calculate text similarity
                        content_text = f"{init_data.get('name', '')} {init_data.get('ai_type', '')} {init_data.get('description', '')}"
                        content_words = set(content_text.lower().split())
                        
                        # Simple Jaccard similarity
                        intersection = len(query_words & content_words)
                        union = len(query_words | content_words)
                        similarity = intersection / union if union > 0 else 0
                        
                        if similarity > 0.1:  # Minimum similarity threshold
                            similar_initiatives.append({
                                'function_name': function_name,
                                'initiative_id': init_id,
                                'initiative_name': init_data.get('name', ''),
                                'similarity_score': similarity,
                                'metadata': init_data
                            })
        
        # Sort by similarity and return top results
        similar_initiatives.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similar_initiatives[:limit]
    
    def store_industry_patterns(self, industry: str, patterns: List[Dict[str, Any]]) -> bool:
        """Store industry-specific AI implementation patterns"""
        if not self.vector_enabled:
            return False
        
        try:
            with self.db.engine.connect() as conn:
                for pattern in patterns:
                    content_text = f"{pattern.get('name', '')} | {pattern.get('description', '')} | {pattern.get('context', '')}"
                    embedding = self.generate_embedding(content_text)
                    
                    if embedding:
                        conn.execute(text("""
                            INSERT INTO industry_pattern_embeddings 
                            (industry, pattern_type, pattern_name, content_text, embedding, metadata)
                            VALUES (:industry, :pattern_type, :pattern_name, :content_text, :embedding, :metadata);
                        """), {
                            'industry': industry,
                            'pattern_type': pattern.get('type', 'general'),
                            'pattern_name': pattern.get('name', ''),
                            'content_text': content_text,
                            'embedding': embedding,
                            'metadata': json.dumps(pattern)
                        })
                
                conn.commit()
            return True
            
        except Exception as e:
            st.error(f"Error storing industry patterns: {e}")
            return False
    
    def get_contextual_recommendations(self, function_name: str, industry: str, 
                                     current_initiatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get contextual recommendations based on current initiatives and industry patterns"""
        
        recommendations = []
        
        # Analyze current initiatives for gaps
        if current_initiatives:
            initiative_types = [init.get('ai_type', '') for init in current_initiatives]
            initiative_descriptions = [f"{init.get('name', '')} {init.get('description', '')}" for init in current_initiatives]
            
            # Find similar initiatives from other functions
            for desc in initiative_descriptions[:2]:  # Limit to avoid too many API calls
                similar = self.find_similar_initiatives(desc, industry, limit=3)
                
                for sim in similar:
                    if sim['function_name'] != function_name:  # Only from other functions
                        recommendations.append({
                            'type': 'Similar Initiative',
                            'source_function': sim['function_name'],
                            'recommendation': f"Consider adapting '{sim['initiative_name']}' for {function_name}",
                            'similarity_score': sim['similarity_score'],
                            'metadata': sim['metadata']
                        })
        
        # Add industry-specific recommendations
        industry_recommendations = self._get_industry_recommendations(industry, function_name)
        recommendations.extend(industry_recommendations)
        
        # Remove duplicates and sort by relevance
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            key = rec.get('recommendation', '')
            if key not in seen:
                seen.add(key)
                unique_recommendations.append(rec)
        
        return unique_recommendations[:10]  # Limit to top 10
    
    def _get_industry_recommendations(self, industry: str, function_name: str) -> List[Dict[str, Any]]:
        """Get industry-specific recommendations"""
        
        # Predefined industry patterns (in a real implementation, these would be stored in the vector database)
        industry_patterns = {
            'Technology': [
                {'type': 'Development Acceleration', 'name': 'AI-Powered Code Generation', 'function_match': 'Engineering'},
                {'type': 'Customer Intelligence', 'name': 'Behavioral Analytics Platform', 'function_match': 'Product'},
                {'type': 'Operational Efficiency', 'name': 'Automated Testing Framework', 'function_match': 'QA'}
            ],
            'Healthcare': [
                {'type': 'Clinical Decision Support', 'name': 'AI Diagnostic Assistant', 'function_match': 'Clinical'},
                {'type': 'Patient Experience', 'name': 'Personalized Treatment Plans', 'function_match': 'Patient Care'},
                {'type': 'Operational Efficiency', 'name': 'Resource Optimization System', 'function_match': 'Operations'}
            ],
            'Financial Services': [
                {'type': 'Risk Management', 'name': 'Real-time Fraud Detection', 'function_match': 'Risk'},
                {'type': 'Customer Experience', 'name': 'Personalized Financial Advisory', 'function_match': 'Customer'},
                {'type': 'Compliance', 'name': 'Automated Regulatory Reporting', 'function_match': 'Compliance'}
            ],
            'Retail': [
                {'type': 'Customer Experience', 'name': 'Personalized Recommendation Engine', 'function_match': 'Customer'},
                {'type': 'Supply Chain', 'name': 'Demand Forecasting System', 'function_match': 'Supply'},
                {'type': 'Operations', 'name': 'Dynamic Pricing Optimization', 'function_match': 'Operations'}
            ]
        }
        
        patterns = industry_patterns.get(industry, [])
        recommendations = []
        
        for pattern in patterns:
            if any(word in function_name.lower() for word in pattern['function_match'].lower().split()):
                recommendations.append({
                    'type': 'Industry Best Practice',
                    'source': f'{industry} Industry',
                    'recommendation': f"Implement {pattern['name']} for {pattern['type'].lower()}",
                    'pattern_type': pattern['type'],
                    'relevance_score': 0.8
                })
        
        return recommendations

class SemanticAnalyzer:
    """Semantic analysis for cross-functional insights"""
    
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db
    
    def analyze_initiative_clusters(self, baseline_data: Dict, categories_data: Dict) -> Dict[str, Any]:
        """Analyze clusters of similar AI initiatives across functions"""
        
        all_initiatives = []
        
        # Collect all initiatives
        for function_name in baseline_data.keys():
            if f'categories_{function_name}' in categories_data:
                categories = categories_data[f'categories_{function_name}']
                
                for category_name, category_data in categories.items():
                    initiatives = category_data.get('ai_initiatives', {})
                    
                    for init_id, init_data in initiatives.items():
                        all_initiatives.append({
                            'function_name': function_name,
                            'category_name': category_name,
                            'initiative_id': init_id,
                            'initiative_data': init_data
                        })
        
        if len(all_initiatives) < 2:
            return {'clusters': [], 'insights': []}
        
        # Find clusters using semantic similarity
        clusters = self._cluster_initiatives(all_initiatives)
        
        # Generate insights from clusters
        insights = self._generate_cluster_insights(clusters)
        
        return {
            'clusters': clusters,
            'insights': insights
        }
    
    def _cluster_initiatives(self, initiatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Cluster initiatives by semantic similarity"""
        
        clusters = []
        processed = set()
        
        for i, init1 in enumerate(initiatives):
            if i in processed:
                continue
            
            # Start new cluster
            cluster = {
                'id': len(clusters),
                'initiatives': [init1],
                'ai_types': [init1['initiative_data'].get('ai_type', '')],
                'functions': [init1['function_name']],
                'theme': init1['initiative_data'].get('ai_type', 'Mixed')
            }
            
            processed.add(i)
            
            # Find similar initiatives
            init1_text = f"{init1['initiative_data'].get('name', '')} {init1['initiative_data'].get('ai_type', '')}"
            
            for j, init2 in enumerate(initiatives[i+1:], i+1):
                if j in processed:
                    continue
                
                init2_text = f"{init2['initiative_data'].get('name', '')} {init2['initiative_data'].get('ai_type', '')}"
                
                # Simple similarity check (in production, would use vector similarity)
                similarity = self._calculate_text_similarity(init1_text, init2_text)
                
                if similarity > 0.3:  # Similarity threshold
                    cluster['initiatives'].append(init2)
                    cluster['ai_types'].append(init2['initiative_data'].get('ai_type', ''))
                    cluster['functions'].append(init2['function_name'])
                    processed.add(j)
            
            # Only keep clusters with multiple initiatives
            if len(cluster['initiatives']) > 1:
                cluster['functions'] = list(set(cluster['functions']))
                cluster['ai_types'] = list(set(cluster['ai_types']))
                clusters.append(cluster)
        
        return clusters
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0
    
    def _generate_cluster_insights(self, clusters: List[Dict[str, Any]]) -> List[str]:
        """Generate insights from initiative clusters"""
        
        insights = []
        
        for cluster in clusters:
            if len(cluster['initiatives']) > 2:
                insights.append(
                    f"Found {len(cluster['initiatives'])} similar {cluster['theme']} initiatives "
                    f"across {len(cluster['functions'])} functions: {', '.join(cluster['functions'])}"
                )
            
            # Check for cross-functional opportunities
            if len(cluster['functions']) > 1:
                total_investment = sum(
                    init['initiative_data'].get('investment', 0) 
                    for init in cluster['initiatives']
                )
                insights.append(
                    f"Cross-functional synergy opportunity: ${total_investment:,.0f} invested in "
                    f"similar initiatives across {', '.join(cluster['functions'])}"
                )
        
        if not insights:
            insights.append("No significant clustering patterns found. Consider more diverse AI initiatives.")
        
        return insights