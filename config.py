"""
Configuration module for environment variables and API keys.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys - must be set in environment variables
DEFAULT_GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEFAULT_FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# Real estate websites
AVAILABLE_WEBSITES = ["Zillow", "Realtor.com", "Trulia", "Homes.com"]
DEFAULT_WEBSITES = ["Zillow", "Realtor.com"]
