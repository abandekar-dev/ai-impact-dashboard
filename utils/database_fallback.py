"""
Fallback database implementation using session state for data persistence
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class DatabaseManagerFallback:
    """Fallback database manager using local storage"""
    
    def __init__(self):
        self.storage_file = "dashboard_data.json"
        self.is_available = True
        
    def save_function_baseline(self, function_name: str, baseline_data: Dict):
        """Save function baseline data"""
        data = self._load_all_data()
        if 'baseline_data' not in data:
            data['baseline_data'] = {}
        data['baseline_data'][function_name] = baseline_data
        data['last_updated'] = datetime.now().isoformat()
        self._save_all_data(data)
        
    def save_ai_initiative(self, function_name: str, initiative_data: Dict):
        """Save AI initiative data"""
        data = self._load_all_data()
        if 'ai_initiatives' not in data:
            data['ai_initiatives'] = {}
        if function_name not in data['ai_initiatives']:
            data['ai_initiatives'][function_name] = {}
        data['ai_initiatives'][function_name].update(initiative_data)
        data['last_updated'] = datetime.now().isoformat()
        self._save_all_data(data)
        
    def save_prediction(self, function_name: str, predictions: Dict):
        """Save prediction data"""
        data = self._load_all_data()
        if 'predictions' not in data:
            data['predictions'] = {}
        data['predictions'][function_name] = predictions
        data['last_updated'] = datetime.now().isoformat()
        self._save_all_data(data)
        
    def load_all_data(self) -> Dict[str, Any]:
        """Load all dashboard data"""
        data = self._load_all_data()
        return {
            'baseline_data': data.get('baseline_data', {}),
            'ai_initiatives': data.get('ai_initiatives', {}),
            'predictions': data.get('predictions', {})
        }
        
    def _load_all_data(self) -> Dict[str, Any]:
        """Load data from storage file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
        
    def _save_all_data(self, data: Dict[str, Any]):
        """Save data to storage file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except IOError:
            pass  # Silent fail for file write issues