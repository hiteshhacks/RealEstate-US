"""
Pydantic models for property data exchange and validation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class PropertyDetails(BaseModel):
    """Model for individual property details."""
    address: str = Field(description="Full property address")
    price: Optional[str] = Field(description="Property price")
    bedrooms: Optional[str] = Field(description="Number of bedrooms")
    bathrooms: Optional[str] = Field(description="Number of bathrooms")
    square_feet: Optional[str] = Field(description="Square footage")
    property_type: Optional[str] = Field(description="Type of property")
    description: Optional[str] = Field(description="Property description")
    features: Optional[List[str]] = Field(description="Property features")
    images: Optional[List[str]] = Field(description="Property image URLs")
    agent_contact: Optional[str] = Field(description="Agent contact information")
    listing_url: Optional[str] = Field(description="Original listing URL")


class PropertyListing(BaseModel):
    """Model for a collection of property listings."""
    properties: List[PropertyDetails] = Field(description="List of properties found")
    total_count: int = Field(description="Total number of properties found")
    source_website: str = Field(description="Website where properties were found")
