#!/usr/bin/env python3
"""
Startup script for Sttarkel News Scraper API
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from main import app
from config import get_config

def main():
    """Main function to start the server"""
    config = get_config()
    
    print("🚀 Starting Sttarkel News Scraper API...")
    print(f"📡 Server will run on http://{config.HOST}:{config.PORT}")
    print(f"🔧 Debug mode: {config.DEBUG}")
    print(f"📊 API Documentation: http://{config.HOST}:{config.PORT}/docs")
    print(f"📋 Alternative docs: http://{config.HOST}:{config.PORT}/redoc")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host=config.HOST,
            port=config.PORT,
            reload=config.DEBUG,
            log_level=config.LOG_LEVEL.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 