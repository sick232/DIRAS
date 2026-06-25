"""
Database configuration and session management
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import logging
import os
from src.shared.config import settings

logger = logging.getLogger(__name__)

# Try to create PostgreSQL engine, fallback to SQLite if not available
try:
    # Create database engine
    engine = create_engine(
        settings.database_url,
        echo=settings.database_echo,
        pool_pre_ping=True,  # Verify connections before using
    )
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("✓ PostgreSQL engine created")
except Exception as e:
    logger.warning(f"⚠ PostgreSQL not available: {e}")
    logger.info("Falling back to SQLite for development")
    
    # Create SQLite fallback
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        "sqlite:///data/diras.db",
        echo=settings.database_echo,
        connect_args={"check_same_thread": False}
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Import models to register them with Base
# This MUST happen after Base is defined but before init_db() is called
from src.models.document import Document, DocumentChunk, Embedding, IndexingLog  # noqa: E402, F401

def get_db() -> Session:
    """
    Dependency for getting database session
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database (create tables)"""
    global engine, SessionLocal
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        if engine.url.drivername.startswith("postgres"):
            logger.warning("Falling back to SQLite because PostgreSQL initialization failed")
            os.makedirs("data", exist_ok=True)
            engine.dispose()
            engine = create_engine(
                "sqlite:///data/diras.db",
                echo=settings.database_echo,
                connect_args={"check_same_thread": False}
            )
            SessionLocal.configure(bind=engine)
            Base.metadata.create_all(bind=engine)
            logger.info("Database initialized successfully with SQLite fallback")
            return
        raise

def drop_db():
    """Drop all tables (USE WITH CAUTION)"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped")
    except Exception as e:
        logger.error(f"Failed to drop database tables: {e}")
        raise

def test_db_connection():
    """Test database connection"""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        logger.info("Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
