from textwrap import dedent
from crewai import Agent, Task


class Tasks:
    def fg_analysis(self, agent: Agent) -> Task:
        return Task(
            description=dedent("""
                Analyze the Fear and Greed Index for the cryptocurrency market right now.
                This task involves evaluating the latest Fear and Greed Index data for the cryptocurrency market as a whole and interpreting the overall market sentiment.

                Your analysis should include:
                - Identifying key trends and patterns in the Fear and Greed Index data.
                - Noting any significant changes, trend reversals, or anomalies in the current data.
                - Providing a summary of the current market sentiment based on the Fear and Greed Index.
                - Making actionable recommendations for trading or investment based on the observed trends.

                Utilize your expertise to provide an in-depth analysis of the cryptocurrency market as reflected in the Fear and Greed Index data.
            """),
            expected_output=dedent("""
                The expected output is a comprehensive analysis report of the Fear and Greed Index for the cryptocurrency market.
                The report should be clear, actionable, and provide insights to help guide strategic decisions in the cryptocurrency market.
                Make sure the characters are within the limit of 500 characters.
                Use below format for the report:
                
                Fear and Greed Index Analysis Report:
                
                Current Index Value is <fill with the current value>
                Which indicates the current market sentiment is <fill with the current sentiment>
                
                - A summary of key trends and patterns in the Fear and Greed Index data.
                - Observations of any significant changes or anomalies in the current market sentiment.
                - An assessment of the current market sentiment based on the Fear and Greed Index.
                - Actionable recommendations for trading or investment based on the analysis of the Fear and Greed Index trends.
            """),
            agent=agent,
        )
