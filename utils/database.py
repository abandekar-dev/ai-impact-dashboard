import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from typing import Dict, List, Optional

Base = declarative_base()

class EnterpriseFunction(Base):
    __tablename__ = 'enterprise_functions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    current_productivity = Column(Float)
    headcount = Column(Integer)
    annual_revenue = Column(Float)
    annual_costs = Column(Float)
    performance_satisfaction = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AIInitiative(Base):
    __tablename__ = 'ai_initiatives'
    
    id = Column(Integer, primary_key=True)
    function_name = Column(String(100), nullable=False)
    ai_type = Column(String(50))
    complexity = Column(String(20))
    investment = Column(Float)
    timeline = Column(String(50))
    change_management = Column(String(50))
    technical_risk = Column(Float)
    adoption_risk = Column(Float)
    integration_risk = Column(Float)
    regulatory_risk = Column(Float)
    competitive_risk = Column(Float)
    data_risk = Column(Float)
    automation_level = Column(Float)
    accuracy_improvement = Column(Float)
    speed_improvement = Column(Float)
    workforce_reduction = Column(Float)
    upskilling_required = Column(Float)
    new_roles_created = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Prediction(Base):
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True)
    function_name = Column(String(100), nullable=False)
    productivity_gain = Column(Float)
    value_generated = Column(Float)
    roi = Column(Float)
    payback_period = Column(Float)
    workforce_impact = Column(JSON)
    risk_adjusted_roi = Column(Float)
    confidence_interval = Column(JSON)
    monthly_value = Column(Float)
    annual_savings = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    """Database manager for AI Impact Dashboard"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not found")
        
        # Configure engine with connection pooling and retry logic
        self.engine = create_engine(
            self.database_url,
            pool_pre_ping=True,  # Validate connections before use
            pool_recycle=300,    # Recycle connections every 5 minutes
            pool_size=5,
            max_overflow=10,
            connect_args={
                "connect_timeout": 10,
                "application_name": "ai_dashboard"
            }
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables with retry logic
        self._create_tables_with_retry()
    
    def _create_tables_with_retry(self, max_retries=3):
        """Create database tables with retry logic"""
        import time
        for attempt in range(max_retries):
            try:
                Base.metadata.create_all(bind=self.engine)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise e
    
    def get_session(self):
        """Get database session with connection validation"""
        return self.SessionLocal()
    
    def _execute_with_retry(self, operation, *args, **kwargs):
        """Execute database operation with retry logic"""
        import time
        max_retries = 3
        for attempt in range(max_retries):
            session = None
            try:
                session = self.get_session()
                result = operation(session, *args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                if session:
                    session.rollback()
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                print(f"Database operation failed after {max_retries} attempts: {e}")
                return False
            finally:
                if session:
                    session.close()
    
    def save_function_baseline(self, function_name: str, baseline_data: Dict) -> bool:
        """Save or update enterprise function baseline data"""
        session = None
        try:
            session = self.get_session()
            
            # Check if function exists
            existing_function = session.query(EnterpriseFunction).filter(
                EnterpriseFunction.name == function_name
            ).first()
            
            if existing_function:
                # Update existing
                existing_function.current_productivity = baseline_data['productivity']
                existing_function.headcount = baseline_data['headcount']
                existing_function.annual_revenue = baseline_data['revenue']
                existing_function.annual_costs = baseline_data['costs']
                existing_function.performance_satisfaction = baseline_data['satisfaction']
            else:
                # Create new
                new_function = EnterpriseFunction(
                    name=function_name,
                    current_productivity=baseline_data['productivity'],
                    headcount=baseline_data['headcount'],
                    annual_revenue=baseline_data['revenue'],
                    annual_costs=baseline_data['costs'],
                    performance_satisfaction=baseline_data['satisfaction']
                )
                session.add(new_function)
            
            session.commit()
            return True
            
        except Exception as e:
            if session:
                session.rollback()
            print(f"Error saving function baseline: {e}")
            return False
        finally:
            if session:
                session.close()
    
    def save_ai_initiative(self, function_name: str, initiative_data: Dict) -> bool:
        """Save or update AI initiative data"""
        session = None
        try:
            session = self.get_session()
            
            # Check if initiative exists
            existing_initiative = session.query(AIInitiative).filter(
                AIInitiative.function_name == function_name
            ).first()
            
            if existing_initiative:
                # Update existing
                for key, value in initiative_data.items():
                    if hasattr(existing_initiative, key):
                        setattr(existing_initiative, key, value)
            else:
                # Create new
                new_initiative = AIInitiative(
                    function_name=function_name,
                    **initiative_data
                )
                session.add(new_initiative)
            
            session.commit()
            return True
            
        except Exception as e:
            if session:
                session.rollback()
            print(f"Error saving AI initiative: {e}")
            return False
        finally:
            if session:
                session.close()
    
    def save_prediction(self, function_name: str, prediction_data: Dict) -> bool:
        """Save prediction results"""
        session = None
        try:
            session = self.get_session()
            
            new_prediction = Prediction(
                function_name=function_name,
                productivity_gain=prediction_data.get('productivity_gain'),
                value_generated=prediction_data.get('value_generated'),
                roi=prediction_data.get('roi'),
                payback_period=prediction_data.get('payback_period'),
                workforce_impact=prediction_data.get('workforce_impact'),
                risk_adjusted_roi=prediction_data.get('risk_adjusted_roi'),
                confidence_interval=prediction_data.get('confidence_interval'),
                monthly_value=prediction_data.get('monthly_value'),
                annual_savings=prediction_data.get('annual_savings')
            )
            
            session.add(new_prediction)
            session.commit()
            return True
            
        except Exception as e:
            if session:
                session.rollback()
            print(f"Error saving prediction: {e}")
            return False
        finally:
            if session:
                session.close()
    
    def load_function_baseline(self, function_name: str) -> Optional[Dict]:
        """Load function baseline data"""
        session = None
        try:
            session = self.get_session()
            
            function = session.query(EnterpriseFunction).filter(
                EnterpriseFunction.name == function_name
            ).first()
            
            if function:
                return {
                    'productivity': function.current_productivity,
                    'headcount': function.headcount,
                    'revenue': function.annual_revenue,
                    'costs': function.annual_costs,
                    'satisfaction': function.performance_satisfaction
                }
            return None
            
        except Exception as e:
            print(f"Error loading function baseline: {e}")
            return None
        finally:
            if session:
                session.close()
    
    def load_ai_initiative(self, function_name: str) -> Optional[Dict]:
        """Load AI initiative data"""
        session = None
        try:
            session = self.get_session()
            
            initiative = session.query(AIInitiative).filter(
                AIInitiative.function_name == function_name
            ).first()
            
            if initiative:
                return {
                    'type': initiative.ai_type,
                    'complexity': initiative.complexity,
                    'investment': initiative.investment,
                    'timeline': initiative.timeline,
                    'change_management': initiative.change_management,
                    'technical_risk': initiative.technical_risk,
                    'adoption_risk': initiative.adoption_risk,
                    'integration_risk': initiative.integration_risk,
                    'automation_level': initiative.automation_level,
                    'accuracy_improvement': initiative.accuracy_improvement,
                    'speed_improvement': initiative.speed_improvement,
                    'workforce_reduction': initiative.workforce_reduction,
                    'upskilling_required': initiative.upskilling_required,
                    'new_roles_created': initiative.new_roles_created
                }
            return None
            
        except Exception as e:
            print(f"Error loading AI initiative: {e}")
            return None
        finally:
            if session:
                session.close()
    
    def load_latest_prediction(self, function_name: str) -> Optional[Dict]:
        """Load latest prediction for a function"""
        session = None
        try:
            session = self.get_session()
            
            prediction = session.query(Prediction).filter(
                Prediction.function_name == function_name
            ).order_by(Prediction.created_at.desc()).first()
            
            session.close()
            
            if prediction:
                return {
                    'productivity_gain': prediction.productivity_gain,
                    'value_generated': prediction.value_generated,
                    'roi': prediction.roi,
                    'payback_period': prediction.payback_period,
                    'workforce_impact': prediction.workforce_impact,
                    'risk_adjusted_roi': prediction.risk_adjusted_roi,
                    'confidence_interval': prediction.confidence_interval,
                    'monthly_value': prediction.monthly_value,
                    'annual_savings': prediction.annual_savings
                }
            return None
            
        except Exception as e:
            if session:
                session.close()
            print(f"Error loading prediction: {e}")
            return None
    
    def get_all_configured_functions(self) -> List[str]:
        """Get list of all configured functions"""
        session = None
        try:
            session = self.get_session()
            
            functions = session.query(EnterpriseFunction.name).all()
            session.close()
            
            return [f[0] for f in functions]
            
        except Exception as e:
            if session:
                session.close()
            print(f"Error getting configured functions: {e}")
            return []
    
    def load_all_data(self) -> Dict:
        """Load all data for session state"""
        try:
            baseline_data = {}
            ai_initiatives = {}
            predictions = {}
            
            configured_functions = self.get_all_configured_functions()
            
            for function_name in configured_functions:
                # Load baseline data
                baseline = self.load_function_baseline(function_name)
                if baseline:
                    baseline_data[function_name] = baseline
                
                # Load AI initiative data
                initiative = self.load_ai_initiative(function_name)
                if initiative:
                    ai_initiatives[function_name] = initiative
                
                # Load latest prediction
                prediction = self.load_latest_prediction(function_name)
                if prediction:
                    predictions[function_name] = prediction
            
            return {
                'baseline_data': baseline_data,
                'ai_initiatives': ai_initiatives,
                'predictions': predictions
            }
            
        except Exception as e:
            print(f"Error loading all data: {e}")
            return {
                'baseline_data': {},
                'ai_initiatives': {},
                'predictions': {}
            }
    
    def get_prediction_history(self, function_name: str, limit: int = 10) -> List[Dict]:
        """Get prediction history for a function"""
        session = None
        try:
            session = self.get_session()
            
            predictions = session.query(Prediction).filter(
                Prediction.function_name == function_name
            ).order_by(Prediction.created_at.desc()).limit(limit).all()
            
            session.close()
            
            history = []
            for pred in predictions:
                history.append({
                    'date': pred.created_at,
                    'productivity_gain': pred.productivity_gain,
                    'value_generated': pred.value_generated,
                    'roi': pred.roi,
                    'payback_period': pred.payback_period
                })
            
            return history
            
        except Exception as e:
            if session:
                session.close()
            print(f"Error getting prediction history: {e}")
            return []
    
    def export_data_to_csv(self) -> pd.DataFrame:
        """Export all data to CSV format"""
        session = None
        try:
            session = self.get_session()
            
            # Join all tables to get complete view
            query = session.query(
                EnterpriseFunction.name,
                EnterpriseFunction.current_productivity,
                EnterpriseFunction.headcount,
                EnterpriseFunction.annual_revenue,
                EnterpriseFunction.annual_costs,
                AIInitiative.ai_type,
                AIInitiative.complexity,
                AIInitiative.investment,
                AIInitiative.timeline,
                Prediction.productivity_gain,
                Prediction.value_generated,
                Prediction.roi,
                Prediction.payback_period,
                Prediction.created_at
            ).outerjoin(
                AIInitiative, EnterpriseFunction.name == AIInitiative.function_name
            ).outerjoin(
                Prediction, EnterpriseFunction.name == Prediction.function_name
            )
            
            df = pd.read_sql(query.statement, session.bind)
            session.close()
            
            return df
            
        except Exception as e:
            if session:
                session.close()
            print(f"Error exporting data: {e}")
            return pd.DataFrame()