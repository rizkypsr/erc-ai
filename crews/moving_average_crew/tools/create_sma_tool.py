import os
from typing import Any, Type

import matplotlib.pyplot as plt
import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from network.httpx_client import client


class CreateSMAToolSchema(BaseModel):
    """Input for the CreateSMATool"""

    coin: str = Field(
        ...,
        description="The coin symbol to extract and create the moving average chart.",
    )


class CreateSMATool(BaseTool):
    name: str = "Making small moving average chart"
    description: str = "Generate the moving average chart then save it"
    args_schema: Type[BaseModel] = CreateSMAToolSchema

    def _run(self, **kwargs: Any) -> Any:
        coin = kwargs.get("coin")
        if not coin:
            return "Coin symbol is required."

        fmp_api_key = os.getenv("FMP_API_KEY")
        url = f"https://financialmodelingprep.com/api/v3/technical_indicator/1day/{coin}USD?type=sma&period=5&apikey={fmp_api_key}"
        technical_indicator_name = "sma"
        response = client.get(url)

        print(f"xxxx url: {url}")
        print(response.status_code)

        if response.status_code == 200:
            data = response.json()

            df = pd.DataFrame(data)
            df = df[:30]

            if "date" not in df.columns:
                return "Error: 'date' column not found in the data. Tell the user to try again later."

            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)

            plt.figure(figsize=(14, 7))
            plt.plot(df.index, df["close"], label="Close Price", color="blue")

            if technical_indicator_name in df.columns:
                plt.plot(
                    df.index,
                    df[technical_indicator_name],
                    label=f"{technical_indicator_name.upper()} (5)",
                    color="orange",
                )
            else:
                return (
                    f"Error: {technical_indicator_name.upper()} not found in the data"
                )

            plt.title(
                f"last 1 month Closing Prices of {coin}/USD and {technical_indicator_name.upper()} (5-day)"
            )
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.legend()
            plt.grid(True)
            plt.savefig("sma.jpeg")

            return f"Moving Average chart created successfully for {coin}."
        else:
            return "Failed to fetch data from the API. Please check the coin symbol."
