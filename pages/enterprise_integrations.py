import streamlit as st
import pandas as pd
from typing import Dict, List
from datetime import datetime
from utils.enterprise_integrations import DataIntegrationManager

def show_enterprise_integrations():
    """Enterprise data source integration configuration page"""
    
    st.header("🔗 Enterprise Data Integration")
    st.markdown("**Connect to your ERP and HRM systems for authentic data synchronization**")
    
    # Initialize integration manager
    integration_manager = DataIntegrationManager()
    supported_systems = integration_manager.get_supported_systems()
    
    # Initialize session state for integration settings
    if 'integration_settings' not in st.session_state:
        st.session_state.integration_settings = {
            'erp_system': None,
            'hrm_system': None,
            'auto_sync': False,
            'last_sync': None
        }
    
    st.markdown("---")
    
    # Integration configuration tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏢 ERP Systems", 
        "👥 HRM Systems", 
        "🔄 Data Synchronization", 
        "📊 Integration Status"
    ])
    
    with tab1:
        show_erp_configuration(integration_manager, supported_systems['ERP'])
    
    with tab2:
        show_hrm_configuration(integration_manager, supported_systems['HRM'])
    
    with tab3:
        show_data_synchronization(integration_manager)
    
    with tab4:
        show_integration_status(integration_manager)

def show_erp_configuration(integration_manager, erp_systems):
    """Configure ERP system connections"""
    
    st.subheader("💼 ERP System Configuration")
    
    # ERP system selection
    erp_options = ["None"] + list(erp_systems.keys())
    current_erp = st.session_state.integration_settings.get('erp_system', 'None')
    
    selected_erp = st.selectbox(
        "Select ERP System", 
        erp_options,
        index=erp_options.index(current_erp) if current_erp in erp_options else 0
    )
    
    if selected_erp != "None":
        erp_info = erp_systems[selected_erp]
        st.info(f"Configuring connection to {erp_info['name']}")
        
        # Credentials configuration
        st.markdown("#### Connection Settings")
        
        with st.expander("🔐 Authentication Configuration", expanded=True):
            auth_type = erp_info['auth_type']
            
            if auth_type == 'oauth':
                st.markdown("**OAuth 2.0 Configuration**")
                col1, col2 = st.columns(2)
                with col1:
                    client_id = st.text_input(f"{selected_erp} Client ID", type="password")
                    base_url = st.text_input(f"{selected_erp} Base URL") if erp_info.get('base_url_required') else ""
                with col2:
                    client_secret = st.text_input(f"{selected_erp} Client Secret", type="password")
                    tenant_id = st.text_input(f"{selected_erp} Tenant ID") if selected_erp in ['Microsoft', 'Workday'] else ""
                
            elif auth_type == 'basic':
                st.markdown("**Basic Authentication**")
                col1, col2 = st.columns(2)
                with col1:
                    username = st.text_input(f"{selected_erp} Username")
                    base_url = st.text_input(f"{selected_erp} Base URL") if erp_info.get('base_url_required') else ""
                with col2:
                    password = st.text_input(f"{selected_erp} Password", type="password")
                
            elif auth_type == 'token':
                st.markdown("**Token-based Authentication**")
                col1, col2 = st.columns(2)
                with col1:
                    account_id = st.text_input(f"{selected_erp} Account ID")
                    consumer_key = st.text_input(f"{selected_erp} Consumer Key", type="password")
                    token_id = st.text_input(f"{selected_erp} Token ID", type="password")
                with col2:
                    consumer_secret = st.text_input(f"{selected_erp} Consumer Secret", type="password")
                    token_secret = st.text_input(f"{selected_erp} Token Secret", type="password")
        
        # Test connection
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Test ERP Connection", type="primary"):
                with st.spinner("Testing connection..."):
                    test_result = integration_manager.test_connection('ERP', selected_erp)
                    
                    if test_result['success']:
                        st.success(f"✅ Successfully connected to {selected_erp}")
                        if test_result.get('data_preview'):
                            st.json(test_result['data_preview'])
                        st.session_state.integration_settings['erp_system'] = selected_erp
                    else:
                        st.error(f"❌ Connection failed: {test_result['error']}")
                        if "credentials not configured" in test_result['error'].lower():
                            st.info("Please ensure you have provided the required API credentials in your secrets configuration.")
        
        with col2:
            if st.button("💾 Save ERP Configuration"):
                st.session_state.integration_settings['erp_system'] = selected_erp
                st.success("ERP configuration saved!")
        
        # Data mapping configuration
        st.markdown("#### Data Mapping")
        
        with st.expander("📋 Field Mapping Configuration"):
            st.markdown("**Map ERP fields to dashboard metrics:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Revenue Field", value="Revenue", help="ERP field name for revenue data")
                st.text_input("Cost Field", value="Costs", help="ERP field name for cost data")
                st.text_input("Department Field", value="CostCenter", help="ERP field name for department/cost center")
            
            with col2:
                st.text_input("Date Field", value="AccountingDate", help="ERP field name for transaction date")
                st.text_input("Currency Field", value="Currency", help="ERP field name for currency")
                st.selectbox("Data Aggregation", ["Monthly", "Quarterly", "Annual"], index=2)

