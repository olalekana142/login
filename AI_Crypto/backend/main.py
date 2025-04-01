import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Crypto AI Assistant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your website domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from environment variable
COIN_API_KEY = os.environ.get("COIN_API_KEY")
if not COIN_API_KEY:
    logger.warning("COIN_API_KEY environment variable not set. API calls may fail.")

# Endpoints for popular crypto price APIs
COINMARKETCAP_BASE_URL = "https://pro-api.coinmarketcap.com/v1"
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

@app.get("/")
def read_root():
    return {"message": "Crypto AI Assistant API is running"}

@app.get("/prices/current")
async def get_current_prices(limit: int = 20, convert: str = "USD"):
    """
    Get current prices for top cryptocurrencies
    """
    try:
        # Use CoinGecko (free tier)
        url = f"{COINGECKO_BASE_URL}/coins/markets"
        params = {
            "vs_currency": convert.lower(),
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        coins = response.json()
        
        result = []
        for coin in coins:
            result.append({
                "id": coin["id"],
                "symbol": coin["symbol"].upper(),
                "name": coin["name"],
                "current_price": coin["current_price"],
                "market_cap": coin["market_cap"],
                "price_change_24h": coin["price_change_percentage_24h"],
                "last_updated": coin["last_updated"],
                "image": coin["image"]
            })
        
        return {"data": result}
    
    except Exception as e:
        logger.error(f"Error fetching current prices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/prices/historical/{coin_id}")
async def get_historical_prices(coin_id: str, days: int = 30, convert: str = "USD"):
    """
    Get historical prices for a specific cryptocurrency
    """
    try:
        url = f"{COINGECKO_BASE_URL}/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": convert.lower(),
            "days": days,
            "interval": "daily",
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Process price data
        prices = data["prices"]
        market_caps = data["market_caps"]
        volumes = data["total_volumes"]
        
        result = []
        for i in range(len(prices)):
            timestamp = prices[i][0]
            date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
            result.append({
                "date": date,
                "price": prices[i][1],
                "market_cap": market_caps[i][1] if i < len(market_caps) else None,
                "volume": volumes[i][1] if i < len(volumes) else None
            })
        
        return {"data": result}
    
    except Exception as e:
        logger.error(f"Error fetching historical prices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add more endpoints as needed for your crypto assistant

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)