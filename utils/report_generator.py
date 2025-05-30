import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import io
import base64

class ReportGenerator:
    """Generate executive reports and summaries"""
    
    def __init__(self):
        self.report_date = datetime.now()
    
    def generate_executive_summary(self, baseline_data: Dict, ai_initiatives: Dict, 
                                 predictions: Dict) -> Dict:
        """Generate executive summary data"""
        
        if not predictions:
            return {
                'total_investment': 0,
                'average_roi': 0,
                'average_payback': 0,
                'total_value': 0,
                'average_productivity': 0,
                'functions_count': 0,
                'high_priority_functions': [],
                'total_headcount_impact': 0
            }
        
        # Calculate aggregate metrics with data validation
        total_investment = sum(ai_initiatives[f]['investment'] for f in predictions.keys() 
                             if f in ai_initiatives and 'investment' in ai_initiatives[f])
        total_value = sum(predictions[f]['value_generated'] for f in predictions.keys()
                         if 'value_generated' in predictions[f])
        
        roi_values = [predictions[f]['roi'] for f in predictions.keys() 
                     if 'roi' in predictions[f] and predictions[f]['roi'] is not None]
        average_roi = np.mean(roi_values) if roi_values else 0
        
        payback_values = [predictions[f]['payback_period'] for f in predictions.keys() 
                         if 'payback_period' in predictions[f] and 
                         predictions[f]['payback_period'] != float('inf') and
                         predictions[f]['payback_period'] is not None]
        average_payback = np.mean(payback_values) if payback_values else 0
        
        productivity_values = [predictions[f]['productivity_gain'] for f in predictions.keys()]
        average_productivity = np.mean(productivity_values)
        
        # Calculate total headcount impact
        total_headcount_impact = 0
        for func in predictions.keys():
            if func in baseline_data and func in ai_initiatives:
                current_headcount = baseline_data[func]['headcount']
                workforce_reduction = ai_initiatives[func].get('workforce_reduction', 0)
                headcount_reduction = current_headcount * (workforce_reduction / 100)
                total_headcount_impact += headcount_reduction
        
        # Identify high priority functions (high ROI, low risk)
        high_priority_functions = []
        for func in predictions.keys():
            if func in ai_initiatives and 'roi' in predictions[func]:
                roi = predictions[func]['roi']
                risk_score = self._calculate_risk_score(ai_initiatives[func])
                
                if roi > average_roi and risk_score < 50:  # Above average ROI, below average risk
                    high_priority_functions.append(func)
        
        return {
            'total_investment': total_investment,
            'average_roi': average_roi,
            'average_payback': average_payback,
            'total_value': total_value,
            'average_productivity': average_productivity,
            'functions_count': len(predictions),
            'high_priority_functions': high_priority_functions,
            'total_headcount_impact': total_headcount_impact,
            'net_value': total_value - total_investment,
            'portfolio_roi': ((total_value - total_investment) / total_investment * 100) if total_investment > 0 else 0
        }
    
    def generate_risk_assessment(self, ai_initiatives: Dict) -> Dict:
        """Generate comprehensive risk assessment"""
        
        risk_categories = {
            'high_risk': [],
            'medium_risk': [],
            'low_risk': []
        }
        
        for func, initiative in ai_initiatives.items():
            risk_score = self._calculate_risk_score(initiative)
            
            if risk_score >= 70:
                risk_categories['high_risk'].append(func)
            elif risk_score >= 40:
                risk_categories['medium_risk'].append(func)
            else:
                risk_categories['low_risk'].append(func)
        
        return risk_categories
    
    def generate_recommendations(self, predictions: Dict, ai_initiatives: Dict) -> List[Dict]:
        """Generate strategic recommendations"""
        
        recommendations = []
        
        if not predictions:
            return [{
                'title': 'Configure AI Initiatives',
                'description': 'Start by configuring AI initiatives for your enterprise functions to receive personalized recommendations.'
            }]
        
        # Analyze ROI distribution
        roi_values = [predictions[f]['roi'] for f in predictions.keys()]
        avg_roi = np.mean(roi_values)
        max_roi = np.max(roi_values)
        
        # Recommendation 1: Prioritize high-ROI functions
        high_roi_functions = [f for f in predictions.keys() if predictions[f]['roi'] > avg_roi]
        if high_roi_functions:
            recommendations.append({
                'title': 'Prioritize High-ROI Functions',
                'description': f"Focus immediate implementation on {', '.join(high_roi_functions[:3])} as they show above-average ROI potential."
            })
        
        # Recommendation 2: Address high-risk functions
        high_risk_functions = []
        for func in ai_initiatives.keys():
            if self._calculate_risk_score(ai_initiatives[func]) >= 70:
                high_risk_functions.append(func)
        
        if high_risk_functions:
            recommendations.append({
                'title': 'Develop Risk Mitigation Strategies',
                'description': f"Create detailed risk mitigation plans for {', '.join(high_risk_functions)} before implementation."
            })
        
        # Recommendation 3: Optimize investment allocation
        total_investment = sum(ai_initiatives[f]['investment'] for f in predictions.keys())
        if total_investment > 1000000:  # Large investment
            recommendations.append({
                'title': 'Consider Phased Implementation',
                'description': 'Given the significant investment required, consider implementing AI initiatives in phases to manage risk and cash flow.'
            })
        
        # Recommendation 4: Workforce planning
        total_workforce_impact = sum(
            ai_initiatives[f].get('workforce_reduction', 0) for f in ai_initiatives.keys()
        )
        if total_workforce_impact > 100:  # Significant workforce impact
            recommendations.append({
                'title': 'Develop Comprehensive Change Management',
                'description': 'The projected workforce changes require a robust change management strategy including retraining and communication plans.'
            })
        
        # Recommendation 5: Quick wins
        quick_win_functions = []
        for func in predictions.keys():
            payback = predictions[func]['payback_period']
            if payback < 12 and payback != float('inf'):  # Less than 1 year payback
                quick_win_functions.append(func)
        
        if quick_win_functions:
            recommendations.append({
                'title': 'Pursue Quick Wins',
                'description': f"Start with {', '.join(quick_win_functions)} for rapid value realization and momentum building."
            })
        
        return recommendations
    
    def prepare_export_data(self, baseline_data: Dict, ai_initiatives: Dict, 
                          predictions: Dict) -> pd.DataFrame:
        """Prepare data for CSV export"""
        
        export_rows = []
        
        for func in predictions.keys():
            if func in baseline_data and func in ai_initiatives:
                baseline = baseline_data[func]
                initiative = ai_initiatives[func]
                prediction = predictions[func]
                
                row = {
                    'Function': func,
                    'Current_Productivity': baseline['productivity'],
                    'Current_Headcount': baseline['headcount'],
                    'Current_Revenue': baseline['revenue'],
                    'Current_Costs': baseline['costs'],
                    'AI_Type': initiative['type'],
                    'Implementation_Complexity': initiative['complexity'],
                    'Investment_Amount': initiative['investment'],
                    'Implementation_Timeline': initiative['timeline'],
                    'Predicted_Productivity_Gain': prediction['productivity_gain'],
                    'Predicted_Value_Generated': prediction['value_generated'],
                    'Predicted_ROI': prediction['roi'],
                    'Payback_Period_Months': prediction['payback_period'],
                    'Technical_Risk': initiative.get('technical_risk', 0),
                    'Adoption_Risk': initiative.get('adoption_risk', 0),
                    'Integration_Risk': initiative.get('integration_risk', 0),
                    'Automation_Level': initiative.get('automation_level', 0),
                    'Workforce_Reduction_Percent': initiative.get('workforce_reduction', 0),
                    'Risk_Adjusted_ROI': prediction.get('risk_adjusted_roi', prediction['roi'])
                }
                
                export_rows.append(row)
        
        return pd.DataFrame(export_rows)
    
    def generate_text_report(self, summary_data: Dict, recommendations: List[Dict]) -> str:
        """Generate comprehensive text report"""
        
        report = f"""
AI IMPLEMENTATION IMPACT ANALYSIS
Executive Summary Report
Generated: {self.report_date.strftime('%B %d, %Y')}

========================================
EXECUTIVE SUMMARY
========================================

Portfolio Overview:
• Total Functions Analyzed: {summary_data['functions_count']}
• Total Investment Required: ${summary_data['total_investment']:,.0f}
• Expected Total Value Generation: ${summary_data['total_value']:,.0f}
• Net Value Creation: ${summary_data.get('net_value', 0):,.0f}
• Portfolio ROI: {summary_data.get('portfolio_roi', 0):.1f}%

Key Performance Indicators:
• Average ROI: {summary_data['average_roi']:.1f}%
• Average Payback Period: {summary_data['average_payback']:.1f} months
• Average Productivity Gain: {summary_data['average_productivity']:.1f}%
• Projected Headcount Impact: {summary_data['total_headcount_impact']:.0f} positions

High Priority Functions:
{self._format_function_list(summary_data['high_priority_functions'])}

========================================
STRATEGIC RECOMMENDATIONS
========================================
"""
        
        for i, rec in enumerate(recommendations, 1):
            report += f"""
{i}. {rec['title']}
   {rec['description']}
"""
        
        report += f"""

========================================
IMPLEMENTATION CONSIDERATIONS
========================================

Risk Management:
• Establish clear governance structure for AI initiatives
• Develop comprehensive change management strategy
• Create regular monitoring and evaluation processes
• Plan for workforce transition and upskilling programs

Success Factors:
• Executive sponsorship and clear communication
• Adequate investment in training and support
• Phased implementation approach
• Regular assessment and course correction

Timeline Considerations:
• Allow sufficient time for user adoption
• Plan for integration challenges
• Budget for ongoing maintenance and improvements
• Consider external factors and market conditions

========================================
NEXT STEPS
========================================

1. Review and validate assumptions with functional leaders
2. Develop detailed implementation roadmaps for priority functions
3. Secure necessary budget approvals and resources
4. Establish project governance and success metrics
5. Begin with pilot implementations for quick wins

Report prepared by AI Impact Dashboard
For questions or clarifications, please review the interactive dashboard.
"""
        
        return report
    
    def generate_presentation_summary(self, summary_data: Dict) -> Dict:
        """Generate data optimized for presentation slides"""
        
        presentation_data = {
            'key_metrics': {
                'total_investment': f"${summary_data['total_investment']:,.0f}",
                'total_value': f"${summary_data['total_value']:,.0f}",
                'portfolio_roi': f"{summary_data.get('portfolio_roi', 0):.1f}%",
                'average_payback': f"{summary_data['average_payback']:.1f} months"
            },
            'highlights': [
                f"Portfolio spans {summary_data['functions_count']} enterprise functions",
                f"Average productivity gain of {summary_data['average_productivity']:.1f}%",
                f"Net value creation of ${summary_data.get('net_value', 0):,.0f}",
                f"{len(summary_data['high_priority_functions'])} high-priority opportunities identified"
            ],
            'investment_summary': {
                'total': summary_data['total_investment'],
                'expected_return': summary_data['total_value'],
                'net_benefit': summary_data.get('net_value', 0)
            }
        }
        
        return presentation_data
    
    def _calculate_risk_score(self, initiative: Dict) -> float:
        """Calculate overall risk score for an initiative"""
        technical_risk = initiative.get('technical_risk', 30)
        adoption_risk = initiative.get('adoption_risk', 30)
        integration_risk = initiative.get('integration_risk', 30)
        
        # Weight the risks
        weighted_risk = (technical_risk * 0.4 + adoption_risk * 0.4 + integration_risk * 0.2)
        
        # Adjust for complexity
        complexity_multiplier = {
            'Low': 0.8,
            'Medium': 1.0,
            'High': 1.3
        }
        
        complexity = initiative.get('complexity', 'Medium')
        final_risk = weighted_risk * complexity_multiplier.get(complexity, 1.0)
        
        return min(final_risk, 100)  # Cap at 100
    
    def _format_function_list(self, functions: List[str]) -> str:
        """Format function list for text report"""
        if not functions:
            return "• None identified"
        
        return '\n'.join([f"• {func}" for func in functions])
    
    def generate_financial_projection(self, predictions: Dict, ai_initiatives: Dict, 
                                    years: int = 3) -> Dict:
        """Generate multi-year financial projections"""
        
        projections = {
            'years': list(range(1, years + 1)),
            'annual_value': [],
            'annual_costs': [],
            'cumulative_value': [],
            'cumulative_roi': []
        }
        
        total_investment = sum(ai_initiatives[f]['investment'] for f in predictions.keys())
        annual_value_base = sum(predictions[f]['value_generated'] for f in predictions.keys())
        
        cumulative_value = 0
        
        for year in range(1, years + 1):
            # Apply growth assumptions (conservative 5% annual improvement)
            annual_value = annual_value_base * (1 + (year - 1) * 0.05)
            
            # Calculate annual maintenance costs (8% of investment)
            annual_costs = total_investment * 0.08
            
            # Net annual value
            net_annual_value = annual_value - annual_costs
            cumulative_value += net_annual_value
            
            # Calculate cumulative ROI
            cumulative_roi = (cumulative_value / total_investment) * 100 if total_investment > 0 else 0
            
            projections['annual_value'].append(annual_value)
            projections['annual_costs'].append(annual_costs)
            projections['cumulative_value'].append(cumulative_value)
            projections['cumulative_roi'].append(cumulative_roi)
        
        return projections
