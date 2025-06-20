# AI Impact Predictive Dashboard

## Overview

The AI Impact Predictive Dashboard is an enterprise-grade Streamlit application designed to help C-level executives analyze and predict the business impact of AI implementations across their organization. The application provides comprehensive analysis tools for evaluating AI initiatives, workforce transformation, and strategic planning across different enterprise functions.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for rapid web application development
- **Visualization**: Plotly for interactive charts and dashboards
- **UI Components**: Multi-page application with tabbed interfaces
- **Responsive Design**: Wide layout configuration optimized for executive dashboards

### Backend Architecture
- **Core Engine**: Modular Python architecture with utility modules
- **Predictive Analytics**: Advanced ML ensemble models using scikit-learn
- **Data Processing**: Pandas and NumPy for data manipulation
- **Session Management**: Streamlit session state for application state persistence

### Database Layer
- **Primary Database**: PostgreSQL 16 for persistent data storage
- **ORM**: SQLAlchemy for database operations
- **Models**: Enterprise functions, AI initiatives, and predictions tracking
- **Fallback**: Session-based storage when database unavailable

## Key Components

### Core Analysis Modules
1. **Predictive Engine** (`utils/predictive_engine.py`)
   - Advanced ensemble ML models for ROI prediction
   - Monte Carlo simulation capabilities
   - Time series analysis and forecasting
   - Handles limited data scenarios with domain knowledge fallbacks

2. **Workforce Analytics** (`utils/workforce_analytics.py`)
   - Comprehensive workforce transformation analysis
   - Human-AI integration architecture design
   - Predictive skill gap analysis and upskilling recommendations

3. **Visualization Engine** (`utils/visualization.py`)
   - Professional chart styling and theming
   - Interactive dashboard visualizations
   - Executive-level summary charts and radar plots

4. **Strategic Planning** (`utils/strategic_scenarios.py`)
   - Business value scenario creation
   - Strategic scenario planning based on real business questions
   - Multi-dimensional scenario comparison

### Data Management
1. **Database Manager** (`utils/database.py`)
   - PostgreSQL integration with SQLAlchemy
   - Session management and data persistence
   - Automated table creation and migration support

2. **Session Manager** (`utils/session_manager.py`)
   - Analysis session saving and loading
   - Cross-session data persistence
   - Database synchronization capabilities

3. **Category Manager** (`utils/category_manager.py`)
   - Industry-specific function categorization
   - Dynamic AI initiative management
   - Pre-configured templates for 9 major industries

### Enterprise Integration
1. **ERP Integration** (`utils/enterprise_integrations.py`)
   - Support for major ERP systems (SAP, Oracle, Microsoft, Workday)
   - Financial data synchronization
   - Automated baseline data population

2. **AI Assistant** (`utils/ai_assistant.py`)
   - Conversational AI interface using OpenAI GPT-4o
   - Context-aware dashboard analysis
   - Executive-level insights and recommendations

## Data Flow

1. **Input Layer**: Enterprise functions and AI initiatives configuration
2. **Processing Layer**: Predictive modeling and scenario analysis
3. **Analytics Layer**: Advanced calculations and benchmarking
4. **Visualization Layer**: Interactive charts and executive summaries
5. **Integration Layer**: External system data synchronization
6. **Persistence Layer**: Database storage and session management

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualization library
- **Pandas/NumPy**: Data manipulation and analysis
- **scikit-learn**: Machine learning algorithms
- **SQLAlchemy**: Database ORM
- **psycopg2-binary**: PostgreSQL adapter

### AI Integration
- **OpenAI**: GPT-4o integration for AI assistant
- **Anthropic**: Alternative AI provider support

### Enterprise Integration
- **requests**: HTTP client for API integrations
- **trafilatura**: Web content extraction for benchmarking

## Deployment Strategy

### Development Environment
- **Platform**: Replit with Python 3.11 runtime
- **Database**: PostgreSQL 16 module
- **Port Configuration**: Service runs on port 5000, external port 80
- **Auto-scaling**: Configured for autoscale deployment target

### Production Considerations
- The application is designed to handle enterprise-scale data
- Database connections include error handling and fallback mechanisms
- Session state management ensures data persistence across user interactions
- Modular architecture supports horizontal scaling

### Configuration
- Environment variables for API keys and database connections
- Streamlit configuration optimized for headless deployment
- Security considerations for enterprise data handling

## Changelog
- June 20, 2025. Initial setup
- June 20, 2025. Resolved dependency installation issues and created simplified dashboard version
- June 20, 2025. Implemented comprehensive compatibility layer for missing libraries
- June 20, 2025. Dashboard fully operational with core AI impact analysis functionality

## Recent Changes
- Fixed system resource limitations preventing dependency installation
- Created simple_dashboard.py with graceful fallback for missing libraries
- All navigation sections working: Overview, Function Analysis, Executive Summary
- ROI calculations and enterprise metrics displaying properly
- Application running successfully on port 5000

## User Preferences

Preferred communication style: Simple, everyday language.