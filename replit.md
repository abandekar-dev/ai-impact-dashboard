# AI-Powered Strategic Modeling Platform

## Overview

This is a comprehensive AI-powered strategic modeling platform built with Streamlit, designed to help enterprise executives analyze, predict, and optimize AI implementation strategies across their organizations. The platform provides advanced analytics, predictive modeling, and strategic planning capabilities to support data-driven decision-making for AI transformation initiatives.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with multi-page architecture
- **UI Components**: Interactive dashboards, charts (Plotly), data input forms, and conversational AI interface
- **Page Structure**: Modular page-based architecture with dedicated sections for different analysis types
- **Styling**: Custom chart theming with professional color palettes and modern UI components

### Backend Architecture
- **Core Engine**: Python-based analytical engine with multiple specialized modules
- **Data Processing**: Pandas and NumPy for data manipulation and analysis
- **Machine Learning**: Scikit-learn ensemble models for predictive analytics
- **Statistical Analysis**: Monte Carlo simulations and advanced statistical modeling

### Data Storage Solutions
- **Primary Database**: PostgreSQL with SQLAlchemy ORM
- **Vector Database**: pgvector extension for semantic search and analysis
- **Session Management**: Streamlit's built-in session state with database persistence
- **Data Models**: Structured data models for enterprise functions and AI initiatives

### AI/ML Components
- **Predictive Engine**: Multi-algorithm ensemble predictor with cross-validation
- **Natural Language Processing**: OpenAI GPT integration for conversational AI and text analysis
- **Monte Carlo Simulation**: Statistical modeling for risk assessment and outcome distribution
- **Anthropic Integration**: Secondary AI provider for enhanced analysis capabilities

## Key Components

### Core Analytics Modules
1. **Predictive Engine** (`utils/predictive_engine.py`): Advanced ML models for ROI prediction and impact analysis
2. **Monte Carlo Simulator** (`utils/monte_carlo.py`): Risk modeling and scenario analysis
3. **Workforce Analytics** (`utils/workforce_analytics.py`): Comprehensive workforce transformation analysis
4. **Strategic Scenarios** (`utils/strategic_scenarios.py`): Business value scenario planning

### Data Management
1. **Database Manager** (`utils/database.py`): PostgreSQL connection and data persistence
2. **Session Manager** (`utils/session_manager.py`): Analysis session management and state persistence
3. **Category Manager** (`utils/category_manager.py`): Industry-specific function and initiative management

### Visualization & Reporting
1. **Dashboard Visualizer** (`utils/visualization.py`): Interactive chart and dashboard generation
2. **Chart Styling** (`utils/chart_styling.py`): Professional theming and visual components
3. **Report Generator** (`utils/report_generator.py`): Executive summary and report generation

### AI & Integration
1. **AI Assistant** (`utils/ai_assistant.py`): Conversational AI for strategic analysis
2. **Natural Language Processor** (`utils/natural_language_processor.py`): Text analysis and initiative parsing
3. **Enterprise Integrations** (`utils/enterprise_integrations.py`): ERP and HRM system connectivity

## Data Flow

1. **Data Input**: Users configure enterprise functions, AI initiatives, and strategic parameters through interactive forms
2. **Processing**: Core engines analyze data using ML models, statistical simulations, and industry benchmarks
3. **Prediction**: Predictive models generate ROI forecasts, workforce impact, and performance metrics
4. **Visualization**: Results are presented through interactive dashboards and executive summaries
5. **Persistence**: All analysis data is stored in PostgreSQL with session management for continuity

## External Dependencies

### AI/ML Services
- **OpenAI API**: GPT models for conversational AI and natural language processing
- **Anthropic API**: Claude integration for enhanced AI analysis capabilities

### Data Visualization
- **Plotly**: Interactive charts and sophisticated data visualizations
- **Matplotlib**: Additional charting capabilities and diagram generation

### Database & Storage
- **PostgreSQL**: Primary database with pgvector extension for semantic search
- **SQLAlchemy**: Object-relational mapping and database abstraction

### Scientific Computing
- **NumPy/Pandas**: Data manipulation and numerical computing
- **Scikit-learn**: Machine learning algorithms and statistical modeling
- **SciPy**: Advanced statistical functions and distributions

## Deployment Strategy

### Platform Configuration
- **Deployment Target**: Autoscale deployment on Replit infrastructure
- **Port Configuration**: Application runs on port 5000 with external port 80 mapping
- **Environment**: Python 3.11 with PostgreSQL 16 backend

### System Requirements
- **Python Packages**: Comprehensive scientific computing and web development stack
- **System Dependencies**: Cairo, FFmpeg, Ghostscript, and GUI libraries for advanced visualization
- **Database**: PostgreSQL with vector extension support

### Workflow Management
- **Run Configuration**: Parallel workflow execution with dedicated AI Dashboard Server task
- **Process Management**: Streamlit server with proper port binding and health checks

## Changelog

- June 20, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.