"""
Basic tests for SttarkelTool backend.
Tests main application functionality and endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Welcome to SttarkelTool Backend"


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "services" in data


def test_get_companies():
    """Test getting company list."""
    response = client.get("/company/list")
    assert response.status_code == 200
    data = response.json()
    assert "companies" in data
    assert "total" in data
    assert len(data["companies"]) > 0


def test_get_company_details():
    """Test getting company details."""
    response = client.get("/company/google")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "google"
    assert data["name"] == "Google"


def test_get_company_not_found():
    """Test getting non-existent company."""
    response = client.get("/company/nonexistent")
    assert response.status_code == 404


def test_get_interview_personas():
    """Test getting interview personas."""
    response = client.get("/interview/personas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "id" in data[0]
    assert "name" in data[0]


def test_get_mcq_categories():
    """Test getting MCQ categories."""
    response = client.get("/assessment/categories/mcq")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert len(data["categories"]) > 0


def test_get_coding_languages():
    """Test getting supported coding languages."""
    response = client.get("/assessment/languages/coding")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    assert len(data["languages"]) > 0


def test_search_companies():
    """Test company search functionality."""
    response = client.get("/company/search?query=google")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "results" in data
    assert len(data["results"]) > 0


def test_search_companies_with_filters():
    """Test company search with filters."""
    response = client.get("/company/search?query=tech&industry=Technology")
    assert response.status_code == 200
    data = response.json()
    assert "filters" in data
    assert data["filters"]["industry"] == "Technology"


if __name__ == "__main__":
    pytest.main([__file__]) 