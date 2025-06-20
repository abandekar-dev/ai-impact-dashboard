# AI Impact Predictive Dashboard

## Overview

This repository contains an AI-powered strategic modeling platform designed for enterprise workforce transformation and AI implementation analysis. The platform provides C-level executives with comprehensive analytics, predictive modeling, and strategic planning tools to assess and optimize AI initiatives across enterprise functions.

Built as a Streamlit web application with Python backend, the platform offers sophisticated analytical capabilities including Monte Carlo simulations, workforce analytics, industry benchmarking, and natural language processing for initiative configuration.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **Interface**: Multi-page dashboard with tabbed navigation
- **Visualization**: Plotly for interactive charts and graphs
- **User Experience**: Executive-level interface with conversational AI assistant

### Backend Architecture
- **Language**: Python 3.11
- **ML/Analytics**: scikit-learn, NumPy, pandas for predictive modeling
- **Database**: PostgreSQL 16 with SQLAlchemy ORM
- **Vector Database**: pgvector extension for semantic search capabilities
- **AI Integration**: OpenAI GPT-4 for natural language processing and conversational AI

### Data Management
- **ORM**: SQLAlchemy with declarative base models
- **Session Management**: Streamlit session state with database persistence
- **Data Models**: Structured dataclasses for enterprise functions and AI initiatives
- **Vector Storage**: Embedding-based semantic analysis for AI initiatives

## Key Components

### Core Analytics Engine
- **Predictive Engine**: Advanced ensemble ML models combining Random Forest, Gradient Boosting, and neural networks
- **Monte Carlo Simulator**: 10,000+ iteration risk assessment with uncertainty quantification
- **Metrics Calculator**: Comprehensive ROI, NPV, and payback period calculations
- **Industry Benchmarking**: Comparative analysis against industry standards

### AI Initiative Management
- **Natural Language Processor**: Converts plain English descriptions into structured AI configurations
- **Category Manager**: Manages AI categories and initiatives within enterprise functions
- **Cross-Function Analysis**: Dependencies and impact relationship modeling
- **Strategic Scenario Planner**: Business value scenario generation and optimization

### Workforce Transformation
- **Workforce Analytics**: Comprehensive transformation planning and skill gap analysis
- **Learning Personas**: Dynamic persona generation for AI upskilling programs
- **Human-AI Integration Architecture**: Optimal collaboration model design
- **Experience Optimizer**: Workforce experience enhancement planning

### Visualization & Reporting
- **Dashboard Visualizer**: Professional chart theming with modern color palettes
- **Report Generator**: Executive summary and comprehensive analysis reports
- **Chart Styling**: Responsive visualizations with gradient themes
- **Interactive Charts**: Real-time filtering and drill-down capabilities

## Data Flow

1. **Input Collection**: Enterprise functions, baseline metrics, and AI initiative descriptions
2. **NLP Processing**: Natural language conversion to structured configurations
3. **Predictive Modeling**: ML ensemble predictions with uncertainty quantification
4. **Monte Carlo Simulation**: Risk assessment and outcome distribution analysis
5. **Cross-Function Analysis**: Dependency mapping and optimization
6. **Visualization Generation**: Interactive dashboards and executive reports
7. **Database Persistence**: Session management and historical analysis

## External Dependencies

### Required Services
- **OpenAI API**: GPT-4 for natural language processing and AI assistant
- **PostgreSQL**: Primary database with pgvector extension
- **Anthropic API**: Alternative AI provider integration

### Python Packages
- **streamlit**: Web application framework
- **plotly**: Interactive visualization library
- **scikit-learn**: Machine learning algorithms
- **sqlalchemy**: Database ORM
- **pandas/numpy**: Data manipulation and analysis
- **psycopg2-binary**: PostgreSQL adapter
- **anthropic/openai**: AI service clients

### Optional Integrations
- **Enterprise Systems**: SAP, Oracle, Microsoft Dynamics, Workday, NetSuite, Salesforce
- **Vector Database**: pgvector for semantic search (falls back to similarity matching)

## Deployment Strategy

### Container Configuration
- **Runtime**: Python 3.11 with Nix package management
- **Database**: PostgreSQL 16 integrated container
- **Port Configuration**: Internal 5000 → External 80
- **Deployment Target**: Autoscale infrastructure

### Development Workflow
- **Run Command**: `streamlit run app.py --server.port 5000`
- **Package Management**: uv lock file with dependency resolution
- **Configuration**: Streamlit config with headless mode

### Production Considerations
- Environment variables for API keys and database credentials
- Session state management for multi-user scenarios
- Database connection pooling and error handling
- Responsive design for various screen sizes

## Changelog

- June 19, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.