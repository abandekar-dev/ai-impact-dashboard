# AI Strategic Workforce Modeling Platform

## Overview

This is an advanced AI-powered strategic workforce modeling platform built with Python and Streamlit. The application transforms enterprise talent management by providing predictive analytics, scenario modeling, and comprehensive workforce transformation analysis. It enables C-level executives to make data-driven decisions about AI implementation across enterprise functions.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for web application interface
- **UI Components**: Professional dashboard with multiple analysis pages
- **Visualization**: Plotly for interactive charts and graphs
- **Responsive Design**: Multi-column layouts with tabbed interfaces

### Backend Architecture
- **Language**: Python 3.11
- **Web Framework**: Streamlit application server
- **Database**: PostgreSQL 16 with pgvector extension for vector operations
- **ORM**: SQLAlchemy for database operations
- **ML Framework**: scikit-learn for predictive modeling

### Data Storage Solutions
- **Primary Database**: PostgreSQL with vector extension for semantic search
- **Session Management**: Streamlit's built-in session state
- **Data Models**: SQLAlchemy declarative models for enterprise functions, AI initiatives, and predictions

## Key Components

### Core Application Files
- `app.py`: Main comprehensive application with full feature set
- `app_minimal.py`: Simplified version for lightweight deployment
- `utils/`: Extensive utility modules for specialized functionality

### Data Management
- **Database Manager**: PostgreSQL connection and operations
- **Session Manager**: Analysis session persistence
- **Category Manager**: Enterprise function categorization by industry

### Analytics Engine
- **Predictive Engine**: Multi-algorithm ensemble for ROI prediction
- **Monte Carlo Simulator**: Risk analysis and scenario modeling
- **Benchmarking**: Industry comparison and sensitivity analysis

### AI Integration
- **Natural Language Processor**: OpenAI integration for initiative configuration
- **AI Assistant**: Conversational interface for dashboard queries
- **Vector Database**: Semantic search and analysis capabilities

### Visualization & Reporting
- **Dashboard Visualizer**: Interactive charts and metrics
- **Report Generator**: Executive summary generation
- **Chart Styling**: Professional theming and color schemes

### Advanced Features
- **Workforce Analytics**: Comprehensive transformation analysis
- **Learning Personas**: Dynamic curriculum generation
- **Enterprise Integrations**: ERP and HRM system connections
- **Strategic Scenarios**: Business value scenario planning

## Data Flow

1. **Input Collection**: Enterprise function baseline data through industry-specific forms
2. **AI Initiative Configuration**: Natural language processing or structured input
3. **Predictive Analysis**: Multi-algorithm ensemble generates predictions
4. **Risk Assessment**: Monte Carlo simulation for uncertainty analysis
5. **Visualization**: Interactive dashboards and executive reports
6. **Session Persistence**: Save/load analysis configurations

## External Dependencies

### Required Services
- **OpenAI API**: Natural language processing and AI assistant functionality
- **PostgreSQL**: Primary data storage with vector extension support

### Python Packages
- `streamlit>=1.46.0`: Web application framework
- `plotly>=6.1.2`: Interactive visualization library
- `pandas>=2.3.0`: Data manipulation and analysis
- `numpy>=2.3.0`: Numerical computing
- `scikit-learn>=1.7.0`: Machine learning algorithms
- `sqlalchemy>=2.0.41`: Database ORM
- `psycopg2-binary>=2.9.10`: PostgreSQL adapter
- `openai>=1.88.0`: OpenAI API client
- `anthropic>=0.54.0`: Anthropic API client

## Deployment Strategy

### Platform Configuration
- **Environment**: Replit with Python 3.11 and PostgreSQL 16 modules
- **Deployment Target**: Autoscale configuration
- **Port Configuration**: Internal port 5000, external port 80
- **Run Command**: `streamlit run app.py --server.port 5000`

### Workflow Configuration
- **Primary Workflow**: Runs the full application (`app.py`)
- **Minimal Workflow**: Runs simplified version (`app_minimal.py`)
- **Development Mode**: Parallel execution support

### Environment Requirements
- Nix packages: gcc-unwrapped, glibcLocales, libstdcxx5
- Environment variables for API keys (OpenAI, database credentials)

## Changelog

Changelog:
- June 19, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.