def show_hrm_configuration(integration_manager, hrm_systems):
    """Configure HRM system connections"""
    
    st.subheader("👥 HRM System Configuration")
    
    # HRM system selection
    hrm_options = ["None"] + list(hrm_systems.keys())
    current_hrm = st.session_state.integration_settings.get('hrm_system', 'None')
    
    selected_hrm = st.selectbox(
        "Select HRM System", 
        hrm_options,
        index=hrm_options.index(current_hrm) if current_hrm in hrm_options else 0
    )
    
    if selected_hrm != "None":
        hrm_info = hrm_systems[selected_hrm]
        st.info(f"Configuring connection to {hrm_info['name']}")
        
        # Credentials configuration
        st.markdown("#### Connection Settings")
        
        with st.expander("🔐 Authentication Configuration", expanded=True):
            auth_type = hrm_info['auth_type']
            
            if auth_type == 'oauth':
                st.markdown("**OAuth 2.0 Configuration**")
                col1, col2 = st.columns(2)
                with col1:
                    client_id = st.text_input(f"{selected_hrm} Client ID", type="password", key="hrm_client_id")
                    base_url = st.text_input(f"{selected_hrm} Base URL", key="hrm_base_url")
                with col2:
                    access_token = st.text_input(f"{selected_hrm} Access Token", type="password", key="hrm_access_token")
                    tenant_id = st.text_input(f"{selected_hrm} Tenant ID", key="hrm_tenant") if selected_hrm == 'Workday' else ""
                
            elif auth_type == 'basic':
                st.markdown("**Basic Authentication**")
                col1, col2 = st.columns(2)
                with col1:
                    api_key = st.text_input(f"{selected_hrm} API Key", type="password", key="hrm_api_key")
                    subdomain = st.text_input(f"{selected_hrm} Subdomain", key="hrm_subdomain") if selected_hrm == 'BambooHR' else ""
                with col2:
                    username = st.text_input(f"{selected_hrm} Username", key="hrm_username")
                    password = st.text_input(f"{selected_hrm} Password", type="password", key="hrm_password")
        
        # Test connection
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Test HRM Connection", type="primary"):
                with st.spinner("Testing connection..."):
                    test_result = integration_manager.test_connection('HRM', selected_hrm)
                    
                    if test_result['success']:
                        st.success(f"✅ Successfully connected to {selected_hrm}")
                        if test_result.get('data_preview'):
                            st.json(test_result['data_preview'])
                        st.session_state.integration_settings['hrm_system'] = selected_hrm
                    else:
                        st.error(f"❌ Connection failed: {test_result['error']}")
                        if "credentials not configured" in test_result['error'].lower():
                            st.info("Please ensure you have provided the required API credentials in your secrets configuration.")
        
        with col2:
            if st.button("💾 Save HRM Configuration"):
                st.session_state.integration_settings['hrm_system'] = selected_hrm
                st.success("HRM configuration saved!")
        
        # Data mapping configuration
        st.markdown("#### Data Mapping")
        
        with st.expander("📋 Workforce Data Mapping"):
            st.markdown("**Map HRM fields to dashboard metrics:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Employee Count Field", value="headcount", help="HRM field for employee count")
                st.text_input("Department Field", value="department", help="HRM field for department")
                st.text_input("Job Title Field", value="jobTitle", help="HRM field for job titles")
            
            with col2:
                st.text_input("Performance Field", value="performanceRating", help="HRM field for performance ratings")
                st.text_input("Salary Field", value="salary", help="HRM field for salary data")
                st.selectbox("Data Sync Frequency", ["Daily", "Weekly", "Monthly"], index=1)

