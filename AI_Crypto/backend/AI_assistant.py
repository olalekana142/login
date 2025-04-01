import re
import json
from typing import Dict, List, Any, Optional
import logging
import requests
from datetime import datetime, timedelta
import random

# Intent recognition patterns
INTENT_PATTERNS = {
    "price_check": [
        r"(?:what is|what's|show|get|check) (?:the )?(?:price|value) (?:of |for )?([a-zA-Z0-9 ]+)",
        r"how much (?:is|does) ([a-zA-Z0-9 ]+) cost",
        r"([a-zA-Z0-9 ]+) price"
    ],
    "price_prediction": [
        r"(?:will|is|could) ([a-zA-Z0-9 ]+) (?:price )?(?:go up|increase|rise|grow|moon)",
        r"(?:will|is|could) ([a-zA-Z0-9 ]+) (?:price )?(?:go down|decrease|fall|drop|crash)",
        r"(?:what will|predict|forecast) ([a-zA-Z0-9 ]+) (?:be worth|price)"
    ],
    "recommendation": [
        r"(?:what|which) (?:crypto|coin|token)s? (?:should I|to) (?:buy|invest in|trade)",
        r"recommend (?:a |some )?(?:crypto|coin|token)s?",
        r"good (?:crypto|coin|token)s? to (?:buy|invest in|trade) (?:now|today|right now)?",
        r"when (?:should I|to) (?:buy|sell) ([a-zA-Z0-9 ]+)"
    ],
    "portfolio": [
        r"(?:how is|check) my portfolio",
        r"portfolio performance",
        r"my holdings"
    ],
    "market_overview": [
        r"(?:how is|what's|overview of) the (?:crypto |)market",
        r"market (?:summary|overview|condition)",
        r"top (?:performing |)(?:crypto|coin|token)s?"
    ]
}

