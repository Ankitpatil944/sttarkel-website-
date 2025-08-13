# SttarkelTool Backend

A comprehensive FastAPI backend for a job preparation web application that handles user assessments (MCQ, coding, aptitude), AI-driven interview simulations using Tavus Conversational Video Interface (CVI), and post-assessment analytics with PDF report generation.

## 🚀 Features

- **Assessment Management**: MCQ, coding, and aptitude assessments with automated scoring
- **AI Interview Sessions**: Integration with Tavus CVI for realistic interview simulations
- **Analytics & Reporting**: Comprehensive performance analytics and PDF report generation
- **User Management**: User profiles and performance tracking
- **Company Data**: Mock company-specific interview data and flows
- **Real-time Feedback**: AI-powered feedback generation for all assessment types

## 🏗️ Architecture

```
sttarkel_backend/
├── app/
│   ├── main.py                      # FastAPI app entry
│   ├── config.py                    # Environment variables & API keys
│   ├── routes/                      # API routes
│   │   ├── auth.py                  # User authentication
│   │   ├── assessment.py            # MCQ, aptitude, coding
│   │   ├── interview_ai.py          # Tavus CVI session management
│   │   ├── dashboard.py             # Analytics and feedback
│   │   └── company.py               # Company-specific data
│   ├── services/                    # Core business logic
│   │   ├── mcq_service.py           # MCQ assessment logic
│   │   ├── coding_service.py        # Code execution & evaluation
│   │   ├── aptitude_service.py      # Aptitude assessment logic
│   │   ├── ai_interview.py          # Tavus API integration
│   │   ├── face_analysis.py         # Face analysis utilities
│   │   └── pdf_report.py            # PDF generation
│   ├── models/                      # SQLAlchemy ORM models
│   ├── db/                          # Database operations
│   ├── schemas/                     # Pydantic validation schemas
│   ├── utils/                       # Utility functions
│   └── middleware/                  # Custom middleware
├── tests/                           # Unit tests
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🛠️ Technology Stack

- **Framework**: FastAPI (async)
- **Database**: SQLAlchemy with SQLite (configurable for PostgreSQL/MySQL)
- **Code Execution**: Judge0 API integration
- **AI Interviews**: Tavus Conversational Video Interface (CVI)
- **PDF Generation**: ReportLab
- **Validation**: Pydantic
- **Testing**: pytest
- **Documentation**: Auto-generated OpenAPI/Swagger

## 📋 Prerequisites

- Python 3.8+
- pip or poetry
- SQLite (or PostgreSQL/MySQL for production)
- Tavus API key (optional, uses mock data if not provided)
- Judge0 API key (optional, uses simulation if not provided)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd sttarkel_backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp env.example .env
```

Edit `.env` with your configuration:

```env
# Required: Database URL
DATABASE_URL=sqlite:///./sttarkel.db

# Optional: API Keys (for production features)
TAVUS_API_KEY=your_tavus_api_key_here
JUDGE0_API_KEY=your_judge0_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Server settings
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### 5. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the main.py
python -m app.main
```

### 6. Access the API

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Assessment Endpoints

- `POST /assessment/mcq` - Submit MCQ assessment
- `POST /assessment/coding` - Submit coding assessment
- `POST /assessment/aptitude` - Submit aptitude assessment
- `GET /assessment/user/{user_id}` - Get user assessments
- `GET /assessment/{assessment_id}` - Get specific assessment

### Interview Endpoints

- `GET /interview/personas` - Get available Tavus personas
- `POST /interview/session` - Create AI interview session
- `GET /interview/session/{session_id}` - Get session status
- `GET /interview/session/{session_id}/transcript` - Get interview transcript
- `POST /interview/session/{session_id}/feedback` - Submit interview feedback

### Dashboard Endpoints

- `GET /dashboard/user/{user_id}` - Get user performance summary
- `GET /dashboard/analytics/{user_id}` - Get detailed analytics
- `POST /dashboard/report/generate` - Generate PDF report
- `GET /dashboard/report/{report_id}` - Download report

### Company Endpoints

- `GET /company/list` - Get list of companies
- `GET /company/{company_id}` - Get company details
- `GET /company/{company_id}/interview-flow` - Get interview flow

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./sttarkel.db` |
| `TAVUS_API_KEY` | Tavus CVI API key | None |
| `JUDGE0_API_KEY` | Judge0 code execution API key | None |
| `DEBUG` | Enable debug mode | `true` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### Database Configuration

The application uses SQLAlchemy with support for multiple databases:

- **SQLite** (default): `sqlite:///./sttarkel.db`
- **PostgreSQL**: `postgresql://user:password@localhost/dbname`
- **MySQL**: `mysql://user:password@localhost/dbname`

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📊 Database Schema

### Core Tables

- **users**: User profiles and information
- **assessments**: Assessment results and metadata
- **interview_sessions**: AI interview session data
- **reports**: Generated PDF reports
- **analytics**: User performance analytics

## 🔒 Security

- CORS middleware configured
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy
- Rate limiting (configurable)
- Environment-based configuration

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Database**: Use PostgreSQL or MySQL for production
2. **API Keys**: Configure all required API keys
3. **HTTPS**: Use reverse proxy (nginx) with SSL
4. **Monitoring**: Enable metrics and logging
5. **Caching**: Configure Redis for caching
6. **Rate Limiting**: Enable rate limiting for API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the test files for usage examples

## 🔄 Development Workflow

1. **Setup**: Follow the Quick Start guide
2. **Development**: Use `uvicorn app.main:app --reload`
3. **Testing**: Run `pytest` before committing
4. **Documentation**: Update README and docstrings
5. **Deployment**: Use Docker or direct deployment

## 📈 Performance

- Async FastAPI for high concurrency
- Database connection pooling
- Caching for frequently accessed data
- Background task processing
- Optimized database queries

## 🔍 Monitoring

- Health check endpoint: `/health`
- Metrics endpoint: `/metrics` (if enabled)
- Structured logging
- Performance monitoring
- Error tracking

---

**SttarkelTool Backend** - Empowering job seekers with AI-driven assessment and interview preparation. 