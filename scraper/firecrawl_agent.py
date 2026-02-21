"""
Direct Firecrawl agent for property search and extraction.
"""
import json
from agno.agent import Agent
from agno.models.google import Gemini
from firecrawl import FirecrawlApp
from schemas import PropertyListing


class DirectFirecrawlAgent:
    """Agent with direct Firecrawl integration for property search"""
    
    def __init__(self, firecrawl_api_key: str, google_api_key: str, model_id: str = "gemini-2.5-flash"):
        """
        Initialize the DirectFirecrawlAgent.
        
        Args:
            firecrawl_api_key: API key for Firecrawl service
            google_api_key: API key for Google Gemini
            model_id: Model identifier for Gemini (default: gemini-2.5-flash)
        """
        self.agent = Agent(
            model=Gemini(id=model_id, api_key=google_api_key),
            markdown=True,
            description="I am a real estate expert who helps find and analyze properties based on user preferences."
        )
        self.firecrawl = FirecrawlApp(api_key=firecrawl_api_key)

    def find_properties_direct(self, city: str, state: str, user_criteria: dict, selected_websites: list) -> dict:
        """
        Direct Firecrawl integration for property search.
        
        Args:
            city: City name for property search
            state: State abbreviation
            user_criteria: Dictionary containing user search criteria
            selected_websites: List of selected real estate websites to search
        
        Returns:
            Dictionary with search results or error information
        """
        city_formatted = city.replace(' ', '-').lower()
        state_upper = state.upper() if state else ''
        
        # Create URLs for selected websites
        state_lower = state.lower() if state else ''
        city_trulia = city.replace(' ', '_')  # Trulia uses underscores for spaces
        search_urls = {
            "Zillow": f"https://www.zillow.com/homes/for_sale/{city_formatted}-{state_upper}/",
            "Realtor.com": f"https://www.realtor.com/realestateandhomes-search/{city_formatted}_{state_upper}/pg-1",
            "Trulia": f"https://www.trulia.com/{state_upper}/{city_trulia}/",
            "Homes.com": f"https://www.homes.com/homes-for-sale/{city_formatted}-{state_lower}/"
        }
        
        # Filter URLs based on selected websites
        urls_to_search = [url for site, url in search_urls.items() if site in selected_websites]
        
        print(f"Selected websites: {selected_websites}")
        print(f"URLs to search: {urls_to_search}")
        
        if not urls_to_search:
            return {"error": "No websites selected"}
        
        # Create comprehensive prompt with specific schema guidance
        prompt = f"""You are extracting property listings from real estate websites. Extract EVERY property listing you can find on the page.

USER SEARCH CRITERIA:
- Budget: {user_criteria.get('budget_range', 'Any')}
- Property Type: {user_criteria.get('property_type', 'Any')}
- Bedrooms: {user_criteria.get('bedrooms', 'Any')}
- Bathrooms: {user_criteria.get('bathrooms', 'Any')}
- Min Square Feet: {user_criteria.get('min_sqft', 'Any')}
- Special Features: {user_criteria.get('special_features', 'Any')}

EXTRACTION INSTRUCTIONS:
Extract property data in this exact JSON format:
{{
  "properties": [
    {{
      "address": "street address",
      "price": "$XX,XXX",
      "bedrooms": "number",
      "bathrooms": "number",
      "square_feet": "sf or Not specified",
      "property_type": "House/Condo/Townhouse/etc",
      "description": "description or Not specified",
      "listing_url": "url or Not specified",
      "agent_contact": "contact or Not specified",
      "features": []
    }}
  ],
  "total_count": "number of properties",
  "source_website": "Zillow/Realtor/Trulia/Homes"
}}

REQUIREMENTS:
- Extract ALL visible property listings (20-40+ per page)
- Include ALL available fields for each property
- For missing fields use "Not specified"
- Ensure address and price are NEVER empty
- Return only valid JSON matching the format above
- Set total_count to actual number of properties extracted
- Do NOT filter or exclude any properties

EXTRACT EVERY VISIBLE PROPERTY - THIS IS CRITICAL!
        """
        
        try:
            # Direct Firecrawl call - using correct API format
            print(f"Calling Firecrawl with {len(urls_to_search)} URLs")
            raw_response = self.firecrawl.extract(
                urls_to_search,
                prompt=prompt,
                schema=PropertyListing.model_json_schema()
            )
            
            print("Raw Firecrawl Response:", raw_response)
            
            if hasattr(raw_response, 'success') and raw_response.success:
                # Handle Firecrawl response object
                properties = raw_response.data.get('properties', []) if hasattr(raw_response, 'data') else []
                total_count = raw_response.data.get('total_count', 0) if hasattr(raw_response, 'data') else 0
                print(f"Response data keys: {list(raw_response.data.keys()) if hasattr(raw_response, 'data') else 'No data'}")
            elif isinstance(raw_response, dict) and raw_response.get('success'):
                # Handle dictionary response
                properties = raw_response['data'].get('properties', [])
                total_count = raw_response['data'].get('total_count', 0)
                print(f"Response data keys: {list(raw_response['data'].keys())}")
            else:
                properties = []
                total_count = 0
                print(f"Response failed or unexpected format: {type(raw_response)}")
            
            print(f"Extracted {len(properties)} properties from {total_count} total found")
            
            # If we found listings but extraction returned empty, try without schema
            if len(properties) == 0 and total_count > 0:
                print("Schema extraction returned empty. Attempting raw extraction...")
                try:
                    # Retry without schema to get raw data
                    raw_response_2 = self.firecrawl.extract(
                        urls_to_search,
                        prompt=f"""Extract EVERY property listing from this page. Return only valid JSON:
{{
  "properties": [list of all visible properties with address, price, bedrooms, bathrooms, square_feet, property_type, description, listing_url, agent_contact],
  "total_count": [actual count],
  "source_website": [Zillow/Realtor/Trulia/Homes]
}}
"""
                    )
                    
                    if hasattr(raw_response_2, 'success') and raw_response_2.success and hasattr(raw_response_2, 'data'):
                        raw_data = raw_response_2.data
                        if isinstance(raw_data, dict):
                            properties = raw_data.get('properties', [])
                            total_count = raw_data.get('total_count', len(properties))
                            print(f"Retry succeeded: Extracted {len(properties)} properties")
                    elif isinstance(raw_response_2, dict) and raw_response_2.get('success'):
                        raw_data = raw_response_2.get('data', {})
                        properties = raw_data.get('properties', [])
                        total_count = raw_data.get('total_count', len(properties))
                        print(f"Retry succeeded: Extracted {len(properties)} properties")
                except Exception as retry_error:
                    print(f"Retry failed: {str(retry_error)}")
            
            # Debug: Print first property if available
            if properties:
                print(f"First property sample: {properties[0]}")
                return {
                    'success': True,
                    'properties': properties,
                    'total_count': len(properties),
                    'source_websites': selected_websites
                }
            else:
                # Enhanced error message with debugging info
                error_msg = f"""No properties extracted despite finding {total_count} listings.
                
POSSIBLE CAUSES:
1. Website structure changed - pages may require JavaScript rendering
2. Website blocking automated requests or showing captcha
3. Dynamic content not being captured properly
4. Firecrawl schema validation too strict for page format

SUGGESTIONS TO TRY:
1. Refresh and try again - temporary website issues
2. Select different websites (Zillow, Realtor.com, Trulia, Homes.com)
3. Use broader search criteria (Any bedrooms, Any type, etc.)
4. Check Internet connection and website availability

DEBUG INFO:
- Total listings detected: {total_count}
- Properties extracted: {len(properties)}
- URLs searched: {len(urls_to_search)}
- Selected websites: {selected_websites}

TECHNICAL: Schema extraction may have failed due to page structure changes."""
                
                return {"error": error_msg}
                
        except Exception as e:
            return {"error": f"Firecrawl extraction failed: {str(e)}\n\nPlease check your API keys and try again."}
