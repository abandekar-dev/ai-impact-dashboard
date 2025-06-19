import streamlit as st
from typing import Dict, List, Optional
import uuid
from datetime import datetime

class CategoryManager:
    """Manages categories and AI initiatives within enterprise functions"""
    
    def __init__(self):
        self.default_categories = {
            # Technology Industry
            "IT & Technology": [
                "Infrastructure Planning and Management",
                "Cloud Services and Architecture",
                "Network Administration and Security",
                "System Administration and Monitoring",
                "Enterprise Application Management",
                "IT Service Management and Support",
                "Technology Strategy and Governance",
                "Vendor and License Management",
                "IT Asset and Configuration Management"
            ],
            "Data & Analytics": [
                "Data Architecture and Engineering",
                "Business Intelligence and Reporting",
                "Advanced Analytics and Machine Learning",
                "Data Governance and Quality Management",
                "Data Integration and ETL Processes",
                "Real-time Analytics and Streaming",
                "Data Visualization and Dashboards",
                "Data Privacy and Security",
                "Analytics Strategy and ROI"
            ],
            "Product Development": [
                "Product Strategy and Roadmap Planning",
                "Software Engineering and Development",
                "Quality Assurance and Testing",
                "User Experience and Interface Design",
                "Product Management and Lifecycle",
                "Release Management and Deployment",
                "Technical Documentation and Standards",
                "Product Performance and Analytics",
                "Innovation and Research"
            ],
            "Customer Support": [
                "Technical Support and Troubleshooting",
                "Customer Success and Onboarding",
                "Knowledge Base and Documentation",
                "Escalation and Case Management",
                "Self-Service Portal and Automation",
                "Support Analytics and Performance",
                "Training and Certification Programs",
                "Community and User Engagement",
                "Support Process Optimization"
            ],
            
            # Retail Industry
            "Store Operations": [
                "Store Staffing and Scheduling",
                "Inventory Management",
                "Merchandising Execution",
                "Point of Sale Operations",
                "Customer Experience and Service",
                "Loss Prevention and Security",
                "Compliance and Store Audits",
                "Store Communications",
                "Facilities and Maintenance"
            ],
            "E-commerce": [
                "Website and Mobile Platform Operations",
                "Digital Product Catalog Management",
                "Online Order Processing and Fulfillment",
                "Customer Account Management",
                "Payment Gateway and Security",
                "Digital Marketing and SEO",
                "Customer Reviews and Ratings",
                "Returns and Refund Processing",
                "Site Performance and Analytics"
            ],
            "Supply Chain & Logistics": [
                "Demand Planning and Forecasting",
                "Vendor and Supplier Management",
                "Warehouse Operations and Management",
                "Transportation and Distribution",
                "Inventory Optimization",
                "Last-Mile Delivery Solutions",
                "Cross-Docking and Consolidation",
                "Supply Chain Visibility and Tracking",
                "Logistics Cost Management"
            ],
            "Merchandising": [
                "Category Planning and Management",
                "Product Assortment Planning",
                "Pricing Strategy and Optimization",
                "Seasonal and Promotional Planning",
                "Visual Merchandising and Display",
                "Space Planning and Allocation",
                "Product Performance Analysis",
                "Vendor Negotiations and Relations",
                "Private Label Development"
            ],
            "Customer Experience": [
                "Customer Journey Design and Optimization",
                "Loyalty Program Management",
                "Customer Feedback and Voice Programs",
                "Personalization and Recommendation Engines",
                "Omnichannel Experience Coordination",
                "Customer Service Excellence",
                "Digital Experience Optimization",
                "Customer Retention Strategies",
                "Experience Analytics and Insights"
            ],
            "Marketing & Promotions": [
                "Campaign Planning and Execution",
                "Digital and Social Media Marketing",
                "Brand Management and Positioning",
                "Promotional Strategy and Tactics",
                "Customer Segmentation and Targeting",
                "Marketing Analytics and ROI",
                "Content Creation and Management",
                "Influencer and Partnership Marketing",
                "Local and Regional Marketing"
            ],
            
            # Manufacturing Industry
            "Production & Assembly": [
                "Production Planning and Scheduling",
                "Assembly Line Management and Operations",
                "Workflow Design and Optimization",
                "Material Requirements Planning (MRP)",
                "Production Quality Monitoring",
                "Equipment Operation and Control",
                "Capacity Planning and Utilization",
                "Work Order Management",
                "Production Cost Control"
            ],
            "Quality Control": [
                "Inspection Planning and Execution",
                "Statistical Process Control",
                "Quality Testing and Validation",
                "Defect Detection and Analysis",
                "Corrective and Preventive Actions",
                "Quality Documentation and Records",
                "Supplier Quality Management",
                "Customer Quality Requirements",
                "Continuous Quality Improvement"
            ],
            "Plant Operations": [
                "Facility and Equipment Management",
                "Utilities and Energy Management",
                "Environmental Health and Safety",
                "Operational Performance Monitoring",
                "Plant Maintenance Coordination",
                "Production Support Services",
                "Resource Allocation and Planning",
                "Operational Cost Management",
                "Plant Communication and Coordination"
            ],
            "R&D & Engineering": [
                "Product Design and Development",
                "Process Engineering and Optimization",
                "Materials Research and Selection",
                "Prototype Development and Testing",
                "Design for Manufacturing (DFM)",
                "Engineering Documentation and Standards",
                "Innovation and Technology Development",
                "Product Testing and Validation",
                "Engineering Change Management"
            ],
            "Maintenance & Facilities": [
                "Preventive Maintenance Planning",
                "Equipment Repair and Troubleshooting",
                "Facility Infrastructure Management",
                "Asset Lifecycle Management",
                "Maintenance Scheduling and Coordination",
                "Spare Parts Inventory Management",
                "Maintenance Cost Control",
                "Equipment Performance Monitoring",
                "Facility Safety and Security"
            ],
            "Safety & Compliance": [
                "Workplace Safety Programs and Protocols",
                "Regulatory Compliance Management",
                "Incident Investigation and Reporting",
                "Environmental Health and Safety Training",
                "Safety Audits and Inspections",
                "Risk Assessment and Mitigation",
                "Emergency Response Planning",
                "Safety Performance Metrics",
                "Compliance Documentation and Reporting"
            ],
            
            # Healthcare Industry
            "Patient Care": [
                "Patient Assessment and Monitoring",
                "Treatment Planning and Coordination",
                "Medication Administration and Management",
                "Patient Education and Communication",
                "Care Documentation and Records",
                "Patient Safety and Quality Measures",
                "Discharge Planning and Follow-up",
                "Interdisciplinary Care Coordination",
                "Patient Experience and Satisfaction"
            ],
            "Clinical Operations": [
                "Patient Scheduling and Appointments",
                "Clinical Workflow Management",
                "Medical Equipment and Resource Management",
                "Clinical Decision Support Systems",
                "Quality Metrics and Performance Monitoring",
                "Regulatory Compliance and Reporting",
                "Clinical Staff Coordination",
                "Patient Flow and Capacity Management",
                "Clinical Protocol and Guideline Management"
            ],
            "Medical Records": [
                "Electronic Health Records",
                "Medical Coding",
                "Documentation Management",
                "Data Privacy & Security",
                "Interoperability",
                "Clinical Data Analytics"
            ],
            "Pharmacy": [
                "Medication Management",
                "Prescription Processing",
                "Drug Interaction Monitoring",
                "Inventory Management",
                "Clinical Pharmacy Services",
                "Regulatory Compliance"
            ],
            "Laboratory Services": [
                "Sample Processing",
                "Test Management",
                "Quality Control",
                "Results Reporting",
                "Equipment Management",
                "Laboratory Information Systems"
            ],
            "Administrative Services": [
                "Patient Registration",
                "Insurance Processing",
                "Billing & Collections",
                "Scheduling Coordination",
                "Medical Records Management",
                "Regulatory Documentation"
            ],
            "Finance & Billing": [
                "Revenue Cycle Management",
                "Claims Processing",
                "Patient Billing",
                "Insurance Verification",
                "Payment Processing",
                "Financial Reporting"
            ],
            "Compliance & Risk Management": [
                "Regulatory Compliance",
                "Risk Assessment",
                "Quality Assurance",
                "Policy Management",
                "Audit & Monitoring",
                "Safety Management"
            ],
            
            # Life Sciences Industry
            "R&D & Discovery": [
                "Target Identification and Validation",
                "Lead Compound Discovery and Optimization",
                "Preclinical Research and Development",
                "Biomarker Discovery and Development",
                "Research Data Management and Analysis",
                "Laboratory Information Management",
                "Intellectual Property Management",
                "Scientific Literature and Intelligence",
                "Research Collaboration and Partnerships"
            ],
            "Clinical Trials": [
                "Protocol Design and Development",
                "Clinical Trial Management and Operations",
                "Patient Recruitment and Retention",
                "Clinical Data Management and Monitoring",
                "Regulatory Submissions and Reporting",
                "Site Management and Training",
                "Safety Monitoring and Pharmacovigilance",
                "Clinical Trial Supply Management",
                "Clinical Quality Assurance"
            ],
            "Regulatory Affairs": [
                "Regulatory Strategy and Planning",
                "Regulatory Submissions and Filings",
                "Regulatory Compliance and Monitoring",
                "Agency Interactions and Communications",
                "Product Labeling and Documentation",
                "Post-Market Surveillance and Reporting",
                "Global Regulatory Intelligence",
                "Regulatory Change Management",
                "Regulatory Training and Education"
            ],
            "Manufacturing & Production": [
                "Process Development and Scale-up",
                "Production Planning and Scheduling",
                "Manufacturing Execution and Control",
                "Quality Control and Testing",
                "Batch Record Management",
                "Equipment Validation and Qualification",
                "Supply Chain and Materials Management",
                "Manufacturing Technology Transfer",
                "Production Cost Management"
            ],
            "Quality Assurance": [
                "Quality Management Systems",
                "Validation and Verification Programs",
                "Quality Audit and Inspection Management",
                "Deviation Investigation and CAPA",
                "Document Control and Management",
                "Quality Training and Competency",
                "Supplier Quality Management",
                "Quality Risk Management",
                "Continuous Improvement Programs"
            ],
            "Medical Affairs": [
                "Medical Strategy and Planning",
                "Scientific Communications and Publications",
                "Medical Information and Inquiry Management",
                "Clinical Evidence Generation and RWE",
                "Key Opinion Leader Management",
                "Medical Education and Training",
                "Safety Surveillance and Risk Management",
                "Medical Review and Approval",
                "Health Economics and Outcomes Research"
            ],
            "Commercial Operations": [
                "Sales Strategy and Planning",
                "Sales Force Effectiveness and Training",
                "Marketing Strategy and Campaign Management",
                "Market Access and Pricing Strategy",
                "Customer Relationship Management",
                "Digital Marketing and Omnichannel",
                "Product Launch and Lifecycle Management",
                "Commercial Analytics and Insights",
                "Channel and Distribution Management"
            ],
            "Supply Chain": [
                "Demand Planning",
                "Procurement",
                "Manufacturing Planning",
                "Distribution",
                "Inventory Management",
                "Vendor Management"
            ],
            
            # Common Functions (appear in multiple industries)
            "Finance & Accounting": [
                "Accounts Payable / Receivable",
                "General Ledger / Bookkeeping",
                "Financial Planning & Analysis (FP&A)",
                "Tax & Treasury",
                "Audit & Controls",
                "Financial Reporting"
            ],
            "HR & Talent Management": [
                "Talent Acquisition / Recruiting",
                "Learning & Development",
                "Performance Management",
                "Compensation & Benefits",
                "Workforce Planning",
                "Employee Relations & HR Operations"
            ],
            "Operations & Supply Chain": [
                "Inventory Management",
                "Procurement / Sourcing",
                "Logistics & Distribution",
                "Manufacturing Planning",
                "Demand Forecasting",
                "Vendor & Supplier Management"
            ],
            "Sales & Marketing": [
                "Lead Generation",
                "Sales Enablement",
                "CRM & Pipeline Management",
                "Campaign Management",
                "Digital / Performance Marketing",
                "Brand & Content Strategy",
                "Customer Analytics"
            ],
            "IT & Technology": [
                "Infrastructure & Networks",
                "Security & Access Management",
                "IT Helpdesk / End-User Support",
                "Enterprise Systems (ERP, HCM)",
                "Application Development",
                "DevOps / IT Operations"
            ],
            "Customer Service": [
                "Contact Center Operations",
                "Ticketing / Case Management",
                "Escalation Management",
                "Field Service Support",
                "Omnichannel Engagement",
                "Self-Service & Automation"
            ],
            "Legal & Compliance": [
                "Contract Management",
                "Risk & Regulatory Compliance",
                "Data Privacy & Governance",
                "Litigation Support",
                "Policy Management",
                "IP & Trademark"
            ],
            "R&D": [
                "Product Discovery",
                "Prototype Development",
                "User Research & Testing",
                "Innovation Programs",
                "Scientific or Technical Research",
                "Regulatory Approvals (e.g., FDA, ISO)"
            ],
            "Manufacturing & Production": [
                "Production Planning",
                "Plant Operations",
                "Assembly Line Optimization",
                "Equipment Maintenance",
                "Quality Control",
                "Shop Floor Data Capture"
            ],
            "Quality Assurance": [
                "Product Testing & Certification",
                "Root Cause Analysis",
                "Corrective & Preventive Action (CAPA)",
                "Supplier Quality Management",
                "Customer Feedback Loop",
                "Audits & Documentation"
            ],
            "Business Development": [
                "Strategic Partnerships",
                "M&A Pipeline Development",
                "New Market Entry",
                "Go-to-Market Strategy",
                "Competitive Intelligence",
                "Partner Onboarding"
            ],
            "Strategy & Planning": [
                "Corporate Strategy",
                "Strategic Initiatives / OKRs",
                "Business Case Development",
                "Portfolio & Scenario Planning",
                "Market and Competitive Analysis",
                "Transformation Program Management"
            ],
            "Risk Management": [
                "Enterprise Risk Assessment",
                "Operational Risk",
                "Financial Risk (e.g., credit, liquidity)",
                "Cybersecurity Risk",
                "Third-Party Risk",
                "Risk Controls & Monitoring"
            ],
            "Procurement": [
                "Sourcing Strategy",
                "Supplier Selection",
                "Contract Negotiation",
                "Purchase Order Management",
                "Category Management",
                "Supplier Performance Monitoring"
            ],
            "Facilities Management": [
                "Space Planning",
                "Maintenance & Repairs",
                "Safety & Compliance",
                "Real Estate Management",
                "Energy & Sustainability",
                "Physical Security"
            ],
            "Data & Analytics": [
                "BI & Reporting",
                "Data Engineering",
                "Data Governance",
                "Advanced Analytics & Modeling",
                "ML/AI Ops",
                "Self-Service Analytics Enablement"
            ]
        }
    
    def get_default_categories(self, function_name: str) -> List[str]:
        """Get default categories for a given function"""
        return self.default_categories.get(function_name, [
            "Process Automation",
            "Decision Support",
            "Analytics & Insights",
            "Customer Interaction",
            "Quality Control"
        ])
    
    def initialize_function_categories(self, function_name: str) -> None:
        """Initialize categories for a function if not already present"""
        if f'categories_{function_name}' not in st.session_state:
            default_cats = self.get_default_categories(function_name)
            st.session_state[f'categories_{function_name}'] = {
                cat: {"name": cat, "description": "", "ai_initiatives": {}}
                for cat in default_cats
            }
    
    def add_category(self, function_name: str, category_name: str, description: str = "") -> bool:
        """Add a new category to a function"""
        try:
            categories_key = f'categories_{function_name}'
            if categories_key not in st.session_state:
                self.initialize_function_categories(function_name)
            
            if category_name not in st.session_state[categories_key]:
                st.session_state[categories_key][category_name] = {
                    "name": category_name,
                    "description": description,
                    "ai_initiatives": {}
                }
                return True
            return False
        except Exception:
            return False
    
    def remove_category(self, function_name: str, category_name: str) -> bool:
        """Remove a category from a function"""
        try:
            categories_key = f'categories_{function_name}'
            if categories_key in st.session_state and category_name in st.session_state[categories_key]:
                del st.session_state[categories_key][category_name]
                return True
            return False
        except Exception:
            return False
    
    def get_categories(self, function_name: str) -> Dict:
        """Get all categories for a function"""
        categories_key = f'categories_{function_name}'
        if categories_key not in st.session_state:
            self.initialize_function_categories(function_name)
        return st.session_state[categories_key]
    
    def add_ai_initiative(self, function_name: str, category_name: str, 
                         initiative_name: str, initiative_data: Dict) -> str:
        """Add an AI initiative to a category"""
        try:
            categories_key = f'categories_{function_name}'
            if categories_key not in st.session_state:
                self.initialize_function_categories(function_name)
            
            if category_name not in st.session_state[categories_key]:
                return None
            
            initiative_id = str(uuid.uuid4())
            initiative_data['id'] = initiative_id
            initiative_data['name'] = initiative_name
            initiative_data['created_at'] = datetime.now().isoformat()
            initiative_data['updated_at'] = datetime.now().isoformat()
            
            st.session_state[categories_key][category_name]['ai_initiatives'][initiative_id] = initiative_data
            return initiative_id
        except Exception:
            return None
    
    def update_ai_initiative(self, function_name: str, category_name: str, 
                           initiative_id: str, initiative_data: Dict) -> bool:
        """Update an existing AI initiative"""
        try:
            categories_key = f'categories_{function_name}'
            if (categories_key in st.session_state and 
                category_name in st.session_state[categories_key] and
                initiative_id in st.session_state[categories_key][category_name]['ai_initiatives']):
                
                initiative_data['updated_at'] = datetime.now().isoformat()
                st.session_state[categories_key][category_name]['ai_initiatives'][initiative_id].update(initiative_data)
                return True
            return False
        except Exception:
            return False
    
    def remove_ai_initiative(self, function_name: str, category_name: str, initiative_id: str) -> bool:
        """Remove an AI initiative from a category"""
        try:
            categories_key = f'categories_{function_name}'
            if (categories_key in st.session_state and 
                category_name in st.session_state[categories_key] and
                initiative_id in st.session_state[categories_key][category_name]['ai_initiatives']):
                
                del st.session_state[categories_key][category_name]['ai_initiatives'][initiative_id]
                return True
            return False
        except Exception:
            return False
    
    def get_ai_initiatives(self, function_name: str, category_name: str = None) -> Dict:
        """Get AI initiatives for a category or all categories in a function"""
        categories_key = f'categories_{function_name}'
        if categories_key not in st.session_state:
            return {}
        
        if category_name:
            if category_name in st.session_state[categories_key]:
                return st.session_state[categories_key][category_name]['ai_initiatives']
            return {}
        else:
            # Return all initiatives across all categories
            all_initiatives = {}
            for cat_name, cat_data in st.session_state[categories_key].items():
                for init_id, init_data in cat_data['ai_initiatives'].items():
                    all_initiatives[f"{cat_name}_{init_id}"] = {
                        **init_data,
                        'category': cat_name
                    }
            return all_initiatives
    
    def get_function_summary(self, function_name: str) -> Dict:
        """Get summary statistics for a function"""
        categories = self.get_categories(function_name)
        
        total_initiatives = 0
        total_investment = 0
        ai_types = {}
        
        for category_name, category_data in categories.items():
            initiatives = category_data['ai_initiatives']
            total_initiatives += len(initiatives)
            
            for initiative in initiatives.values():
                investment = initiative.get('investment', 0)
                if isinstance(investment, (int, float)):
                    total_investment += investment
                
                ai_type = initiative.get('ai_type', 'Unknown')
                ai_types[ai_type] = ai_types.get(ai_type, 0) + 1
        
        return {
            'total_categories': len(categories),
            'total_initiatives': total_initiatives,
            'total_investment': total_investment,
            'ai_type_distribution': ai_types,
            'categories': list(categories.keys())
        }
    
    def export_function_data(self, function_name: str) -> Dict:
        """Export all function data including categories and initiatives"""
        return {
            'function_name': function_name,
            'baseline_data': st.session_state.baseline_data.get(function_name, {}),
            'categories': self.get_categories(function_name),
            'summary': self.get_function_summary(function_name),
            'exported_at': datetime.now().isoformat()
        }
    
    def calculate_category_totals(self, function_name: str, category_name: str) -> Dict:
        """Calculate aggregate metrics for all initiatives in a category"""
        initiatives = self.get_ai_initiatives(function_name, category_name)
        
        if not initiatives:
            return {
                'total_investment': 0,
                'total_initiatives': 0,
                'avg_automation_level': 0,
                'avg_expected_roi': 0,
                'total_workforce_impact': 0
            }
        
        total_investment = sum(init.get('investment', 0) for init in initiatives.values())
        total_initiatives = len(initiatives)
        
        automation_levels = [init.get('automation_level', 0) for init in initiatives.values()]
        avg_automation = sum(automation_levels) / len(automation_levels) if automation_levels else 0
        
        workforce_reductions = [init.get('workforce_reduction', 0) for init in initiatives.values()]
        total_workforce_impact = sum(workforce_reductions)
        
        # Estimate combined ROI (simplified calculation)
        rois = []
        for init in initiatives.values():
            # Use stored prediction data if available
            if 'predicted_roi' in init:
                rois.append(init['predicted_roi'])
            else:
                # Basic estimation based on investment and automation level
                investment = init.get('investment', 0)
                automation = init.get('automation_level', 0)
                if investment > 0:
                    estimated_roi = (automation / 100) * 25  # Basic heuristic
                    rois.append(estimated_roi)
        
        avg_roi = sum(rois) / len(rois) if rois else 0
        
        return {
            'total_investment': total_investment,
            'total_initiatives': total_initiatives,
            'avg_automation_level': avg_automation,
            'avg_expected_roi': avg_roi,
            'total_workforce_impact': total_workforce_impact,
            'initiatives_by_type': self._count_by_ai_type(initiatives)
        }
    
    def _count_by_ai_type(self, initiatives: Dict) -> Dict:
        """Count initiatives by AI type"""
        type_counts = {}
        for init in initiatives.values():
            ai_type = init.get('ai_type', 'Unknown')
            type_counts[ai_type] = type_counts.get(ai_type, 0) + 1
        return type_counts