def show_data_synchronization(integration_manager):
    """Configure and manage data synchronization"""
    
    st.subheader("🔄 Data Synchronization")
    
    # Get configured functions
    configured_functions = list(st.session_state.baseline_data.keys()) if st.session_state.baseline_data else []
    
    if not configured_functions:
        st.warning("Please configure functions in 'Input by Department/Business' first.")
        return
    
    erp_system = st.session_state.integration_settings.get('erp_system')
    hrm_system = st.session_state.integration_settings.get('hrm_system')
    
    if not erp_system and not hrm_system:
        st.warning("Please configure at least one enterprise system (ERP or HRM) first.")
        return
    
    # Sync configuration
    st.markdown("#### Synchronization Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_sync = st.checkbox(
            "Enable Automatic Synchronization",
            value=st.session_state.integration_settings.get('auto_sync', False)
        )
        
        sync_frequency = st.selectbox(
            "Sync Frequency",
            ["Real-time", "Hourly", "Daily", "Weekly"],
            index=2
        )
        
        include_historical = st.checkbox("Include Historical Data (12 months)", value=True)
    
    with col2:
        selected_functions = st.multiselect(
            "Functions to Sync",
            configured_functions,
            default=configured_functions
        )
        
        data_validation = st.checkbox("Enable Data Validation", value=True)
        error_handling = st.selectbox("Error Handling", ["Log and Continue", "Stop on Error"], index=0)
    
    # Manual synchronization
    st.markdown("#### Manual Synchronization")
    
    if selected_functions:
        selected_function = st.selectbox("Select Function for Manual Sync", selected_functions)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Sync Financial Data", disabled=not erp_system):
                if erp_system:
                    with st.spinner(f"Syncing financial data from {erp_system}..."):
                        sync_result = integration_manager.sync_department_data(
                            selected_function, erp_system=erp_system
                        )
                        
                        if sync_result['financial_data']:
                            # Update baseline data with synced financial information
                            if selected_function in st.session_state.baseline_data:
                                baseline = st.session_state.baseline_data[selected_function]
                                baseline['revenue'] = sync_result['financial_data'].get('annual_revenue', baseline.get('revenue', 0))
                                baseline['costs'] = sync_result['financial_data'].get('annual_costs', baseline.get('costs', 0))
                                
                            st.success("Financial data synchronized successfully!")
                            st.json(sync_result['financial_data'])
                        
                        if sync_result['errors']:
                            for error in sync_result['errors']:
                                st.error(error)
                else:
                    st.warning("No ERP system configured")
        
        with col2:
            if st.button("👥 Sync Workforce Data", disabled=not hrm_system):
                if hrm_system:
                    with st.spinner(f"Syncing workforce data from {hrm_system}..."):
                        sync_result = integration_manager.sync_department_data(
                            selected_function, hrm_system=hrm_system
                        )
                        
                        if sync_result['workforce_data']:
                            # Update baseline data with synced workforce information
                            if selected_function in st.session_state.baseline_data:
                                baseline = st.session_state.baseline_data[selected_function]
                                baseline['headcount'] = sync_result['workforce_data'].get('headcount', baseline.get('headcount', 0))
                                baseline['productivity'] = sync_result['workforce_data'].get('productivity_index', baseline.get('productivity', 75))
                                baseline['satisfaction'] = sync_result['workforce_data'].get('satisfaction_score', baseline.get('satisfaction', 80))
                                
                            st.success("Workforce data synchronized successfully!")
                            st.json(sync_result['workforce_data'])
                        
                        if sync_result['errors']:
                            for error in sync_result['errors']:
                                st.error(error)
                else:
                    st.warning("No HRM system configured")
        
        with col3:
            if st.button("🔄 Sync All Data"):
                if erp_system or hrm_system:
                    with st.spinner("Syncing all data..."):
                        sync_result = integration_manager.sync_department_data(
                            selected_function, 
                            erp_system=erp_system,
                            hrm_system=hrm_system
                        )
                        
                        # Update baseline data
                        if selected_function in st.session_state.baseline_data:
                            baseline = st.session_state.baseline_data[selected_function]
                            
                            if sync_result['financial_data']:
                                baseline['revenue'] = sync_result['financial_data'].get('annual_revenue', baseline.get('revenue', 0))
                                baseline['costs'] = sync_result['financial_data'].get('annual_costs', baseline.get('costs', 0))
                            
                            if sync_result['workforce_data']:
                                baseline['headcount'] = sync_result['workforce_data'].get('headcount', baseline.get('headcount', 0))
                                baseline['productivity'] = sync_result['workforce_data'].get('productivity_index', baseline.get('productivity', 75))
                                baseline['satisfaction'] = sync_result['workforce_data'].get('satisfaction_score', baseline.get('satisfaction', 80))
                        
                        st.success("All data synchronized successfully!")
                        
                        # Update last sync time
                        st.session_state.integration_settings['last_sync'] = datetime.now().isoformat()
                        
                        if sync_result['errors']:
                            st.warning("Some errors occurred during synchronization:")
                            for error in sync_result['errors']:
                                st.error(error)
                else:
                    st.warning("No enterprise systems configured")
    
    # Bulk synchronization
    st.markdown("#### Bulk Synchronization")
    
    if st.button("🚀 Sync All Functions", type="primary"):
        if erp_system or hrm_system:
            sync_results = []
            progress_bar = st.progress(0)
            
            for i, function in enumerate(selected_functions):
                progress_bar.progress((i + 1) / len(selected_functions))
                
                with st.spinner(f"Syncing {function}..."):
                    sync_result = integration_manager.sync_department_data(
                        function,
                        erp_system=erp_system,
                        hrm_system=hrm_system
                    )
                    sync_results.append(sync_result)
                    
                    # Update baseline data
                    if function in st.session_state.baseline_data:
                        baseline = st.session_state.baseline_data[function]
                        
                        if sync_result['financial_data']:
                            baseline['revenue'] = sync_result['financial_data'].get('annual_revenue', baseline.get('revenue', 0))
                            baseline['costs'] = sync_result['financial_data'].get('annual_costs', baseline.get('costs', 0))
                        
                        if sync_result['workforce_data']:
                            baseline['headcount'] = sync_result['workforce_data'].get('headcount', baseline.get('headcount', 0))
                            baseline['productivity'] = sync_result['workforce_data'].get('productivity_index', baseline.get('productivity', 75))
                            baseline['satisfaction'] = sync_result['workforce_data'].get('satisfaction_score', baseline.get('satisfaction', 80))
            
            progress_bar.progress(1.0)
            st.success(f"Bulk synchronization completed for {len(selected_functions)} functions!")
            
            # Update last sync time
            st.session_state.integration_settings['last_sync'] = datetime.now().isoformat()
            st.session_state.integration_settings['auto_sync'] = auto_sync
        else:
            st.warning("No enterprise systems configured")

