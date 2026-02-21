"""
Sequential agent creation for property analysis workflow.
"""
from agno.agent import Agent


def create_sequential_agents(llm, user_criteria):
    """
    Create agents for sequential manual execution.
    
    Args:
        llm: Language model instance (Gemini)
        user_criteria: User search criteria dictionary
    
    Returns:
        Tuple of (property_search_agent, market_analysis_agent, property_valuation_agent)
    """
    
    property_search_agent = Agent(
        name="Property Search Agent",
        model=llm,
        instructions="""
        You are a property search expert. Your role is to find and extract property listings.
        
        WORKFLOW:
        1. SEARCH FOR PROPERTIES:
           - Use the provided Firecrawl data to extract property listings
           - Focus on properties matching user criteria
           - Extract detailed property information
        
        2. EXTRACT PROPERTY DATA:
           - Address, price, bedrooms, bathrooms, square footage
           - Property type, features, listing URLs
           - Agent contact information
        
        3. PROVIDE STRUCTURED OUTPUT:
           - List properties with complete details
           - Include all listing URLs
           - Rank by match quality to user criteria
        
        IMPORTANT: 
        - Focus ONLY on finding and extracting property data
        - Do NOT provide market analysis or valuations
        - Your output will be used by other agents for analysis
        """,
    )
    
    market_analysis_agent = Agent(
        name="Market Analysis Agent",
        model=llm,
        instructions="""
        You are a market analysis expert. Provide CONCISE market insights.
        
        REQUIREMENTS:
        - Keep analysis brief and to the point
        - Focus on key market trends only
        - Provide 2-3 bullet points per area
        - Avoid repetition and lengthy explanations
        
        COVER:
        1. Market Condition: Buyer's/seller's market, price trends
        2. Key Neighborhoods: Brief overview of areas where properties are located
        3. Investment Outlook: 2-3 key points about investment potential
        
        FORMAT: Use bullet points and keep each section under 100 words.
        """,
    )
    
    property_valuation_agent = Agent(
        name="Property Valuation Agent",
        model=llm,
        instructions="""
        You are a property valuation expert. Provide CONCISE property assessments.
        
        REQUIREMENTS:
        - Keep each property assessment brief (2-3 sentences max)
        - Focus on key points only: value, investment potential, recommendation
        - Avoid lengthy analysis and repetition
        - Use bullet points for clarity
        
        FOR EACH PROPERTY, PROVIDE:
        1. Value Assessment: Fair price, over/under priced
        2. Investment Potential: High/Medium/Low with brief reason
        3. Key Recommendation: One actionable insight
        
        FORMAT: 
        - Use bullet points
        - Keep each property under 50 words
        - Focus on actionable insights only
        """,
    )
    
    return property_search_agent, market_analysis_agent, property_valuation_agent
