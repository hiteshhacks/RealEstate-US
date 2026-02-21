# 🏠 AI Real Estate Agent - Project Structure

A modular Python application for finding and analyzing real estate properties using AI agents (Agno) and Firecrawl web scraping.

## 📁 Project Structure

```
realestate/
├── main.py                    # Entry point - Streamlit application
├── config.py                  # Configuration and environment variables
├── requirements.txt           # Python dependencies
│
├── ui/                        # User Interface Components
│   ├── __init__.py
│   └── display.py            # Streamlit UI components and professional display
│
├── llm/                       # Language Model Configuration
│   ├── __init__.py
│   └── models.py             # Gemini LLM initialization
│
├── agent/                     # AI Agent Logic (Agno Framework)
│   ├── __init__.py
│   ├── sequential_agents.py  # Agent creation and configuration
│   └── analysis.py           # Sequential analysis workflow orchestration
│
├── scraper/                   # Web Scraping & Data Extraction
│   ├── __init__.py
│   └── firecrawl_agent.py    # DirectFirecrawlAgent for property search
│
├── schemas/                   # Pydantic Models
│   ├── __init__.py
│   └── models.py             # Property data schemas (PropertyDetails, PropertyListing)
│
└── utils/                     # Utility Functions
    ├── __init__.py
    └── helpers.py            # Helper functions for data processing
```

## 📦 Module Descriptions

### **main.py**
- **Purpose**: Streamlit web application entry point
- **Key Functions**: 
  - `main()`: Initializes UI, handles form input, orchestrates analysis
- **Runs**: `streamlit run main.py`

### **config.py**
- **Purpose**: Centralized configuration management
- **Contains**:
  - Environment variable loading
  - API key defaults
  - Website list configuration

### **ui/ - User Interface**
- **display.py**:
  - `display_properties_professionally()`: Renders property cards, metrics, and tabs
  - Professional UI layout with property details, market analysis, and valuations

### **llm/ - Language Model**
- **models.py**:
  - `initialize_gemini_model()`: Factory function for Gemini LLM initialization
  - Encapsulates LLM configuration

### **agent/ - AI Agents (Agno Framework)**
- **sequential_agents.py**:
  - `create_sequential_agents()`: Creates three specialized agents:
    - 🔍 Property Search Agent
    - 📊 Market Analysis Agent
    - 💰 Property Valuation Agent

- **analysis.py**:
  - `run_sequential_analysis()`: Orchestrates sequential workflow:
    1. Property Search (Firecrawl integration)
    2. Market Analysis (Gemini analysis)
    3. Property Valuation (Gemini assessment)
    4. Results synthesis

### **scraper/ - Web Scraping**
- **firecrawl_agent.py**:
  - `DirectFirecrawlAgent` class
  - `find_properties_direct()`: Uses Firecrawl + schema to extract properties
  - Supports: Zillow, Realtor.com, Trulia, Homes.com

### **schemas/ - Data Models**
- **models.py**:
  - `PropertyDetails`: Individual property schema
  - `PropertyListing`: Collection of properties schema
  - Pydantic validation and serialization

### **utils/ - Helper Functions**
- **helpers.py**:
  - `extract_property_valuation()`: Extracts specific property analysis from full results

## 🚀 Running the Application

### Prerequisites
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
GOOGLE_API_KEY=your_google_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

### Run Application
```bash
streamlit run main.py
```

The application will be available at `http://localhost:8501`

## 🔄 Data Flow

```
User Input (Form)
    ↓
config.py (Loads API keys)
    ↓
main.py (Validates input)
    ↓
agent/analysis.py (run_sequential_analysis)
    ├─→ scraper/firecrawl_agent.py (Find properties)
    ├─→ llm/models.py (Initialize Gemini)
    ├─→ agent/sequential_agents.py (Create agents)
    ├─→ Market Analysis Agent
    ├─→ Property Valuation Agent
    └─→ Results compilation
    ↓
ui/display.py (display_properties_professionally)
    ↓
Streamlit UI Output
```

## 🤖 Agent Workflow

1. **Property Search Agent**
   - Finds properties using Firecrawl API
   - Extracts: address, price, bedrooms, bathrooms, features
   - Output: List of PropertyDetails

2. **Market Analysis Agent**
   - Analyzes market trends
   - Provides neighborhood insights
   - Output: Market analysis text

3. **Property Valuation Agent**
   - Assesses property values
   - Estimates investment potential
   - Output: Individual property valuations

## 📝 Key Features

✅ **Multi-agent architecture** - Specialized agents for different tasks
✅ **Web scraping** - Firecrawl integration for real estate websites
✅ **AI-powered analysis** - Google Gemini for intelligent insights
✅ **Professional UI** - Streamlit for interactive dashboard
✅ **Modular design** - Easy to extend and maintain
✅ **Type-safe** - Pydantic schemas for data validation
✅ **Configurable** - Easy API key management

## 🛠️ Extending the Project

### Add a New Agent
1. Create function in `agent/sequential_agents.py`
2. Use the `Agent` class from Agno framework
3. Integrate in `agent/analysis.py` workflow

### Add a New Website
1. Update `config.py` with new website URL
2. Modify `scraper/firecrawl_agent.py` to handle new website
3. Update UI in `ui/display.py` if needed

### Add Helper Functions
1. Add new functions to `utils/helpers.py`
2. Import and use in relevant modules

## 📚 Dependencies

- **streamlit**: Web UI framework
- **agno**: AI agent framework
- **pydantic**: Data validation
- **firecrawl-py**: Web scraping library
- **openai/google**: LLM models
- **python-dotenv**: Environment management

## 👨‍💻 Development Tips

- Keep modules focused on single responsibility
- Use type hints for better IDE support
- Document functions with docstrings
- Test individual modules independently
- Use environment variables for secrets

## 📄 License

This project is part of the AI Real Estate Agent system.

---

**Version**: 1.0.0  
**Last Updated**: February 2026
