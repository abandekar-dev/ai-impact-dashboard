import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Optional

class SessionManager:
    """Manage analysis sessions using Streamlit's built-in session state"""
    
    def __init__(self, db_manager=None):
        self.db = db_manager
        # Initialize session storage in Streamlit's session state
        if 'saved_sessions' not in st.session_state:
            st.session_state.saved_sessions = {}
    
    def save_session(self, session_name: str, description: str = "") -> bool:
        """Save current session state"""
        try:
            session_data = {
                'name': session_name,
                'description': description,
                'baseline_data': dict(st.session_state.baseline_data),
                'ai_initiatives': dict(st.session_state.ai_initiatives),
                'predictions': dict(st.session_state.predictions),
                'saved_at': datetime.now().isoformat()
            }
            
            st.session_state.saved_sessions[session_name] = session_data
            
            # Also save to database if available
            if self.db:
                try:
                    # Use the existing database methods
                    for func_name, baseline in st.session_state.baseline_data.items():
                        self.db.save_function_baseline(func_name, baseline)
                    
                    for func_name, initiative in st.session_state.ai_initiatives.items():
                        self.db.save_ai_initiative(func_name, initiative)
                    
                    for func_name, prediction in st.session_state.predictions.items():
                        self.db.save_prediction(func_name, prediction)
                        
                except Exception as e:
                    print(f"Database save failed, but session saved locally: {e}")
            
            return True
            
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def load_session(self, session_name: str) -> bool:
        """Load session state"""
        try:
            if session_name in st.session_state.saved_sessions:
                session_data = st.session_state.saved_sessions[session_name]
                
                # Load data into session state
                st.session_state.baseline_data = session_data['baseline_data']
                st.session_state.ai_initiatives = session_data['ai_initiatives']
                st.session_state.predictions = session_data['predictions']
                
                return True
            
            # Try loading from database if available
            if self.db:
                try:
                    configured_functions = self.db.get_all_configured_functions()
                    if configured_functions:
                        # Load from database
                        data = self.db.load_all_data()
                        st.session_state.baseline_data = data['baseline_data']
                        st.session_state.ai_initiatives = data['ai_initiatives']
                        st.session_state.predictions = data['predictions']
                        return True
                except Exception as e:
                    print(f"Database load failed: {e}")
            
            return False
            
        except Exception as e:
            print(f"Error loading session: {e}")
            return False
    
    def get_saved_sessions(self) -> List[Dict]:
        """Get list of all saved sessions"""
        try:
            sessions = []
            
            # Get sessions from session state
            for name, data in st.session_state.saved_sessions.items():
                sessions.append({
                    'name': name,
                    'description': data.get('description', 'No description'),
                    'updated_at': data.get('saved_at', datetime.now().isoformat())
                })
            
            # Sort by update time (most recent first)
            sessions.sort(key=lambda x: x['updated_at'], reverse=True)
            return sessions
                
        except Exception as e:
            print(f"Error getting sessions: {e}")
            return []
    
    def delete_session(self, session_name: str) -> bool:
        """Delete a saved session"""
        try:
            if session_name in st.session_state.saved_sessions:
                del st.session_state.saved_sessions[session_name]
                return True
            return False
            
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
    
    def export_session(self, session_name: str) -> Optional[Dict]:
        """Export session data for download"""
        try:
            if session_name in st.session_state.saved_sessions:
                return st.session_state.saved_sessions[session_name]
            return None
            
        except Exception as e:
            print(f"Error exporting session: {e}")
            return None