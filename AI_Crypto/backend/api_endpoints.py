# Add these imports and endpoints to your FastAPI app

from pydantic import BaseModel
from cryptobot.assistant import CryptoAIAssistant

# Initialize the AI assistant
crypto_assistant = CryptoAIAssistant(api_base_url="http://localhost:8000")  # Use your actual API URL

class UserMessage(BaseModel):
    message: str
    user_id: str = None

class AssistantResponse(BaseModel):
    message: str
    data: dict = None
    message_type: str = "text"

@app.post("/assistant/chat", response_model=AssistantResponse)
async def chat_with_assistant(user_message: UserMessage):
    """
    Chat with the crypto AI assistant
    """
    try:
        # Process user input
        response = await crypto_assistant.process_user_input(user_message.message)
        
        # Format response for the client
        return AssistantResponse(
            message=response["content"],
            data=response.get("data"),
            message_type=response["type"]
        )
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process your message")

@app.get("/assistant/recommendations")
async def get_recommendations(limit: int = 5):
    """
    Get top crypto recommendations
    """
    try:
        recommendations = await crypto_assistant.get_top_recommendations(limit)
        return {"data": recommendations}
    
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")

@app.get("/assistant/market-sentiment")
async def get_market_sentiment():
    """
    Get overall market sentiment
    """
    try:
        # Get top coins
        response = requests.get(f"{COINGECKO_BASE_URL}/coins/markets", params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 20,
            "page": 1,
            "sparkline": False,
        })
        response.raise_for_status()
        coins = response.json()
        
        # Calculate sentiment
        up_count = sum(1 for coin in coins if coin["price_change_percentage_24h"] > 0)
        down_count = len(coins) - up_count
        
        if up_count > down_count * 2:
            sentiment = "very bullish"
        elif up_count > down_count:
            sentiment = "bullish"
        elif down_count > up_count * 2:
            sentiment = "very bearish"
        elif down_count > up_count:
            sentiment = "bearish"
        else:
            sentiment = "neutral"
        
        # Get top performers
        coins.sort(key=lambda x: x["price_change_percentage_24h"] or 0, reverse=True)
        top_performers = coins[:5]
        
        return {
            "sentiment": sentiment,
            "up_count": up_count,
            "down_count": down_count,
            "total_coins": len(coins),
            "top_performers": [
                {
                    "id": coin["id"],
                    "name": coin["name"],
                    "symbol": coin["symbol"].upper(),
                    "price_change_24h": coin["price_change_percentage_24h"]
                }
                for coin in top_performers
            ]
        }
    
    except Exception as e:
        logger.error(f"Error getting market sentiment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze market sentiment")