# Enterprise AI Impact Simulator

## Overview

This is the Enterprise AI Impact Simulator, built with Streamlit that helps C-level executives analyze and predict the business impact of AI implementation across enterprise functions. The application provides data-driven insights for strategic AI investment decisions through interactive visualizations, predictive modeling, and scenario analysis.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with multi-page architecture
- **Visualization**: Plotly for interactive charts and dashboards
- **UI Components**: Professional dashboard interface with tabs and columns
- **Styling**: Custom chart theming with modern color palettes

### Backend Architecture
- **Core Engine**: Python-based predictive analytics engine
- **Machine Learning**: Scikit-learn ensemble models (Random Forest, Gradient Boosting, Neural Networks)
- **Data Processing**: Pandas and NumPy for data manipulation and analysis
- **Database Layer**: SQLAlchemy ORM with PostgreSQL backend

### Data Storage Solutions
- **Primary Database**: PostgreSQL for persistent data storage
- **Session Management**: Streamlit's built-in session state for temporary data
- **Data Models**: SQLAlchemy models for enterprise functions, AI initiatives, and predictions

## Key Components

### 1. Predictive Engine (`utils/predictive_engine.py`)
- **Purpose**: Advanced ensemble machine learning for AI impact prediction
- **Features**: Multiple ML algorithms, uncertainty quantification, time series forecasting
- **Components**: EnsemblePredictor, MetricsCalculator, TimeSeriesGenerator

### 2. Data Models (`utils/data_models.py`)
- **Purpose**: Structured data representations for enterprise functions and AI initiatives
- **Components**: EnterpriseFunction, AIInitiative dataclasses with validation

### 3. Visualization System (`utils/visualization.py`)
- **Purpose**: Professional dashboard visualizations and charts
- **Features**: Interactive Plotly charts, radar charts, financial projections

### 4. Monte Carlo Simulation (`utils/monte_carlo.py`)
- **Purpose**: Multi-scenario analysis with uncertainty modeling
- **Features**: Risk assessment, sensitivity analysis, scenario optimization

### 5. Database Management (`utils/database.py`)
- **Purpose**: Data persistence and session management
- **Features**: PostgreSQL integration, data migration, backup functionality

### 6. Enterprise Integrations (`utils/enterprise_integrations.py`)
- **Purpose**: Connect to ERP and HRM systems for data synchronization
- **Supported Systems**: SAP, Oracle, Microsoft Dynamics, Workday, NetSuite, Salesforce

### 7. AI Assistant (`utils/ai_assistant.py`)
- **Purpose**: Conversational AI for dashboard analysis
- **Features**: OpenAI GPT-4o integration, context-aware responses

## Data Flow

1. **Input Collection**: Users configure enterprise functions, AI initiatives, and constraints
2. **Data Processing**: Predictive engine analyzes inputs using ML models
3. **Scenario Generation**: Monte Carlo simulation creates multiple outcome scenarios
4. **Visualization**: Results displayed through interactive dashboards
5. **Integration**: Optional sync with enterprise systems for real-time data
6. **Reporting**: Executive summaries and strategic recommendations generated

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualizations
- **scikit-learn**: Machine learning algorithms
- **sqlalchemy**: Database ORM
- **psycopg2-binary**: PostgreSQL adapter

### AI/ML Services
- **openai**: GPT-4o API for conversational AI
- **anthropic**: Alternative AI provider (configured but not primary)

### Data Processing
- **trafilatura**: Web scraping and content extraction

## Deployment Strategy

### Platform
- **Primary**: Replit autoscale deployment
- **Port Configuration**: Application runs on port 5000, exposed on port 80
- **Environment**: Python 3.11 with PostgreSQL 16

### Configuration Files
- **`.replit`**: Deployment and workflow configuration
- **`pyproject.toml`**: Python project dependencies
- **`.streamlit/config.toml`**: Streamlit server configuration

### Workflows
- **Development**: Parallel workflow execution
- **Production**: Streamlit server with automatic port binding

## Changelog

- June 23, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.