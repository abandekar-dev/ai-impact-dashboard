import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.model_selection import cross_val_score, GridSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_regression
import warnings
warnings.filterwarnings('ignore')

from .data_models import MetricsCalculator, TimeSeriesGenerator

class EnsemblePredictor:
    """Advanced ensemble predictor combining multiple ML algorithms"""
    
    def __init__(self, base_models):
        self.base_models = base_models
        self.weights = None
        self.is_fitted = False
        
    def fit(self, X, y):
        """Fit all base models and learn optimal weights"""
        if len(X) < 5:  # Not enough data for proper training
            return self._use_domain_knowledge(X, y)
            
        # Fit all base models
        predictions = {}
        for name, model in self.base_models.items():
            try:
                model.fit(X, y)
                # Use cross-validation to get predictions
                cv_scores = cross_val_score(model, X, y, cv=min(3, len(X)), scoring='r2')
                predictions[name] = cv_scores.mean()
            except:
                predictions[name] = 0.0
        
        # Calculate ensemble weights based on performance
        total_score = sum(max(score, 0) for score in predictions.values())
        if total_score > 0:
            self.weights = {name: max(score, 0) / total_score for name, score in predictions.items()}
        else:
            # Equal weights if no model performs well
            self.weights = {name: 1.0 / len(self.base_models) for name in self.base_models.keys()}
        
        self.is_fitted = True
        return self
    
    def predict(self, X):
        """Make ensemble predictions"""
        if not self.is_fitted:
            return self._fallback_prediction(X)
        
        predictions = []
        total_weight = 0
        
        for name, model in self.base_models.items():
            try:
                pred = model.predict(X)[0]
                weight = self.weights.get(name, 0)
                predictions.append(pred * weight)
                total_weight += weight
            except:
                continue
        
        if total_weight > 0 and predictions:
            return sum(predictions) / total_weight
        else:
            return self._fallback_prediction(X)
    
    def _use_domain_knowledge(self, X, y):
        """Use domain knowledge when insufficient data"""
        # Fit a simple model for minimal data scenarios
        simple_model = LinearRegression()
        try:
            simple_model.fit(X, y)
            self.base_models['simple'] = simple_model
            self.weights = {'simple': 1.0}
        except:
            self.weights = {name: 1.0 / len(self.base_models) for name in self.base_models.keys()}
        
        self.is_fitted = True
        return self
    
    def _fallback_prediction(self, X):
        """Fallback prediction using domain knowledge"""
        # Extract key features for rule-based prediction
        if X.shape[1] >= 7:  # Ensure we have enough features
            productivity = X[0, 0] if X.shape[1] > 0 else 50
            automation_level = X[0, 6] if X.shape[1] > 6 else 30
            investment_ratio = X[0, 17] if X.shape[1] > 17 else 0.1
            
            # Simple rule-based prediction
            base_impact = automation_level * 0.5
            investment_penalty = investment_ratio * 10
            productivity_bonus = (productivity - 50) * 0.2
            
            return base_impact + productivity_bonus - investment_penalty
        
        return 15.0  # Default conservative estimate

