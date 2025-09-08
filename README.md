# startup.registroimprese.it Web Scraping

A Python project for automated **web scraping of Italian startups** from the official [Registro Imprese - Startup](https://startup.registroimprese.it/isin/home) portal.  
This script was built using **Selenium** and **undetected-chromedriver** to bypass bot detection and interact with dynamic content.

---

## 🚀 Features
- Automates login and navigation on the Registro Imprese Startup portal.  
- Selects all Italian regions dynamically from the dropdown filter.  
- Iterates through all paginated search results.  
- Extracts **startup company names** (and other visible details).  
- Simulates user behavior with randomized **User-Agents** to reduce blocking.  
- Handles dynamic elements with Selenium’s `WebDriverWait` and Expected Conditions.  
- Supports headless and non-headless browser execution.  
