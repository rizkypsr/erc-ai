import os

from crewai.tools import BaseTool
from matplotlib import pyplot as plt

from network.httpx_client import client


class CreateFGChartTool(BaseTool):
    name: str = "Extract symbol and create financial growth chart from api"
    description: str = "Extract symbol and create financial growth chart from the api"

    def _run(self):
        cmc_pro_api_key = os.getenv("CMC_API_KEY")

        if not cmc_pro_api_key:
            return "Error: CMC_API_KEY not found."

        res = client.get(
            "https://pro-api.coinmarketcap.com/v3/fear-and-greed/latest",
            headers={"X-CMC_PRO_API_KEY": cmc_pro_api_key},
        )

        print(res.status_code)

        if res.status_code != 200:
            return None

        data = res.json()

        print(data["data"]["value"])

        colors = ["#4dab6d", "#72c66e", "#f6ee54", "#f36d54", "#ee4d55"]
        value = data["data"]["value"]

        if 1 <= value < 20:
            value = 2.85
        elif 20 <= value < 40:
            value = 2.20
        elif 40 <= value < 60:
            value = 1.55
        elif 60 <= value < 80:
            value = 0.90
        elif 80 <= value <= 100:
            value = 0.25

        # Create the polar plot
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(projection="polar")

        # Adjusting the positions and widths of the bars
        x = [0, 0.6, 1.2, 1.9, 2.5]  # Starting positions
        widths = [0.7, 0.7, 0.7, 0.7, 0.65]  # Widths of segments

        # Use polar bar plot with the correct order of colors (no reversal)
        ax.bar(
            x=x,
            width=widths,
            height=0.5,
            bottom=2,
            linewidth=3,
            edgecolor="white",
            color=colors,
            align="edge",
        )

        # Adjusting text positions and rotations for the correct labels
        plt.annotate(
            "EXTREME GREED",
            xy=(0.2, 2.1),
            rotation=-70,
            color="white",
            fontweight="bold",
        )
        plt.annotate(
            "GREED", xy=(0.89, 2.14), rotation=-40, color="white", fontweight="bold"
        )
        plt.annotate(
            "NEUTRAL", xy=(1.6, 2.2), rotation=0, color="white", fontweight="bold"
        )
        plt.annotate(
            "FEAR", xy=(2.3, 2.25), rotation=40, color="white", fontweight="bold"
        )
        plt.annotate(
            "EXTREME FEAR",
            xy=(2.9, 2.25),
            rotation=70,
            color="white",
            fontweight="bold",
        )

        # Add a needle or indicator for the value
        plt.annotate(
            "",
            xytext=(0, 0),
            xy=(value, 2.0),
            arrowprops=dict(
                arrowstyle="wedge,tail_width=0.5", color="black", shrinkA=0
            ),
            bbox=dict(boxstyle="circle", facecolor="black", linewidth=2.0),
            fontsize=45,
            color="white",
            ha="center",
        )

        plt.title(
            "Fear & Greed Index", loc="center", pad=20, fontsize=35, fontweight="bold"
        )

        # Hide the polar axes
        ax.set_axis_off()

        # Adjust layout and display the plot
        plt.tight_layout()
        plt.savefig("fg.jpeg")
        plt.close(fig)

        return f"Current Fear & Greed Index: {data['data']['value']} which indicates {data['data']['value_classification']}"
