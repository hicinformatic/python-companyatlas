"""Tests for CompanyAtlas client."""

import pytest
from python_companyatlas import CompanyAtlas


def test_companyatlas_init():
    """Test CompanyAtlas initialization."""
    atlas = CompanyAtlas()
    assert atlas.api_key is None
    assert atlas.config == {}


def test_companyatlas_init_with_api_key():
    """Test CompanyAtlas initialization with API key."""
    atlas = CompanyAtlas(api_key="test_key")
    assert atlas.api_key == "test_key"


def test_lookup_basic():
    """Test basic company lookup."""
    atlas = CompanyAtlas()
    result = atlas.lookup("example.com")
    
    assert isinstance(result, dict)
    assert result["domain"] == "example.com"
    assert "name" in result


def test_lookup_invalid_domain():
    """Test lookup with invalid domain."""
    atlas = CompanyAtlas()
    
    with pytest.raises(ValueError, match="Domain must be a non-empty string"):
        atlas.lookup("")
    
    with pytest.raises(ValueError):
        atlas.lookup(None)


def test_enrich():
    """Test company data enrichment."""
    atlas = CompanyAtlas()
    company_data = {"domain": "example.com", "name": "Example Corp"}
    
    enriched = atlas.enrich(company_data)
    
    assert enriched["domain"] == "example.com"
    assert enriched["name"] == "Example Corp"
    assert enriched["enriched"] is True

