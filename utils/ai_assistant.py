import streamlit as st
import json
import os
from typing import Dict, List, Any, Optional

# Handle OpenAI import with fallback
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    # Mock OpenAI class for compatibility
    class OpenAI:
        def __init__(self, api_key=None):
            pass
        
        @property
        def chat(self):
            return MockChat()
    
    class MockChat:
        @property
        def completions(self):
            return MockCompletions()
    
    class MockCompletions:
        def create(self, **kwargs):
            return MockResponse()
            
    class MockResponse:
        def __init__(self):
            self.choices = [MockChoice()]
    
    class MockChoice:
        def __init__(self):
            self.message = MockMessage()
    
    class MockMessage:
        def __init__(self):
            self.content = "AI Assistant is not available without OpenAI API key."

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if OPENAI_AVAILABLE:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = OpenAI()

class AIAssistant:
    """Conversational AI assistant for the dashboard"""
    
    def __init__(self):
        self.client = openai_client
        self.conversation_history = []
        
    def analyze_dashboard_data(self, question: str, context_data: Dict) -> str:
        """Analyze dashboard data and provide intelligent responses"""
        
        # Prepare context summary
        context_summary = self._prepare_context_summary(context_data)
        
        # Create system prompt for dashboard analysis
        system_prompt = f"""You are an expert AI business analyst helping C-level executives understand their AI implementation strategy dashboard. 

Current Dashboard Context:
{context_summary}

Guidelines for responses:
1. Provide clear, executive-level insights
2. Use specific numbers and metrics from the data
3. Offer actionable recommendations
4. Keep responses concise but comprehensive
5. Focus on business value and strategic implications
6. Highlight risks and opportunities
7. Use business terminology appropriate for executives

Answer the user's question based on the dashboard data provided."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        # Add conversation history for context
        for msg in self.conversation_history[-3:]:  # Keep last 3 exchanges
            messages.insert(-1, msg)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=800,
                temperature=0.3
            )
            
            answer = response.choices[0].message.content
            
            # Store conversation
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})
            
            return answer
            
        except Exception as e:
            return f"I'm having trouble analyzing your data right now. Please ensure your API connection is working properly. Error: {str(e)}"
    
    def _prepare_context_summary(self, context_data: Dict) -> str:
        """Prepare a comprehensive summary of dashboard data"""
        
        summary_parts = []
        
        # Baseline data summary
        if context_data.get('baseline_data'):
            baseline = context_data['baseline_data']
            summary_parts.append("## Current Enterprise Functions:")
            for func_name, data in baseline.items():
                summary_parts.append(f"- {func_name}: {data.get('headcount', 0)} employees, ${data.get('revenue', 0):,.0f} revenue, ${data.get('costs', 0):,.0f} costs")
        
        # AI initiatives summary
        if context_data.get('ai_initiatives'):
            total_investment = sum(init.get('investment', 0) for init in context_data['ai_initiatives'].values())
            summary_parts.append(f"\n## AI Initiatives: {len(context_data['ai_initiatives'])} configured, Total Investment: ${total_investment:,.0f}")
            
            for func_name, initiative in context_data['ai_initiatives'].items():
                summary_parts.append(f"- {func_name}: {initiative.get('ai_type', 'Unknown')} ({initiative.get('complexity', 'Unknown')} complexity), ${initiative.get('investment', 0):,.0f}")
        
        # Predictions summary
        if context_data.get('predictions'):
            summary_parts.append("\n## Prediction Results:")
            total_roi = 0
            total_productivity = 0
            
            for func_name, pred in context_data['predictions'].items():
                roi = pred.get('roi', 0)
                productivity = pred.get('productivity_gain', 0)
                total_roi += roi
                total_productivity += productivity
                
                summary_parts.append(f"- {func_name}: {roi:.1f}% ROI, {productivity:.1f}% productivity gain, {pred.get('payback_period', 0):.1f} months payback")
            
            avg_roi = total_roi / len(context_data['predictions']) if context_data['predictions'] else 0
            summary_parts.append(f"\nAverage ROI: {avg_roi:.1f}%")
        
        # Corporate objectives
        if context_data.get('corporate_objectives'):
            objectives = context_data['corporate_objectives']
            summary_parts.append(f"\n## Corporate Objectives: {len(objectives.get('strategic_objectives', []))} strategic goals")
            for obj in objectives.get('strategic_objectives', [])[:3]:
                summary_parts.append(f"- {obj.get('name', 'Unnamed')}: {obj.get('target_value', 0)} {obj.get('metric', '')}")
        
        # Budget constraints
        if context_data.get('budget_constraints'):
            budget = context_data['budget_constraints']
            summary_parts.append(f"\n## Budget: ${budget.get('total_ai_budget', 0):,.0f} total, {budget.get('risk_tolerance', 'Unknown')} risk tolerance")
        
        # Change management readiness
        if context_data.get('change_readiness'):
            readiness = context_data['change_readiness']
            summary_parts.append(f"\n## Change Readiness: {readiness.get('overall_readiness_score', 0):.1f}/100 overall score")
        
        return "\n".join(summary_parts)
    
    def get_suggested_questions(self, context_data: Dict) -> List[str]:
        """Generate suggested questions based on current data"""
        
        suggestions = [
            "What's our overall ROI projection across all AI initiatives?",
            "Which department should we prioritize for AI implementation?",
            "What are the main risks in our AI strategy?",
            "How long will it take to see returns on our AI investment?",
            "Are we adequately prepared for the organizational changes?"
        ]
        
        # Add context-specific suggestions
        if context_data.get('predictions'):
            functions = list(context_data['predictions'].keys())
            if len(functions) > 1:
                suggestions.append(f"Compare the ROI between {functions[0]} and {functions[1]}")
        
        if context_data.get('budget_constraints'):
            suggestions.append("Is our budget allocation optimal across departments?")
        
        if context_data.get('change_readiness'):
            suggestions.append("What change management strategies should we focus on?")
        
        return suggestions[:6]  # Return top 6 suggestions
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def export_conversation(self) -> str:
        """Export conversation history as text"""
        if not self.conversation_history:
            return "No conversation history available."
        
        export_text = "AI Assistant Conversation Export\n"
        export_text += "=" * 40 + "\n\n"
        
        for i, msg in enumerate(self.conversation_history):
            role = "Executive" if msg["role"] == "user" else "AI Assistant"
            export_text += f"{role}: {msg['content']}\n\n"
        
        return export_text

class DashboardDataCollector:
    """Collects and organizes dashboard data for AI analysis"""
    
    @staticmethod
    def collect_dashboard_context() -> Dict[str, Any]:
        """Collect all relevant dashboard data for AI analysis"""
        
        context = {}
        
        # Collect baseline data
        if hasattr(st.session_state, 'baseline_data') and st.session_state.baseline_data:
            context['baseline_data'] = st.session_state.baseline_data
        
        # Collect AI initiatives
        if hasattr(st.session_state, 'ai_initiatives') and st.session_state.ai_initiatives:
            context['ai_initiatives'] = st.session_state.ai_initiatives
        
        # Collect predictions
        if hasattr(st.session_state, 'predictions') and st.session_state.predictions:
            context['predictions'] = st.session_state.predictions
        
        # Collect corporate objectives
        if hasattr(st.session_state, 'corporate_objectives') and st.session_state.corporate_objectives:
            context['corporate_objectives'] = st.session_state.corporate_objectives
        
        # Collect budget constraints
        if hasattr(st.session_state, 'budget_constraints') and st.session_state.budget_constraints:
            context['budget_constraints'] = st.session_state.budget_constraints
        
        # Collect change management data
        if hasattr(st.session_state, 'change_readiness') and st.session_state.change_readiness:
            context['change_readiness'] = st.session_state.change_readiness
        
        # Collect category manager data
        if hasattr(st.session_state, 'category_manager') and st.session_state.category_manager:
            # Get aggregated function data
            aggregated_data = {}
            for function_name in st.session_state.category_manager.categories.keys():
                summary = st.session_state.category_manager.get_function_summary(function_name)
                if summary['total_initiatives'] > 0:
                    aggregated_data[function_name] = summary
            
            if aggregated_data:
                context['function_summaries'] = aggregated_data
        
        return context
    
    @staticmethod
    def get_data_completeness() -> float:
        """Calculate how much data is available for analysis"""
        
        required_sections = [
            'baseline_data',
            'ai_initiatives', 
            'predictions',
            'corporate_objectives',
            'budget_constraints'
        ]
        
        completed_sections = 0
        for section in required_sections:
            if hasattr(st.session_state, section) and getattr(st.session_state, section):
                completed_sections += 1
        
        return (completed_sections / len(required_sections)) * 100