class PredictiveEngine:
    """Main engine for predictive modeling of AI implementation impact"""
    
    def __init__(self):
        self.metrics_calc = MetricsCalculator()
        self.ts_generator = TimeSeriesGenerator()
        self.models = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize advanced machine learning models with ensemble capabilities"""
        # Base models with optimized hyperparameters
        self.base_models = {
            'rf': RandomForestRegressor(
                n_estimators=200, 
                max_depth=10, 
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            ),
            'gb': GradientBoostingRegressor(
                n_estimators=150, 
                learning_rate=0.1, 
                max_depth=6,
                subsample=0.8,
                random_state=42
            ),
            'et': ExtraTreesRegressor(
                n_estimators=200,
                max_depth=12,
                min_samples_split=5,
                random_state=42
            ),
            'ridge': Ridge(alpha=1.0),
            'lasso': Lasso(alpha=0.1),
            'elastic': ElasticNet(alpha=0.1, l1_ratio=0.5),
            'svr': SVR(kernel='rbf', C=1.0, gamma='scale'),
            'mlp': MLPRegressor(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=42,
                early_stopping=True
            )
        }
        
        # Specialized models for different prediction tasks
        self.models = {
            'productivity': self._create_ensemble_model(),
            'value': self._create_ensemble_model(),
            'roi': self._create_ensemble_model(),
            'risk': self._create_ensemble_model()
        }
        
        # Multiple scalers for different model types
        self.scalers = {
            'standard': StandardScaler(),
            'robust': RobustScaler(),
            'minmax': MinMaxScaler()
        }
        
        # Feature selector
        self.feature_selector = SelectKBest(score_func=f_regression, k=10)
        
        # Model performance tracking
        self.model_performance = {}
        
        # Ensemble weights (will be learned dynamically)
        self.ensemble_weights = {
            'productivity': None,
            'value': None,
            'roi': None,
            'risk': None
        }
    
    def _create_ensemble_model(self):
        """Create an ensemble model combining multiple algorithms"""
        return EnsemblePredictor(self.base_models)
    
    def _engineer_features(self, baseline_data: dict, ai_initiative: dict) -> np.ndarray:
        """Advanced feature engineering for better predictions"""
        features = []
        
        # Baseline features
        features.extend([
            baseline_data['productivity'],
            baseline_data['revenue'],
            baseline_data['costs'],
            baseline_data['headcount'],
            baseline_data['satisfaction']
        ])
        
        # AI initiative features
        features.extend([
            ai_initiative['investment'],
            ai_initiative['automation_level'],
            ai_initiative['accuracy_improvement'],
            ai_initiative['speed_improvement'],
            ai_initiative['workforce_reduction'],
            ai_initiative['upskilling_required'],
            ai_initiative['new_roles_created']
        ])
        
        # Risk features
        risk_features = [
            ai_initiative.get('technical_risk', 0.3),
            ai_initiative.get('adoption_risk', 0.3),
            ai_initiative.get('integration_risk', 0.3),
            ai_initiative.get('regulatory_risk', 0.2),
            ai_initiative.get('competitive_risk', 0.2),
            ai_initiative.get('data_risk', 0.3)
        ]
        features.extend(risk_features)
        
        # Derived features (feature interactions)
        features.extend([
            baseline_data['revenue'] / max(baseline_data['costs'], 1),  # Current efficiency
            ai_initiative['investment'] / max(baseline_data['revenue'], 1),  # Investment ratio
            ai_initiative['automation_level'] * ai_initiative['accuracy_improvement'],  # AI impact
            baseline_data['productivity'] * baseline_data['satisfaction'],  # Current performance
            sum(risk_features) / len(risk_features),  # Average risk
            ai_initiative['automation_level'] / max(ai_initiative.get('workforce_reduction', 1), 0.1),  # Automation efficiency
        ])
        
        # Complexity encoding
        complexity_map = {'Low': 1, 'Medium': 2, 'High': 3}
        features.append(complexity_map.get(ai_initiative.get('complexity', 'Medium'), 2))
        
        # AI type encoding (one-hot style)
        ai_types = ['Automation', 'Augmentation', 'Analytics', 'Hybrid']
        ai_type = ai_initiative.get('ai_type', 'Hybrid')
        for ai_t in ai_types:
            features.append(1 if ai_type == ai_t else 0)
        
        # Timeline encoding
        timeline_map = {'3-6 months': 4.5, '6-12 months': 9, '12-18 months': 15, '18+ months': 24}
        features.append(timeline_map.get(ai_initiative.get('timeline', '6-12 months'), 9))
        
        return np.array(features).reshape(1, -1)
    
    def predict_impact(self, baseline_data: dict, ai_initiative: dict) -> dict:
        """
        Main prediction method that calculates impact across all metrics
        """
        try:
            # Extract key parameters
            baseline_productivity = baseline_data['productivity']
            baseline_revenue = baseline_data['revenue']
            baseline_costs = baseline_data['costs']
            investment = ai_initiative['investment']
            
            # Calculate productivity improvements
            productivity_gain = self._predict_productivity_gain(baseline_data, ai_initiative)
            
            # Calculate value generation
            value_generated = self._predict_value_generation(baseline_data, ai_initiative, productivity_gain)
            
            # Calculate ROI
            roi = self._predict_roi(value_generated, investment, baseline_costs, ai_initiative)
            
            # Calculate payback period
            monthly_value = value_generated / 12
            payback_period = self.metrics_calc.calculate_payback_period(investment, monthly_value)
            
            # Calculate workforce impact
            workforce_impact = self._calculate_workforce_impact(baseline_data, ai_initiative)
            
            # Apply risk adjustments
            risk_factors = {
                'technical_risk': ai_initiative.get('technical_risk', 30),
                'adoption_risk': ai_initiative.get('adoption_risk', 30),
                'integration_risk': ai_initiative.get('integration_risk', 30)
            }
            
            risk_adjusted_roi = self.metrics_calc.apply_risk_adjustment(roi, risk_factors)
            risk_adjusted_value = self.metrics_calc.apply_risk_adjustment(value_generated, risk_factors)
            
            # Calculate confidence intervals
            confidence_interval = self._calculate_confidence_intervals(
                productivity_gain, value_generated, roi, risk_factors
            )
            
            return {
                'productivity_gain': productivity_gain,
                'value_generated': risk_adjusted_value,
                'roi': risk_adjusted_roi,
                'payback_period': payback_period,
                'workforce_impact': workforce_impact,
                'risk_adjusted_roi': risk_adjusted_roi,
                'confidence_interval': confidence_interval,
                'monthly_value': monthly_value,
                'annual_savings': self._calculate_annual_savings(baseline_data, ai_initiative)
            }
            
        except Exception as e:
            # Return default values in case of error
            return {
                'productivity_gain': 0.0,
                'value_generated': 0.0,
                'roi': 0.0,
                'payback_period': float('inf'),
                'workforce_impact': {'reduction': 0, 'upskilling': 0, 'new_roles': 0},
                'risk_adjusted_roi': 0.0,
                'confidence_interval': {'lower': 0, 'upper': 0},
                'monthly_value': 0.0,
                'annual_savings': 0.0,
                'error': str(e)
            }
    
    def _predict_productivity_gain(self, baseline_data: dict, ai_initiative: dict) -> float:
        """Predict productivity gain based on AI implementation"""
        
        # Base productivity calculation using improvement factors
        automation_impact = ai_initiative.get('automation_level', 0) * 0.6
        accuracy_impact = ai_initiative.get('accuracy_improvement', 0) * 0.3
        speed_impact = ai_initiative.get('speed_improvement', 0) * 0.4
        
        # Weight by AI type
        ai_type_multipliers = {
            'Automation': 1.2,
            'Augmentation': 0.9,
            'Analytics': 0.7,
            'Hybrid': 1.1
        }
        
        type_multiplier = ai_type_multipliers.get(ai_initiative.get('type', 'Hybrid'), 1.0)
        
        # Complexity adjustment
        complexity_adjustments = {
            'Low': 1.1,
            'Medium': 1.0,
            'High': 0.85
        }
        
        complexity_adj = complexity_adjustments.get(ai_initiative.get('complexity', 'Medium'), 1.0)
        
        # Calculate base productivity gain
        base_gain = (automation_impact + accuracy_impact + speed_impact) / 3
        adjusted_gain = base_gain * type_multiplier * complexity_adj
        
        # Apply diminishing returns for high baseline productivity
        baseline_factor = 1 - (baseline_data['productivity'] / 100) * 0.3
        final_gain = adjusted_gain * baseline_factor
        
        return min(final_gain, 60.0)  # Cap at 60% gain
    
    def _predict_value_generation(self, baseline_data: dict, ai_initiative: dict, productivity_gain: float) -> float:
        """Predict monetary value generation"""
        
        baseline_revenue = baseline_data['revenue']
        
        # Primary value from productivity improvements
        productivity_value = baseline_revenue * (productivity_gain / 100)
        
        # Additional value streams
        cost_reduction = self._calculate_cost_reduction(baseline_data, ai_initiative)
        revenue_enhancement = self._calculate_revenue_enhancement(baseline_data, ai_initiative)
        
        # Scale by implementation timeline
        timeline_months = self._parse_timeline(ai_initiative.get('timeline', '12 months'))
        timeline_factor = max(0.7, 1 - (timeline_months - 6) / 24)  # Longer implementations have reduced first-year impact
        
        total_value = (productivity_value + cost_reduction + revenue_enhancement) * timeline_factor
        
        return max(total_value, 0)
    
    def _predict_roi(self, value_generated: float, investment: float, baseline_costs: float, ai_initiative: dict) -> float:
        """Predict return on investment"""
        
        # Calculate ongoing costs (maintenance, training, etc.)
        ongoing_costs_factor = {
            'Low': 0.05,    # 5% of investment annually
            'Medium': 0.08,  # 8% of investment annually
            'High': 0.12     # 12% of investment annually
        }
        
        complexity = ai_initiative.get('complexity', 'Medium')
        annual_ongoing_costs = investment * ongoing_costs_factor.get(complexity, 0.08)
        
        # Calculate net value (first year)
        net_value = value_generated - annual_ongoing_costs
        
        if investment == 0:
            return 0
        
        roi = (net_value / investment) * 100
        
        return roi
    
    def _calculate_workforce_impact(self, baseline_data: dict, ai_initiative: dict) -> dict:
        """Calculate detailed workforce impact"""
        
        current_headcount = baseline_data['headcount']
        
        # Direct workforce changes
        workforce_reduction = ai_initiative.get('workforce_reduction', 0)
        new_roles_created = ai_initiative.get('new_roles_created', 0)
        upskilling_required = ai_initiative.get('upskilling_required', 0)
        
        # Calculate absolute numbers
        reduced_positions = int(current_headcount * workforce_reduction / 100)
        new_positions = int(current_headcount * new_roles_created / 100)
        upskilling_count = int(current_headcount * upskilling_required / 100)
        
        # Net headcount change
        net_headcount_change = new_positions - reduced_positions
        
        return {
            'reduction': reduced_positions,
            'new_roles': new_positions,
            'upskilling': upskilling_count,
            'net_change': net_headcount_change,
            'percentage_change': (net_headcount_change / current_headcount) * 100
        }
    
    def _calculate_cost_reduction(self, baseline_data: dict, ai_initiative: dict) -> float:
        """Calculate cost reduction from AI implementation"""
        
        baseline_costs = baseline_data['costs']
        automation_level = ai_initiative.get('automation_level', 0)
        
        # Cost reduction primarily from automation
        direct_cost_reduction = baseline_costs * (automation_level / 100) * 0.3  # 30% of automated costs saved
        
        # Additional savings from accuracy improvements (reduced errors/rework)
        accuracy_improvement = ai_initiative.get('accuracy_improvement', 0)
        error_cost_reduction = baseline_costs * (accuracy_improvement / 100) * 0.1  # 10% of costs from errors
        
        total_cost_reduction = direct_cost_reduction + error_cost_reduction
        
        return total_cost_reduction
    
    def _calculate_revenue_enhancement(self, baseline_data: dict, ai_initiative: dict) -> float:
        """Calculate revenue enhancement from AI implementation"""
        
        baseline_revenue = baseline_data['revenue']
        
        # Revenue enhancement from speed improvements (faster delivery, more capacity)
        speed_improvement = ai_initiative.get('speed_improvement', 0)
        capacity_revenue = baseline_revenue * (speed_improvement / 100) * 0.2  # 20% of speed improvement translates to revenue
        
        # Revenue enhancement from accuracy improvements (better quality, customer satisfaction)
        accuracy_improvement = ai_initiative.get('accuracy_improvement', 0)
        quality_revenue = baseline_revenue * (accuracy_improvement / 100) * 0.15  # 15% of accuracy improvement
        
        total_revenue_enhancement = capacity_revenue + quality_revenue
        
        return total_revenue_enhancement
    
    def _calculate_annual_savings(self, baseline_data: dict, ai_initiative: dict) -> float:
        """Calculate total annual savings"""
        
        cost_reduction = self._calculate_cost_reduction(baseline_data, ai_initiative)
        
        # Labor cost savings from workforce reduction
        workforce_reduction = ai_initiative.get('workforce_reduction', 0)
        avg_salary = baseline_data['costs'] / baseline_data['headcount'] * 0.7  # Assume 70% of costs are labor
        labor_savings = baseline_data['headcount'] * (workforce_reduction / 100) * avg_salary
        
        total_savings = cost_reduction + labor_savings
        
        return total_savings
    
    def _calculate_confidence_intervals(self, productivity_gain: float, value_generated: float, 
                                     roi: float, risk_factors: dict) -> dict:
        """Calculate confidence intervals for predictions"""
        
        # Base uncertainty factors
        base_uncertainty = 0.2  # 20% base uncertainty
        
        # Adjust uncertainty based on risk factors
        avg_risk = (risk_factors['technical_risk'] + risk_factors['adoption_risk'] + 
                   risk_factors['integration_risk']) / 3
        risk_uncertainty = (avg_risk / 100) * 0.3  # Additional 30% uncertainty for high risk
        
        total_uncertainty = base_uncertainty + risk_uncertainty
        
        return {
            'productivity_gain': {
                'lower': productivity_gain * (1 - total_uncertainty),
                'upper': productivity_gain * (1 + total_uncertainty)
            },
            'value_generated': {
                'lower': value_generated * (1 - total_uncertainty),
                'upper': value_generated * (1 + total_uncertainty)
            },
            'roi': {
                'lower': roi * (1 - total_uncertainty),
                'upper': roi * (1 + total_uncertainty)
            }
        }
    
    def _parse_timeline(self, timeline_str: str) -> int:
        """Parse timeline string to months"""
        timeline_map = {
            '3 months': 3,
            '6 months': 6,
            '12 months': 12,
            '18 months': 18,
            '24 months': 24
        }
        return timeline_map.get(timeline_str, 12)
    
    def generate_temporal_projection(self, baseline_data: dict, ai_initiative: dict, 
                                   predictions: dict, months: int) -> dict:
        """Generate month-by-month projections"""
        
        # Get implementation timeline
        impl_months = self._parse_timeline(ai_initiative.get('timeline', '12 months'))
        
        # Generate adoption curve
        adoption_curve = self.ts_generator.generate_adoption_curve(impl_months, "s-curve")
        
        # Extend adoption curve to full timeline
        if months > impl_months:
            full_adoption = [1.0] * (months - impl_months)
            adoption_curve.extend(full_adoption)
        else:
            adoption_curve = adoption_curve[:months]
        
        # Generate monthly projections
        monthly_data = {
            'month': list(range(1, months + 1)),
            'adoption_rate': adoption_curve,
            'monthly_value': [],
            'cumulative_value': [],
            'monthly_roi': [],
            'cumulative_roi': [],
            'productivity_level': [],
            'cost_savings': []
        }
        
        base_monthly_value = predictions['value_generated'] / 12
        cumulative_value = 0
        investment = ai_initiative['investment']
        
        for i, adoption in enumerate(adoption_curve):
            # Calculate monthly value with adoption rate
            monthly_value = base_monthly_value * adoption
            cumulative_value += monthly_value
            
            # Calculate ROI
            if investment > 0:
                monthly_roi = (monthly_value / investment) * 100
                cumulative_roi = ((cumulative_value - investment) / investment) * 100
            else:
                monthly_roi = 0
                cumulative_roi = 0
            
            # Calculate productivity level
            base_productivity = baseline_data['productivity']
            max_gain = predictions['productivity_gain']
            current_productivity = base_productivity + (max_gain * adoption)
            
            # Calculate cost savings
            monthly_savings = predictions.get('annual_savings', 0) / 12 * adoption
            
            monthly_data['monthly_value'].append(monthly_value)
            monthly_data['cumulative_value'].append(cumulative_value)
            monthly_data['monthly_roi'].append(monthly_roi)
            monthly_data['cumulative_roi'].append(cumulative_roi)
            monthly_data['productivity_level'].append(current_productivity)
            monthly_data['cost_savings'].append(monthly_savings)
        
        return monthly_data
    
    def compare_scenarios(self, baseline_scenario: dict, ai_scenarios: list) -> dict:
        """Compare multiple AI implementation scenarios"""
        
        comparison_results = {
            'baseline': baseline_scenario,
            'scenarios': [],
            'best_scenario': None,
            'comparison_metrics': {}
        }
        
        best_roi = -float('inf')
        best_scenario_idx = -1
        
        for i, scenario in enumerate(ai_scenarios):
            scenario_result = self.predict_impact(baseline_scenario, scenario)
            scenario_result['scenario_name'] = f"Scenario {i+1}"
            scenario_result['configuration'] = scenario
            
            comparison_results['scenarios'].append(scenario_result)
            
            # Track best scenario by risk-adjusted ROI
            if scenario_result['risk_adjusted_roi'] > best_roi:
                best_roi = scenario_result['risk_adjusted_roi']
                best_scenario_idx = i
        
        if best_scenario_idx >= 0:
            comparison_results['best_scenario'] = comparison_results['scenarios'][best_scenario_idx]
        
        # Calculate comparison metrics
        comparison_results['comparison_metrics'] = self._calculate_scenario_metrics(
            comparison_results['scenarios']
        )
        
        return comparison_results
    
    def _calculate_scenario_metrics(self, scenarios: list) -> dict:
        """Calculate metrics for scenario comparison"""
        
        if not scenarios:
            return {}
        
        rois = [s['roi'] for s in scenarios]
        values = [s['value_generated'] for s in scenarios]
        paybacks = [s['payback_period'] for s in scenarios if s['payback_period'] != float('inf')]
        
        metrics = {
            'avg_roi': np.mean(rois),
            'max_roi': np.max(rois),
            'min_roi': np.min(rois),
            'total_value': np.sum(values),
            'avg_value': np.mean(values)
        }
        
        if paybacks:
            metrics['avg_payback'] = np.mean(paybacks)
            metrics['min_payback'] = np.min(paybacks)
        
        return metrics
    
    def _generate_synthetic_training_data(self, baseline_data: dict, ai_initiative: dict) -> list:
        """Generate realistic training scenarios for model fitting"""
        training_scenarios = []
        
        # Create variations around the current scenario
        for i in range(20):
            # Vary key parameters realistically
            variation_data = baseline_data.copy()
            variation_ai = ai_initiative.copy()
            
            # Add realistic noise to parameters
            variation_data['productivity'] = max(10, baseline_data['productivity'] + np.random.normal(0, 10))
            variation_data['revenue'] = max(100000, baseline_data['revenue'] * (1 + np.random.normal(0, 0.2)))
            variation_ai['automation_level'] = max(0, min(100, ai_initiative['automation_level'] + np.random.normal(0, 15)))
            variation_ai['investment'] = max(10000, ai_initiative['investment'] * (1 + np.random.normal(0, 0.3)))
            
            features = self._engineer_features(variation_data, variation_ai)
            
            # Calculate expected outcomes using domain knowledge
            productivity_target = self._domain_knowledge_productivity(variation_data, variation_ai)
            value_target = self._domain_knowledge_value(variation_data, variation_ai, productivity_target)
            roi_target = self._domain_knowledge_roi(value_target, variation_ai['investment'], variation_data['costs'])
            
            training_scenarios.append({
                'features': features,
                'productivity': productivity_target,
                'value': value_target,
                'roi': roi_target
            })
        
        return training_scenarios
    
    def _fit_models(self, training_data: list, current_features: np.ndarray):
        """Fit ensemble models using training data"""
        if len(training_data) < 5:
            return
        
        # Prepare training matrices
        X = np.vstack([scenario['features'] for scenario in training_data])
        
        # Fit models for each target
        for target in ['productivity', 'value', 'roi']:
            y = np.array([scenario[target] for scenario in training_data])
            try:
                self.models[target].fit(X, y)
            except Exception as e:
                print(f"Model fitting error for {target}: {e}")
    
    def _predict_with_ensemble(self, target: str, features: np.ndarray, baseline_data: dict, ai_initiative: dict) -> float:
        """Make prediction using ensemble model with fallback"""
        try:
            prediction = self.models[target].predict(features)
            if isinstance(prediction, (list, np.ndarray)):
                prediction = prediction[0] if len(prediction) > 0 else 0
            
            # Apply domain knowledge bounds
            if target == 'productivity':
                return max(0, min(100, prediction))
            elif target == 'value':
                return max(0, prediction)
            elif target == 'roi':
                return max(-50, min(500, prediction))
            
            return prediction
        except:
            # Fallback to enhanced domain knowledge
            if target == 'productivity':
                return self._domain_knowledge_productivity(baseline_data, ai_initiative)
            elif target == 'value':
                productivity = self._domain_knowledge_productivity(baseline_data, ai_initiative)
                return self._domain_knowledge_value(baseline_data, ai_initiative, productivity)
            elif target == 'roi':
                productivity = self._domain_knowledge_productivity(baseline_data, ai_initiative)
                value = self._domain_knowledge_value(baseline_data, ai_initiative, productivity)
                return self._domain_knowledge_roi(value, ai_initiative['investment'], baseline_data['costs'])
            
            return 0.0  # Default fallback
    
    def _domain_knowledge_productivity(self, baseline_data: dict, ai_initiative: dict) -> float:
        """Calculate productivity gain using enhanced domain knowledge"""
        automation_impact = ai_initiative['automation_level'] * 0.4
        accuracy_impact = ai_initiative['accuracy_improvement'] * 0.3
        speed_impact = ai_initiative['speed_improvement'] * 0.2
        
        complexity_penalty = {'Low': 0.9, 'Medium': 0.8, 'High': 0.6}.get(ai_initiative.get('complexity', 'Medium'), 0.8)
        baseline_factor = (baseline_data['productivity'] / 100) * 0.5
        
        return (automation_impact + accuracy_impact + speed_impact) * complexity_penalty + baseline_factor
    
    def _domain_knowledge_value(self, baseline_data: dict, ai_initiative: dict, productivity_gain: float) -> float:
        """Calculate value generation using enhanced domain knowledge"""
        revenue_enhancement = baseline_data['revenue'] * (productivity_gain / 100) * 0.6
        cost_reduction = baseline_data['costs'] * (ai_initiative['automation_level'] / 100) * 0.3
        efficiency_gains = baseline_data['revenue'] * 0.05 * (productivity_gain / 20)
        
        return revenue_enhancement + cost_reduction + efficiency_gains
    
    def _domain_knowledge_roi(self, value_generated: float, investment: float, baseline_costs: float) -> float:
        """Calculate ROI using enhanced domain knowledge"""
        annual_return = value_generated - (investment * 0.15)  # 15% annual capital cost
        return (annual_return / investment) * 100 if investment > 0 else 0
    
    def get_prediction_confidence(self, baseline_data: dict, ai_initiative: dict) -> dict:
        """Get confidence metrics for predictions"""
        features = self._engineer_features(baseline_data, ai_initiative)
        
        # Calculate various confidence factors
        data_quality = self._assess_data_quality(baseline_data, ai_initiative)
        feature_reliability = self._assess_feature_reliability(features)
        model_stability = self._assess_model_stability()
        
        overall_confidence = (data_quality + feature_reliability + model_stability) / 3
        
        return {
            'overall_confidence': overall_confidence,
            'data_quality': data_quality,
            'feature_reliability': feature_reliability,
            'model_stability': model_stability,
            'confidence_level': 'High' if overall_confidence > 0.8 else 'Medium' if overall_confidence > 0.6 else 'Low'
        }
    
    def _assess_data_quality(self, baseline_data: dict, ai_initiative: dict) -> float:
        """Assess quality of input data"""
        quality_score = 0.8  # Base score
        
        # Check for reasonable values
        if baseline_data['productivity'] < 10 or baseline_data['productivity'] > 95:
            quality_score -= 0.1
        if baseline_data['revenue'] < 100000:
            quality_score -= 0.1
        if ai_initiative['investment'] < 10000:
            quality_score -= 0.1
            
        return max(0.3, quality_score)
    
    def _assess_feature_reliability(self, features: np.ndarray) -> float:
        """Assess reliability of engineered features"""
        if features.shape[1] == 0:
            return 0.5
        
        # Check for extreme values
        extreme_values = np.sum(np.abs(features) > 3) / features.size
        reliability = 1.0 - min(0.5, extreme_values * 2)
        
        return max(0.4, reliability)
    
    def _assess_model_stability(self) -> float:
        """Assess stability of model ensemble"""
        # For now, return a fixed score - could be enhanced with actual model validation
        return 0.75
