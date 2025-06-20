# AI-Powered Strategic Modeling Platform

## Overview

This is a comprehensive AI-powered strategic modeling platform built with Streamlit that helps enterprise organizations plan, analyze, and optimize their AI implementation strategies. The platform provides executive-level insights for workforce transformation, ROI analysis, and strategic decision-making across multiple industry verticals.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with multi-page navigation
- **Deployment**: Autoscale deployment target running on port 5000
- **UI Components**: Interactive dashboards with Plotly visualizations, executive summary cards, and conversational AI interface
- **Page Structure**: Modular page system with dedicated sections for different analysis types

### Backend Architecture
- **Core Engine**: Python-based analytics engine with multiple specialized modules
- **Data Processing**: Pandas and NumPy for data manipulation and analysis
- **Machine Learning**: Scikit-learn ensemble models for predictive analytics
- **Monte Carlo Simulation**: Custom simulation engine for risk assessment and scenario modeling

### Key Technologies
- **Python 3.11** as the primary runtime
- **Streamlit** for the web interface
- **Plotly** for interactive data visualizations
- **PostgreSQL 16** for data persistence
- **SQLAlchemy** for database ORM
- **OpenAI/Anthropic APIs** for conversational AI assistance

## Key Components

### 1. Data Models (`utils/data_models.py`)
- **EnterpriseFunction**: Baseline metrics for business functions
- **AIInitiative**: Configuration for AI implementation projects
- **MetricsCalculator**: Financial and performance calculations
- **TimeSeriesGenerator**: Temporal analysis utilities

### 2. Predictive Engine (`utils/predictive_engine.py`)
- **EnsemblePredictor**: Multi-algorithm ML predictor
- **PredictiveEngine**: Main prediction orchestrator
- **Monte Carlo Integration**: Risk-adjusted forecasting
- **Cross-validation**: Model validation and performance assessment

### 3. Visualization System (`utils/visualization.py`)
- **DashboardVisualizer**: Interactive chart generation
- **ChartTheme**: Professional styling and color palettes
- **Executive Dashboards**: C-level summary visualizations

### 4. AI Assistant (`utils/ai_assistant.py`)
- **Conversational Interface**: Natural language interaction
- **Context-Aware Analysis**: Dashboard data integration
- **Executive Recommendations**: Strategic guidance generation

### 5. Industry-Specific Analysis
- **CategoryManager**: Industry-specific function categorization
- **BenchmarkingEngine**: Industry comparative analysis
- **Workforce Analytics**: Transformation planning and skills assessment

## Data Flow

1. **Input Collection**: Enterprise function baselines, AI initiative configurations, budget constraints
2. **Data Processing**: Industry-specific categorization, validation, and normalization
3. **Predictive Analysis**: ML-powered forecasting with Monte Carlo simulation
4. **Visualization**: Interactive dashboard generation with executive summaries
5. **AI Assistance**: Conversational analysis and strategic recommendations
6. **Persistence**: Database storage for session management and historical analysis

## External Dependencies

### AI Services
- **OpenAI GPT-4o**: Conversational AI and natural language processing
- **Anthropic Claude**: Alternative AI assistant backend

### Data Processing
- **Plotly**: Interactive visualization library
- **Pandas/NumPy**: Data manipulation and numerical computing
- **Scikit-learn**: Machine learning algorithms

### Infrastructure
- **PostgreSQL**: Primary database with optional pgvector extension
- **Streamlit**: Web application framework
- **SQLAlchemy**: Database abstraction layer

## Deployment Strategy

### Production Environment
- **Autoscale Deployment**: Automatic scaling based on demand
- **Port Configuration**: External port 80 mapped to internal port 5000
- **Health Monitoring**: Streamlit built-in health checks

### Development Environment
- **Nix Package Management**: Reproducible development environment
- **Hot Reload**: Streamlit auto-refresh during development
- **Local Database**: PostgreSQL 16 for development testing

### Configuration Management
- **Environment Variables**: API keys and database connections
- **Secrets Management**: Streamlit secrets for sensitive configuration
- **Multi-environment Support**: Development, staging, and production configs

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

Changelog:
- June 20, 2025. Initial setup