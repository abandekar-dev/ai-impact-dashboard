import streamlit as st
import pandas as pd
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import urllib.parse

class ERPIntegration:
    """Integration with Enterprise Resource Planning systems"""
    
    def __init__(self):
        self.supported_systems = {
            'SAP': {'name': 'SAP ERP', 'auth_type': 'oauth', 'base_url_required': True},
            'Oracle': {'name': 'Oracle ERP Cloud', 'auth_type': 'basic', 'base_url_required': True},
            'Microsoft': {'name': 'Microsoft Dynamics 365', 'auth_type': 'oauth', 'base_url_required': True},
            'Workday': {'name': 'Workday ERP', 'auth_type': 'oauth', 'base_url_required': True},
            'NetSuite': {'name': 'Oracle NetSuite', 'auth_type': 'token', 'base_url_required': True},
            'Salesforce': {'name': 'Salesforce', 'auth_type': 'oauth', 'base_url_required': False}
        }
    
    def get_financial_data(self, system: str, department: str = None) -> Dict[str, Any]:
        """Retrieve financial data from ERP system"""
        try:
            if system == 'SAP':
                return self._get_sap_financial_data(department)
            elif system == 'Oracle':
                return self._get_oracle_financial_data(department)
            elif system == 'Microsoft':
                return self._get_dynamics_financial_data(department)
            elif system == 'Workday':
                return self._get_workday_financial_data(department)
            elif system == 'NetSuite':
                return self._get_netsuite_financial_data(department)
            elif system == 'Salesforce':
                return self._get_salesforce_financial_data(department)
            else:
                raise ValueError(f"Unsupported ERP system: {system}")
        except Exception as e:
            st.error(f"Failed to retrieve financial data from {system}: {str(e)}")
            return {}
    
    def _get_sap_financial_data(self, department: str = None) -> Dict[str, Any]:
        """Retrieve financial data from SAP ERP"""
        base_url = st.secrets.get('SAP_BASE_URL', '')
        client_id = st.secrets.get('SAP_CLIENT_ID', '')
        client_secret = st.secrets.get('SAP_CLIENT_SECRET', '')
        
        if not all([base_url, client_id, client_secret]):
            raise ValueError("SAP credentials not configured")
        
        # SAP API endpoint for financial data
        endpoint = f"{base_url}/sap/opu/odata/sap/ZFI_COST_CENTER_SRV/CostCenterSet"
        
        headers = {
            'Authorization': f'Basic {self._encode_credentials(client_id, client_secret)}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        params = {}
        if department:
            params['$filter'] = f"CostCenter eq '{department}'"
        
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return self._process_sap_financial_data(data)
    
    def _get_oracle_financial_data(self, department: str = None) -> Dict[str, Any]:
        """Retrieve financial data from Oracle ERP Cloud"""
        base_url = st.secrets.get('ORACLE_BASE_URL', '')
        username = st.secrets.get('ORACLE_USERNAME', '')
        password = st.secrets.get('ORACLE_PASSWORD', '')
        
        if not all([base_url, username, password]):
            raise ValueError("Oracle ERP credentials not configured")
        
        # Oracle REST API endpoint
        endpoint = f"{base_url}/fscmRestApi/resources/11.13.18.05/financeGeneralLedgerBalances"
        
        headers = {
            'Authorization': f'Basic {self._encode_credentials(username, password)}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        params = {
            'q': f"BalanceDate >= '{(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')}'"
        }
        
        if department:
            params['q'] += f" AND CostCenter = '{department}'"
        
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return self._process_oracle_financial_data(data)
    
    def _get_dynamics_financial_data(self, department: str = None) -> Dict[str, Any]:
        """Retrieve financial data from Microsoft Dynamics 365"""
        base_url = st.secrets.get('DYNAMICS_BASE_URL', '')
        access_token = st.secrets.get('DYNAMICS_ACCESS_TOKEN', '')
        
        if not all([base_url, access_token]):
            raise ValueError("Microsoft Dynamics 365 credentials not configured")
        
        # Dynamics 365 Finance API endpoint
        endpoint = f"{base_url}/data/GeneralLedgerEntries"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        params = {
            '$filter': f"AccountingDate ge {(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')}"
        }
        
        if department:
            params['$filter'] += f" and Department eq '{department}'"
        
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return self._process_dynamics_financial_data(data)
    
    def _get_workday_financial_data(self, department: str = None) -> Dict[str, Any]:
        """Retrieve financial data from Workday"""
        base_url = st.secrets.get('WORKDAY_BASE_URL', '')
        username = st.secrets.get('WORKDAY_USERNAME', '')
        password = st.secrets.get('WORKDAY_PASSWORD', '')
        tenant = st.secrets.get('WORKDAY_TENANT', '')
        
        if not all([base_url, username, password, tenant]):
            raise ValueError("Workday credentials not configured")
        
        # Workday Financial Management API
        endpoint = f"{base_url}/ccx/service/{tenant}/Financial_Management/v39.2"
        
        headers = {
            'Authorization': f'Basic {self._encode_credentials(username, password)}',
            'Accept': 'application/json',
            'Content-Type': 'text/xml'
        }
        
        # Workday uses SOAP/XML format
        soap_body = self._build_workday_soap_request(department)
        
        response = requests.post(endpoint, headers=headers, data=soap_body, timeout=30)
        response.raise_for_status()
        
        return self._process_workday_financial_data(response.text)
    
    def _get_netsuite_financial_data(self, department: str = None) -> Dict[str, Any]:
        """Retrieve financial data from NetSuite"""
        account_id = st.secrets.get('NETSUITE_ACCOUNT_ID', '')
        consumer_key = st.secrets.get('NETSUITE_CONSUMER_KEY', '')
        consumer_secret = st.secrets.get('NETSUITE_CONSUMER_SECRET', '')
        token_id = st.secrets.get('NETSUITE_TOKEN_ID', '')
        token_secret = st.secrets.get('NETSUITE_TOKEN_SECRET', '')
        
        if not all([account_id, consumer_key, consumer_secret, token_id, token_secret]):
            raise ValueError("NetSuite credentials not configured")
        
        # NetSuite RESTlet endpoint
        base_url = f"https://{account_id}.suitetalk.api.netsuite.com/services/rest/record/v1"
        endpoint = f"{base_url}/customrecord_financial_data"
        
        headers = {
            'Authorization': self._build_netsuite_oauth_header(
                consumer_key, consumer_secret, token_id, token_secret
            ),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        params = {}
        if department:
            params['q'] = f"department CONTAINS '{department}'"
        
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return self._process_netsuite_financial_data(data)
    
    def _get_salesforce_financial_data(self, department: str = None) -> Dict[str, Any]:
        """Retrieve financial data from Salesforce"""
        instance_url = st.secrets.get('SALESFORCE_INSTANCE_URL', '')
        access_token = st.secrets.get('SALESFORCE_ACCESS_TOKEN', '')
        
        if not all([instance_url, access_token]):
            raise ValueError("Salesforce credentials not configured")
        
        # Salesforce SOQL query
        soql = "SELECT Id, Name, Amount, Department__c, CreatedDate FROM Financial_Record__c WHERE CreatedDate = LAST_N_DAYS:365"
        
        if department:
            soql += f" AND Department__c = '{department}'"
        
        endpoint = f"{instance_url}/services/data/v58.0/query"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        params = {'q': soql}
        
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return self._process_salesforce_financial_data(data)
    
    def _encode_credentials(self, username: str, password: str) -> str:
        """Encode credentials for basic authentication"""
        import base64
        credentials = f"{username}:{password}"
        return base64.b64encode(credentials.encode()).decode()
    
    def _process_sap_financial_data(self, data: Dict) -> Dict[str, Any]:
        """Process SAP financial data response"""
        results = data.get('d', {}).get('results', [])
        
        total_revenue = sum(float(item.get('Revenue', 0)) for item in results)
        total_costs = sum(float(item.get('Costs', 0)) for item in results)
        
        return {
            'annual_revenue': total_revenue,
            'annual_costs': total_costs,
            'data_source': 'SAP ERP',
            'last_updated': datetime.now().isoformat(),
            'record_count': len(results)
        }
    
    def _process_oracle_financial_data(self, data: Dict) -> Dict[str, Any]:
        """Process Oracle ERP financial data response"""
        items = data.get('items', [])
        
        revenue_items = [item for item in items if item.get('AccountType') == 'Revenue']
        cost_items = [item for item in items if item.get('AccountType') == 'Expense']
        
        total_revenue = sum(float(item.get('BalanceAmount', 0)) for item in revenue_items)
        total_costs = sum(float(item.get('BalanceAmount', 0)) for item in cost_items)
        
        return {
            'annual_revenue': total_revenue,
            'annual_costs': total_costs,
            'data_source': 'Oracle ERP Cloud',
            'last_updated': datetime.now().isoformat(),
            'record_count': len(items)
        }
    
    def _process_dynamics_financial_data(self, data: Dict) -> Dict[str, Any]:
        """Process Microsoft Dynamics 365 financial data response"""
        entries = data.get('value', [])
        
        revenue_entries = [entry for entry in entries if entry.get('AccountCategory') == 'Revenue']
        cost_entries = [entry for entry in entries if entry.get('AccountCategory') == 'Expense']
        
        total_revenue = sum(float(entry.get('AmountCurr', 0)) for entry in revenue_entries)
        total_costs = sum(float(entry.get('AmountCurr', 0)) for entry in cost_entries)
        
        return {
            'annual_revenue': total_revenue,
            'annual_costs': total_costs,
            'data_source': 'Microsoft Dynamics 365',
            'last_updated': datetime.now().isoformat(),
            'record_count': len(entries)
        }
    
    def _build_workday_soap_request(self, department: str = None) -> str:
        """Build SOAP request for Workday API"""
        filter_clause = f"<wd:Cost_Center_Reference><wd:ID wd:type='Cost_Center_ID'>{department}</wd:ID></wd:Cost_Center_Reference>" if department else ""
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wd="urn:com.workday/bsvc">
            <soapenv:Header/>
            <soapenv:Body>
                <wd:Get_Financial_Data_Request>
                    {filter_clause}
                    <wd:Response_Filter>
                        <wd:As_Of_Effective_Date>{datetime.now().strftime('%Y-%m-%d')}</wd:As_Of_Effective_Date>
                    </wd:Response_Filter>
                </wd:Get_Financial_Data_Request>
            </soapenv:Body>
        </soapenv:Envelope>"""
    
    def _process_workday_financial_data(self, xml_data: str) -> Dict[str, Any]:
        """Process Workday XML response"""
        # Basic XML parsing for financial data
        # In production, use proper XML parsing library
        revenue_match = xml_data.find('<wd:Revenue>')
        costs_match = xml_data.find('<wd:Expenses>')
        
        revenue = 0
        costs = 0
        
        if revenue_match != -1:
            end_tag = xml_data.find('</wd:Revenue>', revenue_match)
            revenue = float(xml_data[revenue_match + 12:end_tag])
        
        if costs_match != -1:
            end_tag = xml_data.find('</wd:Expenses>', costs_match)
            costs = float(xml_data[costs_match + 13:end_tag])
        
        return {
            'annual_revenue': revenue,
            'annual_costs': costs,
            'data_source': 'Workday',
            'last_updated': datetime.now().isoformat(),
            'record_count': 1
        }
    
    def _build_netsuite_oauth_header(self, consumer_key: str, consumer_secret: str, 
                                   token_id: str, token_secret: str) -> str:
        """Build OAuth header for NetSuite"""
        import hmac
        import hashlib
        import base64
        import time
        
        timestamp = str(int(time.time()))
        nonce = base64.b64encode(f"{timestamp}:{consumer_key}".encode()).decode()
        
        # Simplified OAuth signature
        signature_base = f"GET&{urllib.parse.quote_plus('netsuite.com')}&{timestamp}"
        signature = base64.b64encode(
            hmac.new(
                f"{consumer_secret}&{token_secret}".encode(),
                signature_base.encode(),
                hashlib.sha256
            ).digest()
        ).decode()
        
        return f'OAuth oauth_consumer_key="{consumer_key}", oauth_token="{token_id}", oauth_signature_method="HMAC-SHA256", oauth_timestamp="{timestamp}", oauth_nonce="{nonce}", oauth_signature="{signature}"'
    
    def _process_netsuite_financial_data(self, data: Dict) -> Dict[str, Any]:
        """Process NetSuite financial data response"""
        items = data.get('items', [])
        
        total_revenue = sum(float(item.get('revenue', 0)) for item in items)
        total_costs = sum(float(item.get('expenses', 0)) for item in items)
        
        return {
            'annual_revenue': total_revenue,
            'annual_costs': total_costs,
            'data_source': 'NetSuite',
            'last_updated': datetime.now().isoformat(),
            'record_count': len(items)
        }
    
    def _process_salesforce_financial_data(self, data: Dict) -> Dict[str, Any]:
        """Process Salesforce financial data response"""
        records = data.get('records', [])
        
        total_revenue = sum(float(record.get('Amount', 0)) for record in records if record.get('Amount'))
        
        return {
            'annual_revenue': total_revenue,
            'annual_costs': 0,  # Assuming revenue-focused data
            'data_source': 'Salesforce',
            'last_updated': datetime.now().isoformat(),
            'record_count': len(records)
        }

class HRMIntegration:
    """Integration with Human Resource Management systems"""
    
    def __init__(self):
        self.supported_systems = {
            'Workday': {'name': 'Workday HCM', 'auth_type': 'oauth'},
            'SuccessFactors': {'name': 'SAP SuccessFactors', 'auth_type': 'oauth'},
            'BambooHR': {'name': 'BambooHR', 'auth_type': 'basic'},
            'ADP': {'name': 'ADP Workforce Now', 'auth_type': 'oauth'},
            'Cornerstone': {'name': 'Cornerstone OnDemand', 'auth_type': 'basic'},
            'UltiPro': {'name': 'UKG Pro', 'auth_type': 'oauth'}
        }
    
    def get_workforce_data(self, system: str, department: str = None) -> Dict[str, Any]:
        """Retrieve workforce data from HRM system"""
        try:
            if system == 'Workday':
                return self._get_workday_hr_data(department)
            elif system == 'SuccessFactors':
                return self._get_successfactors_data(department)
            elif system == 'BambooHR':
                return self._get_bamboo_hr_data(department)
            elif system == 'ADP':
                return self._get_adp_data(department)
            elif system == 'Cornerstone':
                return self._get_cornerstone_data(department)
            elif system == 'UltiPro':
                return self._get_ultipro_data(department)
            else:
                raise ValueError(f"Unsupported HRM system: {system}")
        except Exception as e:
            st.error(f"Failed to retrieve workforce data from {system}: {str(e)}")
            return {}
    
    def _get_workday_hr_data(self, department: str = None) -> Dict[str, Any]:
        """Retrieve workforce data from Workday HCM"""
        base_url = st.secrets.get('WORKDAY_BASE_URL', '')
        username = st.secrets.get('WORKDAY_USERNAME', '')
        password = st.secrets.get('WORKDAY_PASSWORD', '')
        tenant = st.secrets.get('WORKDAY_TENANT', '')
        
        if not all([base_url, username, password, tenant]):
            raise ValueError("Workday HCM credentials not configured")
        
        endpoint = f"{base_url}/ccx/service/{tenant}/Human_Resources/v39.2"
        
        headers = {
            'Authorization': f'Basic {self._encode_credentials(username, password)}',
            'Content-Type': 'text/xml',
            'Accept': 'application/json'
        }
        
        soap_body = self._build_workday_hr_soap_request(department)
        
        response = requests.post(endpoint, headers=headers, data=soap_body, timeout=30)
        response.raise_for_status()
        
        return self._process_workday_hr_data(response.text)
    
    def _get_successfactors_data(self, department: str = None) -> Dict[str, Any]:
        """Retrieve workforce data from SAP SuccessFactors"""
        base_url = st.secrets.get('SUCCESSFACTORS_BASE_URL', '')
        access_token = st.secrets.get('SUCCESSFACTORS_ACCESS_TOKEN', '')
        
        if not all([base_url, access_token]):
            raise ValueError("SAP SuccessFactors credentials not configured")
        
        endpoint = f"{base_url}/odata/v2/User"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        params = {'$format': 'json'}
        if department:
            params['$filter'] = f"department eq '{department}'"
        
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return self._process_successfactors_data(data)
    
    def _get_bamboo_hr_data(self, department: str = None) -> Dict[str, Any]:
        """Retrieve workforce data from BambooHR"""
        subdomain = st.secrets.get('BAMBOOHR_SUBDOMAIN', '')
        api_key = st.secrets.get('BAMBOOHR_API_KEY', '')
        
        if not all([subdomain, api_key]):
            raise ValueError("BambooHR credentials not configured")
        
        endpoint = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/employees/directory"
        
        headers = {
            'Authorization': f'Basic {self._encode_credentials(api_key, "x")}',
            'Accept': 'application/json'
        }
        
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return self._process_bamboo_hr_data(data, department)
    
    def _encode_credentials(self, username: str, password: str) -> str:
        """Encode credentials for basic authentication"""
        import base64
        credentials = f"{username}:{password}"
        return base64.b64encode(credentials.encode()).decode()
    
    def _build_workday_hr_soap_request(self, department: str = None) -> str:
        """Build SOAP request for Workday HCM API"""
        filter_clause = f"<wd:Organization_Reference><wd:ID wd:type='Organization_Reference_ID'>{department}</wd:ID></wd:Organization_Reference>" if department else ""
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wd="urn:com.workday/bsvc">
            <soapenv:Header/>
            <soapenv:Body>
                <wd:Get_Workers_Request>
                    {filter_clause}
                    <wd:Response_Filter>
                        <wd:As_Of_Effective_Date>{datetime.now().strftime('%Y-%m-%d')}</wd:As_Of_Effective_Date>
                        <wd:Count>1000</wd:Count>
                    </wd:Response_Filter>
                </wd:Get_Workers_Request>
            </soapenv:Body>
        </soapenv:Envelope>"""
    
    def _process_workday_hr_data(self, xml_data: str) -> Dict[str, Any]:
        """Process Workday HCM XML response"""
        # Basic XML parsing for workforce data
        worker_count = xml_data.count('<wd:Worker>')
        
        return {
            'headcount': worker_count,
            'data_source': 'Workday HCM',
            'last_updated': datetime.now().isoformat(),
            'productivity_index': 75.0,  # Default value
            'satisfaction_score': 80.0   # Default value
        }
    
    def _process_successfactors_data(self, data: Dict) -> Dict[str, Any]:
        """Process SAP SuccessFactors data response"""
        results = data.get('d', {}).get('results', [])
        
        active_employees = [emp for emp in results if emp.get('status') == 'Active']
        
        return {
            'headcount': len(active_employees),
            'data_source': 'SAP SuccessFactors',
            'last_updated': datetime.now().isoformat(),
            'productivity_index': 75.0,
            'satisfaction_score': 80.0
        }
    
    def _process_bamboo_hr_data(self, data: Dict, department: str = None) -> Dict[str, Any]:
        """Process BambooHR data response"""
        employees = data.get('employees', [])
        
        if department:
            employees = [emp for emp in employees if emp.get('department') == department]
        
        return {
            'headcount': len(employees),
            'data_source': 'BambooHR',
            'last_updated': datetime.now().isoformat(),
            'productivity_index': 75.0,
            'satisfaction_score': 80.0
        }

class DataIntegrationManager:
    """Manages integration with multiple enterprise data sources"""
    
    def __init__(self):
        self.erp_integration = ERPIntegration()
        self.hrm_integration = HRMIntegration()
    
    def test_connection(self, system_type: str, system_name: str) -> Dict[str, Any]:
        """Test connection to enterprise system"""
        try:
            if system_type == 'ERP':
                test_data = self.erp_integration.get_financial_data(system_name)
            elif system_type == 'HRM':
                test_data = self.hrm_integration.get_workforce_data(system_name)
            else:
                return {'success': False, 'error': f'Unknown system type: {system_type}'}
            
            return {
                'success': True,
                'message': f'Successfully connected to {system_name}',
                'data_preview': test_data
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Failed to connect to {system_name}'
            }
    
    def sync_department_data(self, department: str, erp_system: str = None, hrm_system: str = None) -> Dict[str, Any]:
        """Synchronize data for a specific department from enterprise systems"""
        result = {
            'department': department,
            'sync_timestamp': datetime.now().isoformat(),
            'financial_data': {},
            'workforce_data': {},
            'errors': []
        }
        
        # Sync financial data from ERP
        if erp_system:
            try:
                financial_data = self.erp_integration.get_financial_data(erp_system, department)
                result['financial_data'] = financial_data
            except Exception as e:
                result['errors'].append(f'ERP sync failed: {str(e)}')
        
        # Sync workforce data from HRM
        if hrm_system:
            try:
                workforce_data = self.hrm_integration.get_workforce_data(hrm_system, department)
                result['workforce_data'] = workforce_data
            except Exception as e:
                result['errors'].append(f'HRM sync failed: {str(e)}')
        
        return result
    
    def get_supported_systems(self) -> Dict[str, Dict]:
        """Get list of supported enterprise systems"""
        return {
            'ERP': self.erp_integration.supported_systems,
            'HRM': self.hrm_integration.supported_systems
        }