def show_integration_status(integration_manager):
    """Show integration status and monitoring"""
    
    st.subheader("📊 Integration Status")
    
    # System status overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        erp_system = st.session_state.integration_settings.get('erp_system')
        erp_status = "✅ Connected" if erp_system else "❌ Not Connected"
        st.metric("ERP System", erp_status)
        if erp_system:
            st.caption(f"System: {erp_system}")
    
    with col2:
        hrm_system = st.session_state.integration_settings.get('hrm_system')
        hrm_status = "✅ Connected" if hrm_system else "❌ Not Connected"
        st.metric("HRM System", hrm_status)
        if hrm_system:
            st.caption(f"System: {hrm_system}")
    
    with col3:
        last_sync = st.session_state.integration_settings.get('last_sync')
        if last_sync:
            sync_time = datetime.fromisoformat(last_sync)
            st.metric("Last Sync", sync_time.strftime("%Y-%m-%d %H:%M"))
        else:
            st.metric("Last Sync", "Never")
    
    with col4:
        auto_sync = st.session_state.integration_settings.get('auto_sync', False)
        sync_status = "🔄 Enabled" if auto_sync else "⏸️ Manual"
        st.metric("Auto Sync", sync_status)
    
    # Data quality metrics
    st.markdown("#### Data Quality Metrics")
    
    if st.session_state.baseline_data:
        quality_data = []
        
        for function_name, baseline in st.session_state.baseline_data.items():
            completeness = calculate_data_completeness(baseline)
            freshness = calculate_data_freshness(baseline)
            
            quality_data.append({
                'Function': function_name,
                'Data Completeness': f"{completeness:.1f}%",
                'Data Freshness': freshness,
                'Revenue': f"${baseline.get('revenue', 0):,.0f}",
                'Headcount': baseline.get('headcount', 0),
                'Last Updated': baseline.get('last_updated', 'Unknown')
            })
        
        if quality_data:
            quality_df = pd.DataFrame(quality_data)
            st.dataframe(quality_df, use_container_width=True)
    else:
        st.info("No function data available for quality assessment.")
    
    # Integration logs
    st.markdown("#### Integration Activity Log")
    
    # Simulated activity log
    if 'integration_logs' not in st.session_state:
        st.session_state.integration_logs = []
    
    if st.session_state.integration_logs:
        log_df = pd.DataFrame(st.session_state.integration_logs)
        st.dataframe(log_df, use_container_width=True)
    else:
        st.info("No integration activity recorded yet.")
    
    # System health checks
    st.markdown("#### System Health Checks")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Test All Connections"):
            if erp_system:
                with st.spinner(f"Testing {erp_system} connection..."):
                    erp_test = integration_manager.test_connection('ERP', erp_system)
                    if erp_test['success']:
                        st.success(f"✅ {erp_system} connection successful")
                    else:
                        st.error(f"❌ {erp_system} connection failed: {erp_test['error']}")
            
            if hrm_system:
                with st.spinner(f"Testing {hrm_system} connection..."):
                    hrm_test = integration_manager.test_connection('HRM', hrm_system)
                    if hrm_test['success']:
                        st.success(f"✅ {hrm_system} connection successful")
                    else:
                        st.error(f"❌ {hrm_system} connection failed: {hrm_test['error']}")
            
            if not erp_system and not hrm_system:
                st.warning("No systems configured to test")
    
    with col2:
        if st.button("📊 Generate Integration Report"):
            report_data = {
                'erp_system': erp_system,
                'hrm_system': hrm_system,
                'last_sync': last_sync,
                'auto_sync_enabled': auto_sync,
                'configured_functions': len(st.session_state.baseline_data),
                'report_generated': datetime.now().isoformat()
            }
            
            import json
            report_json = json.dumps(report_data, indent=2)
            
            st.download_button(
                label="Download Integration Report",
                data=report_json,
                file_name=f"integration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def calculate_data_completeness(baseline_data: dict) -> float:
    """Calculate data completeness percentage"""
    required_fields = ['revenue', 'costs', 'headcount', 'productivity', 'satisfaction']
    completed_fields = sum(1 for field in required_fields if baseline_data.get(field) is not None)
    return (completed_fields / len(required_fields)) * 100

def calculate_data_freshness(baseline_data: dict) -> str:
    """Calculate data freshness indicator"""
    last_updated = baseline_data.get('last_updated')
    if not last_updated:
        return "Unknown"
    
    try:
        update_time = datetime.fromisoformat(last_updated)
        time_diff = datetime.now() - update_time
        
        if time_diff.days == 0:
            return "Fresh (Today)"
        elif time_diff.days <= 7:
            return f"Recent ({time_diff.days} days ago)"
        elif time_diff.days <= 30:
            return f"Moderate ({time_diff.days} days ago)"
        else:
            return f"Stale ({time_diff.days} days ago)"
    except:
        return "Unknown"