"""Database smoke tests."""

import os
import tempfile
from datetime import datetime
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.models import User, Query, Product, Offer, Review, Ranking


@pytest.fixture
def temp_db():
    """Create a temporary SQLite database for testing."""
    # Create a temporary file for the database
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Create engine and session
    engine = create_engine(f"sqlite:///{path}", echo=False)
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    yield session
    
    # Cleanup
    session.close()
    os.unlink(path)


def test_models_import():
    """Test that all models can be imported without errors."""
    from app.db.models import User, Query, Product, Offer, Review, Ranking
    assert User is not None
    assert Query is not None
    assert Product is not None
    assert Offer is not None
    assert Review is not None
    assert Ranking is not None


def test_user_model(temp_db):
    """Test User model creation and retrieval."""
    session = temp_db
    
    # Create a user
    user = User(
        email="test@example.com",
        plan="free"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Verify user was created
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.plan == "free"
    assert user.created_at is not None
    
    # Retrieve user
    retrieved_user = session.query(User).filter(User.email == "test@example.com").first()
    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"


def test_product_model(temp_db):
    """Test Product model creation and retrieval."""
    session = temp_db
    
    # Create a product
    product = Product(
        asin="B08N5WRWNW",
        title="Test Headphones",
        brand="TestBrand",
        category="Electronics"
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    
    # Verify product was created
    assert product.id is not None
    assert product.asin == "B08N5WRWNW"
    assert product.title == "Test Headphones"
    assert product.brand == "TestBrand"
    assert product.category == "Electronics"
    assert product.created_at is not None


def test_query_model(temp_db):
    """Test Query model creation and relationships."""
    session = temp_db
    
    # Create a user first
    user = User(email="test@example.com", plan="free")
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Create a query
    query = Query(
        user_id=user.id,
        raw_text="Best wireless headphones under $200",
        budget_min=Decimal("50.00"),
        budget_max=Decimal("200.00"),
        usage="gaming"
    )
    session.add(query)
    session.commit()
    session.refresh(query)
    
    # Verify query was created
    assert query.id is not None
    assert query.user_id == user.id
    assert query.raw_text == "Best wireless headphones under $200"
    assert query.budget_min == Decimal("50.00")
    assert query.budget_max == Decimal("200.00")
    assert query.usage == "gaming"
    assert query.created_at is not None


def test_offer_model(temp_db):
    """Test Offer model creation and relationships."""
    session = temp_db
    
    # Create a product first
    product = Product(
        asin="B08N5WRWNW",
        title="Test Headphones",
        brand="TestBrand"
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    
    # Create an offer
    offer = Offer(
        product_id=product.id,
        price_cents=19999,  # $199.99
        currency="USD",
        availability="In Stock"
    )
    session.add(offer)
    session.commit()
    session.refresh(offer)
    
    # Verify offer was created
    assert offer.id is not None
    assert offer.product_id == product.id
    assert offer.price_cents == 19999
    assert offer.currency == "USD"
    assert offer.availability == "In Stock"
    assert offer.last_checked_at is not None


def test_review_model(temp_db):
    """Test Review model creation and relationships."""
    session = temp_db
    
    # Create a product first
    product = Product(
        asin="B08N5WRWNW",
        title="Test Headphones",
        brand="TestBrand"
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    
    # Create a review
    review = Review(
        product_id=product.id,
        source="Amazon",
        url="https://amazon.com/review/123",
        snippet="Great sound quality and comfort"
    )
    session.add(review)
    session.commit()
    session.refresh(review)
    
    # Verify review was created
    assert review.id is not None
    assert review.product_id == product.id
    assert review.source == "Amazon"
    assert review.url == "https://amazon.com/review/123"
    assert review.snippet == "Great sound quality and comfort"
    assert review.created_at is not None


def test_ranking_model(temp_db):
    """Test Ranking model creation and relationships."""
    session = temp_db
    
    # Create a user and query
    user = User(email="test@example.com", plan="free")
    session.add(user)
    session.commit()
    session.refresh(user)
    
    query = Query(
        user_id=user.id,
        raw_text="Best wireless headphones under $200"
    )
    session.add(query)
    session.commit()
    session.refresh(query)
    
    # Create a product
    product = Product(
        asin="B08N5WRWNW",
        title="Test Headphones",
        brand="TestBrand"
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    
    # Create a ranking
    ranking = Ranking(
        query_id=query.id,
        product_id=product.id,
        score=Decimal("8.5"),
        rationale="Excellent sound quality and good value for money"
    )
    session.add(ranking)
    session.commit()
    session.refresh(ranking)
    
    # Verify ranking was created
    assert ranking.id is not None
    assert ranking.query_id == query.id
    assert ranking.product_id == product.id
    assert ranking.score == Decimal("8.5")
    assert ranking.rationale == "Excellent sound quality and good value for money"
    assert ranking.created_at is not None


def test_relationships(temp_db):
    """Test model relationships work correctly."""
    session = temp_db
    
    # Create user
    user = User(email="test@example.com", plan="free")
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Create query
    query = Query(
        user_id=user.id,
        raw_text="Best wireless headphones under $200"
    )
    session.add(query)
    session.commit()
    session.refresh(query)
    
    # Create product
    product = Product(
        asin="B08N5WRWNW",
        title="Test Headphones",
        brand="TestBrand"
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    
    # Create offer
    offer = Offer(
        product_id=product.id,
        price_cents=19999,
        currency="USD"
    )
    session.add(offer)
    session.commit()
    
    # Create review
    review = Review(
        product_id=product.id,
        source="Amazon",
        snippet="Great headphones"
    )
    session.add(review)
    session.commit()
    
    # Create ranking
    ranking = Ranking(
        query_id=query.id,
        product_id=product.id,
        score=Decimal("8.5")
    )
    session.add(ranking)
    session.commit()
    
    # Test relationships
    # User -> queries
    assert len(user.queries) == 1
    assert user.queries[0].id == query.id
    
    # Query -> rankings
    assert len(query.rankings) == 1
    assert query.rankings[0].id == ranking.id
    
    # Product -> offers
    assert len(product.offers) == 1
    assert product.offers[0].id == offer.id
    
    # Product -> reviews
    assert len(product.reviews) == 1
    assert product.reviews[0].id == review.id
    
    # Product -> rankings
    assert len(product.rankings) == 1
    assert product.rankings[0].id == ranking.id
