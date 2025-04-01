import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import ta  # Technical Analysis library

class TechnicalAnalysisEngine:
    def __init__(self):
        pass
    
    def analyze_price_data(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze historical price data and generate technical indicators
        """
        # Convert to DataFrame
        df = pd.DataFrame(historical_data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # Calculate technical indicators
        # RSI (Relative Strength Index)
        df['rsi'] = ta.momentum.RSIIndicator(close=df['price'], window=14).rsi()
        
        # MACD (Moving Average Convergence Divergence)
        macd = ta.trend.MACD(close=df['price'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()
        
        # Bollinger Bands
        bollinger = ta.volatility.BollingerBands(close=df['price'])
        df['bollinger_high'] = bollinger.bollinger_hband()
        df['bollinger_low'] = bollinger.bollinger_lband()
        df['bollinger_mid'] = bollinger.bollinger_mavg()
        
        # Moving Averages
        df['ma_20'] = df['price'].rolling(window=20).mean()
        df['ma_50'] = df['price'].rolling(window=50).mean()
        df['ma_200'] = df['price'].rolling(window=200).mean()
        
        return df.reset_index().to_dict('records')
    
    def generate_signals(self, analysis_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate trading signals based on technical analysis
        """
        df = pd.DataFrame(analysis_data)
        
        # Get the most recent data point
        latest = df.iloc[-1]
        previous = df.iloc[-2] if len(df) > 1 else None
        
        signals = {
            "buy_signals": [],
            "sell_signals": [],
            "strength": "neutral",
            "recommendation": "hold"
        }
        
        # Check for buy signals
        if previous is not None:
            # RSI oversold (below 30)
            if latest['rsi'] < 30:
                signals["buy_signals"].append("RSI indicates oversold conditions")
            
            # MACD line crosses above signal line
            if previous['macd'] < previous['macd_signal'] and latest['macd'] > latest['macd_signal']:
                signals["buy_signals"].append("MACD crossed above signal line")
            
            # Price near Bollinger lower band
            if latest['price'] < latest['bollinger_low'] * 1.02:
                signals["buy_signals"].append("Price near lower Bollinger Band")
            
            # Golden Cross (short-term MA crossing above long-term MA)
            if previous['ma_20'] < previous['ma_50'] and latest['ma_20'] > latest['ma_50']:
                signals["buy_signals"].append("Golden Cross (MA20 crossed above MA50)")
        
        # Check for sell signals
        if previous is not None:
            # RSI overbought (above 70)
            if latest['rsi'] > 70:
                signals["sell_signals"].append("RSI indicates overbought conditions")
            
            # MACD line crosses below signal line
            if previous['macd'] > previous['macd_signal'] and latest['macd'] < latest['macd_signal']:
                signals["sell_signals"].append("MACD crossed below signal line")
            
            # Price near Bollinger upper band
            if latest['price'] > latest['bollinger_high'] * 0.98:
                signals["sell_signals"].append("Price near upper Bollinger Band")
            
            # Death Cross (short-term MA crossing below long-term MA)
            if previous['ma_20'] > previous['ma_50'] and latest['ma_20'] < latest['ma_50']:
                signals["sell_signals"].append("Death Cross (MA20 crossed below MA50)")
        
        # Determine recommendation
        buy_count = len(signals["buy_signals"])
        sell_count = len(signals["sell_signals"])
        
        if buy_count > sell_count + 1:
            signals["strength"] = "strong buy"
            signals["recommendation"] = "buy"
        elif buy_count > sell_count:
            signals["strength"] = "weak buy"
            signals["recommendation"] = "buy"
        elif sell_count > buy_count + 1:
            signals["strength"] = "strong sell"
            signals["recommendation"] = "sell"
        elif sell_count > buy_count:
            signals["strength"] = "weak sell"
            signals["recommendation"] = "sell"
        else:
            signals["strength"] = "neutral"
            signals["recommendation"] = "hold"
        
        # Add current indicators
        signals["current_indicators"] = {
            "rsi": latest['rsi'],
            "macd": latest['macd'],
            "macd_signal": latest['macd_signal'],
            "price": latest['price'],
            "ma_20": latest['ma_20'],
            "ma_50": latest['ma_50']
        }
        
        return signals
    
    def recommend_coins(self, all_coins_data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Generate recommendations for multiple coins
        """
        recommendations = []
        
        for coin_id, data in all_coins_data.items():
            analysis = self.analyze_price_data(data)
            signals = self.generate_signals(analysis)
            
            # Add basic coin info
            coin_info = {
                "id": coin_id,
                "name": data[0].get("name", coin_id),
                "symbol": data[0].get("symbol", coin_id.upper()),
                "current_price": data[-1]["price"],
                "recommendation": signals["recommendation"],
                "strength": signals["strength"],
                "signals": {
                    "buy": signals["buy_signals"],
                    "sell": signals["sell_signals"]
                }
            }
            
            recommendations.append(coin_info)
        
        # Sort by recommendation strength
        strength_order = {
            "strong buy": 5,
            "weak buy": 4,
            "neutral": 3,
            "weak sell": 2,
            "strong sell": 1
        }
        
        recommendations.sort(key=lambda x: strength_order.get(x["strength"], 0), reverse=True)
        
        return recommendations