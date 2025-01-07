from crewai.tools import BaseTool
from openai import OpenAI

import base64
import os


class GetSMATool(BaseTool):
    name: str = "Extract the content from the image"
    description: str = "Extract the content from the image"

    def _run(self, argument: str) -> str:
        image_path = "sma.jpeg"
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        try:
            with open(image_path, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        except FileNotFoundError:
            return f"Error: The image file '{image_path}' was not found."
        except Exception as e:
            return f"Error reading the image file: {str(e)}"

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
                            Please analyze the following image of a cryptocurrency moving average chart and provide a detailed summary.
                            The analysis should include:
                            - Key trends and patterns observed in the chart.
                            - Any significant crossovers or anomalies.
                            - An assessment of the current market position based on the chart.
                            - Provide specific recommendations based on the analysis, such as:
                            - Buy or sell signals based on trend and pattern analysis, give one word answer for this from these five options: Strong Sell, Sell, Neutral, Buy, Strong Buy.
                            - Recommendations based on the moving average data.
  
                            Review the image carefully and provide a comprehensive report.
  
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

        content = response.choices[0].message.content
        if content is None:
            return "Error: No content was returned from the analysis."
        return content
