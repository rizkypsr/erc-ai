from textwrap import dedent
from crewai import Agent, Task


class Tasks:
    def market_analysis(self, agent: Agent, coin: str) -> Task:
        return Task(
            description=dedent(f"""
                Your role involves obtaining a URL using a tool and fetching real-time data from a designated website using another tool.
                Continue this task until you successfully retrieve the content from the website; do not proceed to the next task until this is accomplished.
                Your expertise lies in extracting the following values from the retrieved content and generate a report using these format below:
                1. Current Price(Live Price) and Percentage Change
                2. Market Capitalization (MARKETCAP)
                3. Circulating Supply
                4. 24-Hour Trading Volume
                5. Total Supply
                6. Fully Diluted Valuation
                7. 24-Hour High and Low Prices
                8. All-Time High and Low Prices
                Print these values after extracting them. Ensure accuracy; the values will be provided in the website's content.
                Coin: {coin}
            """),
            expected_output=dedent("""
                Make a report using these values and keep using list formatting.
                Also tell about if the asset is undervalued or overvalued:
                
                Make sure the characters are within the limit of 500 characters."""),
            agent=agent,
        )