class CryptoAIAssistant:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
        self.logger = logging.getLogger(__name__)
        
    def detect_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Detect user intent from their message
        """
        user_input = user_input.lower().strip()
        result = {"intent": "unknown", "entities": {}}
        
        for intent, patterns in INTENT_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, user_input)
                if match:
                    result["intent"] = intent
                    # Extract entity if available
                    if match.groups():
                        coin_name = match.group(1).strip()
                        result["entities"]["coin_name"] = coin_name
                    break
            if result["intent"] != "unknown":
                break
        
        # Default to general help if intent is still unknown
        if result["intent"] == "unknown":
            if "help" in user_input or "guide" in user_input:
                result["intent"] = "help"
        
        return result
    
    def get_coin_id(self, coin_name: str) -> Optional[str]:
        """
        Map a user-friendly coin name to its API ID
        """
        try:
            # Common mappings
            coin_mappings = {
                "bitcoin": "bitcoin",
                "btc": "bitcoin",
                "ethereum": "ethereum",
                "eth": "ethereum",
                "cardano": "cardano",
                "ada": "cardano",
                "solana": "solana",
                "sol": "solana",
                "dogecoin": "dogecoin",
                "doge": "dogecoin",
                # Add more mappings as needed
            }
            
            coin_name = coin_name.lower()
            
            # Check direct mapping
            if coin_name in coin_mappings:
                return coin_mappings[coin_name]
                
            # Search for the coin in the API
            response = requests.get(f"{self.api_base_url}/prices/current?limit=100")
            response.raise_for_status()
            coins = response.json()["data"]
            
            for coin in coins:
                if (coin["symbol"].lower() == coin_name or 
                    coin["name"].lower() == coin_name or
                    coin_name in coin["name"].lower()):
                    return coin["id"]
            
            return None
        
        except Exception as e:
            self.logger.error(f"Error getting coin ID: {str(e)}")
            return None
    
    async def get_current_price(self, coin_id: str) -> Dict[str, Any]:
        """
        Get current price for a specific cryptocurrency
        """
        try:
            response = requests.get(f"{self.api_base_url}/prices/current")
            response.raise_for_status()
            coins = response.json()["data"]
            
            for coin in coins:
                if coin["id"] == coin_id:
                    return coin
            
            return None
        
        except Exception as e:
            self.logger.error(f"Error getting current price: {str(e)}")
            return None
    
    async def get_coin_recommendation(self, coin_id: str) -> Dict[str, Any]:
        """
        Get trading recommendation for a specific coin
        """
        try:
            # Get historical data for analysis
            response = requests.get(f"{self.api_base_url}/prices/historical/{coin_id}?days=60")
            response.raise_for_status()
            historical_data = response.json()["data"]
            
            # Analyze data using the TA engine
            ta_engine = TechnicalAnalysisEngine()
            analysis = ta_engine.analyze_price_data(historical_data)
            signals = ta_engine.generate_signals(analysis)
            
            # Get current price info
            coin_info = await self.get_current_price(coin_id)
            if coin_info:
                result = {
                    "coin": coin_info,
                    "signals": signals
                }
                return result
            return None
        
        except Exception as e:
            self.logger.error(f"Error getting recommendation: {str(e)}")
            return None
    
    async def get_top_recommendations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get top coin recommendations based on technical analysis
        """
        try:
            # Get list of top coins
            response = requests.get(f"{self.api_base_url}/prices/current?limit=20")
            response.raise_for_status()
            coins = response.json()["data"]
            
            # Get historical data for all coins
            all_coins_data = {}
            for coin in coins:
                coin_id = coin["id"]
                response = requests.get(f"{self.api_base_url}/prices/historical/{coin_id}?days=60")
                response.raise_for_status()
                historical_data = response.json()["data"]
                all_coins_data[coin_id] = historical_data
            
            # Generate recommendations
            ta_engine = TechnicalAnalysisEngine()
            recommendations = ta_engine.recommend_coins(all_coins_data)
            
            # Return top recommendations
            return recommendations[:limit]
        
        except Exception as e:
            self.logger.error(f"Error getting top recommendations: {str(e)}")
            return []
    
    async def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input and generate appropriate response
        """
        intent_data = self.detect_intent(user_input)
        
        response = {
            "type": "text",
            "content": "I'm sorry, I'm not sure how to help with that. You can ask me about crypto prices, recommendations, or market overview."
        }
        
        try:
            if intent_data["intent"] == "price_check" and "coin_name" in intent_data["entities"]:
                coin_name = intent_data["entities"]["coin_name"]
                coin_id = self.get_coin_id(coin_name)
                
                if coin_id:
                    coin_data = await self.get_current_price(coin_id)
                    if coin_data:
                        price_change_text = "up" if coin_data["price_change_24h"] > 0 else "down"
                        response = {
                            "type": "price_info",
                            "content": f"{coin_data['name']} ({coin_data['symbol']}) is currently worth ${coin_data['current_price']:.2f}. It's {price_change_text} {abs(coin_data['price_change_24h']):.2f}% in the last 24 hours.",
                            "data": coin_data
                        }
                    else:
                        response["content"] = f"I couldn't find current price information for {coin_name}."
                else:
                    response["content"] = f"I couldn't find a cryptocurrency called {coin_name}. Please check the name and try again."
            
            elif intent_data["intent"] == "recommendation":
                if "coin_name" in intent_data["entities"]:
                    # Recommendation for specific coin
                    coin_name = intent_data["entities"]["coin_name"]
                    coin_id = self.get_coin_id(coin_name)
                    
                    if coin_id:
                        recommendation = await self.get_coin_recommendation(coin_id)
                        if recommendation:
                            coin_info = recommendation["coin"]
                            signals = recommendation["signals"]
                            
                            content = f"For {coin_info['name']} ({coin_info['symbol']}), my recommendation is: {signals['recommendation'].upper()}.\n\n"
                            
                            if signals["buy_signals"]:
                                content += "Buy signals:\n" + "\n".join([f"- {signal}" for signal in signals["buy_signals"]]) + "\n\n"
                            
                            if signals["sell_signals"]:
                                content += "Sell signals:\n" + "\n".join([f"- {signal}" for signal in signals["sell_signals"]])
                            
                            response = {
                                "type": "recommendation",
                                "content": content,
                                "data": recommendation
                            }
                        else:
                            response["content"] = f"I couldn't analyze {coin_name} at the moment. Please try again later."
                    else:
                        response["content"] = f"I couldn't find a cryptocurrency called {coin_name}. Please check the name and try again."
                else:
                    # General recommendations
                    top_recommendations = await self.get_top_recommendations(5)
                    
                    if top_recommendations:
                        content = "Here are my top crypto recommendations right now:\n\n"
                        
                        for i, coin in enumerate(top_recommendations, 1):
                            content += f"{i}. {coin['name']} ({coin['symbol']}) - {coin['strength'].upper()}\n"
                            if coin["signals"]["buy"]:
                                content += f"   Key signal: {coin['signals']['buy'][0]}\n"
                        
                        response = {
                            "type": "top_recommendations",
                            "content": content,
                            "data": top_recommendations
                        }
                    else:
                        response["content"] = "I couldn't generate recommendations at the moment. Please try again later."
            
            elif intent_data["intent"] == "market_overview":
                # Get top coins for market overview
                top_coins_response = requests.get(f"{self.api_base_url}/prices/current?limit=10")
                top_coins_response.raise_for_status()
                top_coins = top_coins_response.json()["data"]
                
                if top_coins:
                    # Calculate market sentiment
                    up_count = sum(1 for coin in top_coins if coin["price_change_24h"] > 0)
                    down_count = len(top_coins) - up_count
                    
                    if up_count > down_count + 3:
                        sentiment = "very bullish"
                    elif up_count > down_count:
                        sentiment = "slightly bullish"
                    elif down_count > up_count + 3:
                        sentiment = "very bearish"
                    elif down_count > up_count:
                        sentiment = "slightly bearish"
                    else:
                        sentiment = "neutral"
                    
                    content = f"The crypto market is currently {sentiment}. "
                    content += f"{up_count} of the top 10 coins are up in the last 24 hours.\n\n"
                    
                    # Add top performers
                    top_coins.sort(key=lambda x: x["price_change_24h"], reverse=True)
                    content += "Top performers:\n"
                    for i, coin in enumerate(top_coins[:3], 1):
                        content += f"{i}. {coin['name']} ({coin['symbol']}): {coin['price_change_24h']:.2f}%\n"
                    
                    response = {
                        "type": "market_overview",
                        "content": content,
                        "data": {
                            "sentiment": sentiment,
                            "top_coins": top_coins
                        }
                    }
                else:
                    response["content"] = "I couldn't retrieve market data at the moment. Please try again later."
            
            elif intent_data["intent"] == "help":
                response = {
                    "type": "help",
                    "content": "I'm your crypto assistant! Here's how I can help you:\n\n"
                              "- Check prices: 'What's the price of Bitcoin?'\n"
                              "- Get recommendations: 'Should I buy Ethereum now?'\n"
                              "- Market overview: 'How is the crypto market today?'\n"
                              "- Top coins: 'What are the best coins to buy?'\n\n"
                              "Just ask me what you'd like to know about cryptocurrencies!"
                }
                
        except Exception as e:
            self.logger.error(f"Error processing input: {str(e)}")
            response = {
                "type": "error",
                "content": "I encountered an error while processing your request. Please try again later."
            }
        
        return response