import os
from typing import Any, Type

import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import requests
from crewai.tools import BaseTool
from matplotlib.dates import DateFormatter
from pydantic import BaseModel, Field


class CreateCandleStickToolSchema(BaseModel):
    """Input for the CreateCandleStickTool"""

    coin: str = Field(
        ..., description="The coin symbol to extract and create the candlestick chart."
    )


class CreateCandleStick(BaseTool):
    name: str = "Extract symbol and create candlestick chart from api"
    description: str = "Extract symbol and create candelstick chart from the api"
    args_schema: Type[BaseModel] = CreateCandleStickToolSchema

    def _run(self, **kwargs: Any) -> Any:
        coin = kwargs.get("coin")
        if not coin:
            return "Coin symbol is required."

        fmp_api_key = os.getenv("FMP_API_KEY")
        api_url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{coin}USD?apikey={fmp_api_key}"

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()

            if not data.get("historical"):
                return f"No historical data found for {coin}. Please check the coin symbol."

            historical_data = data.get("historical", [])
            df = pd.DataFrame(historical_data)
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date")
            df.set_index("date", inplace=True)

            last_30_days_data = df.tail(30)

            custom_style = mpf.make_mpf_style(
                base_mpl_style="default",
                rc={"font.size": 8},
                marketcolors=mpf.make_marketcolors(
                    up="lime",
                    down="red",
                    wick={"up": "lime", "down": "red"},
                    volume="skyblue",
                ),
            )

            # Create a figure with 2 subplots
            fig, (ax1, ax2) = plt.subplots(
                2, 1, figsize=(12, 12), gridspec_kw={"height_ratios": [2, 1]}
            )

            # Plot the candlestick chart
            mpf.plot(
                last_30_days_data,
                type="candle",
                style=custom_style,
                ax=ax1,
                volume=False,
            )
            ax1.set_title(f"{coin}/USD Price", fontsize=16)
            ax1.set_ylabel("Price", fontsize=12)

            # Plot the volume bar chart
            ax2.bar(
                df.index,
                df["volume"],
                width=0.8,
                align="center",
                color="skyblue",
                edgecolor="navy",
            )
            ax2.set_title(f"{coin}/USD Trading Volume", fontsize=16)
            ax2.set_xlabel("Date", fontsize=12)
            ax2.set_ylabel("Volume", fontsize=12)

            # Format x-axis for volume chart
            ax2.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")

            # Format y-axis labels for volume chart
            ax2.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, p: f"{x / 1e9:.1f}B")
            )

            # Add grid lines to volume chart
            ax2.grid(axis="y", linestyle="--", alpha=0.7)

            # Adjust layout and display the plot
            plt.tight_layout()
            plt.savefig("coin_screenshot.jpeg")

            return f"Coin candlestick chart created successfully for {coin}."
        else:
            return "Failed to fetch data from the API. Please check the coin symbol."
