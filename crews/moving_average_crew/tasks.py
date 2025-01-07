from textwrap import dedent
from crewai import Agent, Task


class Tasks:
    def moving_average_analysis(self, agent: Agent, coin: str) -> Task:
        return Task(
            description=dedent(f"""
                Analyze the moving average chart for the specified cryptocurrency, {coin}. 
                The task involves evaluating the simple moving average (SMA) data presented in the chart screenshot for {coin}. 

                Your analysis should include:
                - Identifying key trends and patterns in the SMA data.
                - Noting any significant crossovers, trend reversals, or anomalies.
                - Providing a summary of the current market position based on the SMA.
                - Making actionable recommendations based on the observed SMA trends.

                Use your expertise to deliver a comprehensive assessment of the cryptocurrency's performance as indicated by the moving average data.
            """),
            expected_output=dedent(f"""
                The expected output is a detailed analysis report of the simple moving average for {coin}. 
                The report should include:
                - A summary of key trends and patterns identified in the SMA data.
                - Observations of any significant crossovers or anomalies.
                - An assessment of the cryptocurrency's market position based on the SMA.
                - Actionable recommendations for trading or investment based on the SMA analysis.

                The report should be clear, concise, and tailored to assist in strategic decision-making regarding the cryptocurrency.
                Make sure the characters are within the limit of 500 characters.
            """),
            agent=agent,
        )
