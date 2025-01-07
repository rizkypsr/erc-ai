from textwrap import dedent
from crewai import Agent, Task


class Tasks:
    def chart_analysis_task(self, agent: Agent, coin: str) -> Task:
        return Task(
            description=dedent(f"""
              Your role involves extracting a symbol and then create candlestick chart with volume
              sing a tool. You analyze candlestick charts to understand market sentiment 
              and price movements. By interpreting the patterns formed by candlesticks, they can make informed predictions 
              about future price directions. You assess the overall trend of the market (uptrend, downtrend,
              or sideways) by analyzing the candlestick patterns over various time frames. You can also detect 
              crucial support and resistance levels by analyzing where prices have historically reversed or stalled.
              You can generate buy or sell signals based on predefined criteria and candlestick patterns.
                              
              Coin: {coin}
          """),
            expected_output=dedent("""                          
            1. Trend Analysis:
                - Identify the current trend (uptrend, downtrend, or sideways).
                - Determine trend strength and potential reversal points.
            2. Support and Resistance Levels:
                - Identify major support and resistance levels.
                - Highlight any significant breakouts or breakdowns.
            3. Candlestick Patterns:
                - Detect and interpret common candlestick patterns (e.g., Doji, Hammer, Engulfing patterns, Harami etc).
                - Provide insights on potential bullish or bearish signals based on these patterns.
            5. Volume Analysis:
                - Analyze volume trends to confirm price movements.
                - Highlight any unusual volume spikes and their potential impact.
            6. Risk Assessment:
                - Assess potential risks and provide suggestions for risk management (e.g., stop-loss levels).
            7. Summary and Recommendations:
                - Summarize key findings from the analysis.
                - Provide actionable trading recommendations based on the analysis.
            
            Generate a comprehensive report from the analysis which includes:
            - Identification of the overall market trend (uptrend, downtrend, or sideways) across different time frames.
            - Key candlestick patterns detected and their interpretations.
            - Crucial support and resistance levels identified based on historical price reversals or stalls.
            - Buy or sell signals generated based on predefined criteria and candlestick patterns.
            - A summary of the potential future price directions with rationale.
                                   
            Make sure the characters are within the limit of 500 characters.
            """),
            agent=agent,
        )
