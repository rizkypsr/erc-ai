import base64
import os
from typing import Any

from crewai.tools import BaseTool
from openai import OpenAI


class AnalyzeChart(BaseTool):
    name: str = "Extract the content from the image"
    description: str = "Extract the content from the image"

    def _run(self, **kwargs: Any) -> Any:
        image_path = "coin_screenshot.jpeg"
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        try:
            with open(image_path, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        except FileNotFoundError:
            return "Image file not found. Please try again."
        except Exception:
            return "Error when displaying the image"

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "text"},
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """
                  To perform a comprehensive technical analysis of a provided candlestick chart and to generate the required outputs, you would typically use specialized software or tools like TradingView, MetaTrader, or similar platforms. Since I don't have access to view or analyze specific images directly, I will provide a detailed framework for how you can conduct this analysis:

                    ### 1. Trend Analysis
                    **Current Trend**:
                    - Identify whether the market is in an uptrend, downtrend, or moving sideways. This can be done by observing the direction of the price movement over time.
                    - **Uptrend**: Higher highs and higher lows.
                    - **Downtrend**: Lower highs and lower lows.
                    - **Sideways**: Horizontal movement with no clear direction.

                    **Trend Strength and Potential Reversal Points**:
                    - Use trend strength indicators like the Average Directional Index (ADX). A high ADX indicates a strong trend.
                    - Look for patterns like Head and Shoulders, Double Tops/Bottoms to identify potential reversal points.

                    ### 2. Support and Resistance Levels
                    **Major Support and Resistance Levels**:
                    - Identify key price levels where the market has repeatedly bounced off (support) or reversed from (resistance).

                    **Significant Breakouts or Breakdowns**:
                    - Highlight any recent price movements that have broken through established support or resistance levels, which may indicate strong future price movement.

                    ### 3. Candlestick Patterns
                    **Common Candlestick Patterns**:
                    - **Doji**: Indicates indecision in the market, potential reversal signal.
                    - **Hammer**: Bullish reversal pattern after a downtrend.
                    - **Engulfing Patterns**: Bullish or bearish, indicating strong reversal potential.

                    **Insights on Potential Bullish or Bearish Signals**:
                    - Bullish patterns suggest potential buying opportunities.
                    - Bearish patterns suggest potential selling opportunities.

                    ### 5. Volume Analysis
                    **Analyze Volume Trends**:
                    - Confirm price movements with corresponding volume. An increase in volume confirms the strength of the price movement.

                    **Unusual Volume Spikes**:
                    - Identify significant volume spikes which can indicate strong buying/selling pressure and potential trend changes.

                    ### 6. Risk Assessment
                    **Potential Risks and Suggestions for Risk Management**:
                    - Identify levels for stop-loss orders to manage downside risk.
                    - Suggest appropriate position sizing based on volatility and risk tolerance.

                    Explain these words too given below
                    - support_price:
                    - consolidation_points_price:
                    - major_resistance_price:
                    - psychological_break_price:
                    - immediate_resistance:

                    ### 7. Summary and Recommendations
                    **Key Findings**:
                    - Summarize the identified trend, key support and resistance levels, significant candlestick patterns, and volume analysis.

                    **Actionable Trading Recommendations**:
                    - Provide specific recommendations based on the analysis, such as:
                      - Buy or sell signals based on trend and pattern analysis, give one word answer for this from these five options: Strong Sell, Sell, Neutral, Buy, Strong Buy.
                      - Suggested entry and exit points.
                      - Risk management strategies like stop-loss levels.

                  By following this framework, you can systematically analyze a candlestick chart and derive actionable insights for trading decisions.
                  """,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=800,
            )

            return response.choices[0].message.content

        except Exception:
            return "Error when analyzing the image"
