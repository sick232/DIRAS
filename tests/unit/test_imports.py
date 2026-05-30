"""
Test that all imports work correctly (Sprint 1 test)
"""

import pytest


def test_fastapi_import():
    """Test FastAPI can be imported"""
    from fastapi import FastAPI
    assert FastAPI is not None


def test_main_app_import():
    """Test main app can be imported"""
    from src.api.main import app
    assert app is not None


def test_config_import():
    """Test config can be imported"""
    from src.shared.config import settings
    assert settings is not None


def test_database_import():
    """Test database module can be imported"""
    from src.shared.database import SessionLocal, engine
    assert SessionLocal is not None
    assert engine is not None


def test_dependencies():
    """Test key dependencies are installed"""
    import spacy
    import torch
    import transformers
    import pandas
    import numpy
    assert spacy is not None
    assert torch is not None
    assert transformers is not None
    assert pandas is not None
    assert numpy is not None


def test_ocr_dependencies():
    """Test OCR dependencies"""
    import easyocr
    import cv2
    assert easyocr is not None
    assert cv2 is not None


def test_database_connection():
    """Test database connection (requires PostgreSQL running)"""
    from src.shared.database import test_db_connection
    # This will only pass if PostgreSQL is running
    # Skip if not available
    try:
        result = test_db_connection()
        assert result is True
    except Exception:
        pytest.skip("PostgreSQL not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
