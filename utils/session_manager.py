import streamlit as st
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
from .database import DatabaseManager

class SessionManager:
    """Manage analysis sessions and data persistence"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def save_session(self, session_name: str, description: str = "") -> bool:
        """Save current session state to database"""
        try:
            session = self.db.get_session()
            
            # Create sessions table if it doesn't exist
            session.execute("""
                CREATE TABLE IF NOT EXISTS analysis_sessions (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    baseline_data JSON,
                    ai_initiatives JSON,
                    predictions JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Check if session name already exists
            existing = session.execute(
                "SELECT id FROM analysis_sessions WHERE name = %s",
                (session_name,)
            ).fetchone()
            
            session_data = {
                'baseline_data': st.session_state.baseline_data,
                'ai_initiatives': st.session_state.ai_initiatives,
                'predictions': st.session_state.predictions
            }
            
            if existing:
                # Update existing session
                session.execute("""
                    UPDATE analysis_sessions 
                    SET description = %s, baseline_data = %s, ai_initiatives = %s, 
                        predictions = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE name = %s
                """, (
                    description,
                    json.dumps(session_data['baseline_data']),
                    json.dumps(session_data['ai_initiatives']),
                    json.dumps(session_data['predictions']),
                    session_name
                ))
            else:
                # Create new session
                session.execute("""
                    INSERT INTO analysis_sessions (name, description, baseline_data, ai_initiatives, predictions)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    session_name,
                    description,
                    json.dumps(session_data['baseline_data']),
                    json.dumps(session_data['ai_initiatives']),
                    json.dumps(session_data['predictions'])
                ))
            
            session.commit()
            return True
            
        except Exception as e:
            if session:
                session.rollback()
            print(f"Error saving session: {e}")
            return False
        finally:
            if session:
                session.close()
    
    def load_session(self, session_name: str) -> bool:
        """Load session state from database"""
        try:
            session = self.db.get_session()
            
            result = session.execute(
                "SELECT baseline_data, ai_initiatives, predictions FROM analysis_sessions WHERE name = %s",
                (session_name,)
            ).fetchone()
            
            if result:
                baseline_data, ai_initiatives, predictions = result
                
                # Load data into session state
                st.session_state.baseline_data = json.loads(baseline_data) if baseline_data else {}
                st.session_state.ai_initiatives = json.loads(ai_initiatives) if ai_initiatives else {}
                st.session_state.predictions = json.loads(predictions) if predictions else {}
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Error loading session: {e}")
            return False
        finally:
            if session:
                session.close()
    
    def get_saved_sessions(self) -> List[Dict]:
        """Get list of all saved sessions"""
        try:
            session = self.db.get_session()
            
            # Check if table exists
            try:
                results = session.execute("""
                    SELECT name, description, created_at, updated_at 
                    FROM analysis_sessions 
                    ORDER BY updated_at DESC
                """).fetchall()
                
                sessions = []
                for result in results:
                    name, description, created_at, updated_at = result
                    sessions.append({
                        'name': name,
                        'description': description or 'No description',
                        'created_at': created_at,
                        'updated_at': updated_at
                    })
                
                return sessions
                
            except Exception:
                # Table doesn't exist yet
                return []
            
        except Exception as e:
            print(f"Error getting sessions: {e}")
            return []
        finally:
            if session:
                session.close()
    
    def delete_session(self, session_name: str) -> bool:
        """Delete a saved session"""
        try:
            session = self.db.get_session()
            
            session.execute(
                "DELETE FROM analysis_sessions WHERE name = %s",
                (session_name,)
            )
            
            session.commit()
            return True
            
        except Exception as e:
            if session:
                session.rollback()
            print(f"Error deleting session: {e}")
            return False
        finally:
            if session:
                session.close()
    
    def export_session(self, session_name: str) -> Optional[Dict]:
        """Export session data for download"""
        try:
            session = self.db.get_session()
            
            result = session.execute(
                "SELECT * FROM analysis_sessions WHERE name = %s",
                (session_name,)
            ).fetchone()
            
            if result:
                return {
                    'session_name': result[1],
                    'description': result[2],
                    'baseline_data': json.loads(result[3]) if result[3] else {},
                    'ai_initiatives': json.loads(result[4]) if result[4] else {},
                    'predictions': json.loads(result[5]) if result[5] else {},
                    'created_at': str(result[6]),
                    'updated_at': str(result[7])
                }
            
            return None
            
        except Exception as e:
            print(f"Error exporting session: {e}")
            return None
        finally:
            if session:
                session.close()