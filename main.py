import asyncio
from asyncio.log import logger
import os
import textwrap
import telegramify_markdown
import agentops

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ErrorEvent
from crews.fg_index_crew.crew import FGIndexCrew
from crews.market_analysis_crew.crew import MarketAnalysisCrew
from crews.moving_average_crew.crew import MovingAverageCrew
from crews.technical_analysis_crew.crew import TechnicalAnalysisCrew
from utils.coin_finder import CoinFinder
from utils.load_json import load_json

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
dp = Dispatcher()

commands = [
    types.BotCommand(
        command="/analyze",
        description="Analyze the intrinsic value of the selected coin.",
    ),
    types.BotCommand(
        command="/ta", description="Capture and analyze a 1-month candlestick chart."
    ),
    types.BotCommand(
        command="/ma",
        description="Perform Moving Averages Analysis on the selected coin.",
    ),
    types.BotCommand(command="/fg", description="Perform Fear & Greed analysis."),
]

inline_keyboards = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Technical Analyze 📈", callback_data="technical_analyze"
            ),
            types.InlineKeyboardButton(
                text="Market Analyze 📌", callback_data="market_analyze"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text="Moving Average 🚥", callback_data="moving_average"
            ),
            types.InlineKeyboardButton(
                text="Fear & Greed 🧭", callback_data="fear_greed"
            ),
        ],
        [
            types.InlineKeyboardButton(text="Help 🤷‍♂️", callback_data="help"),
        ],
    ],
)


@dp.error(F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: Message):
    logger.critical("Critical error caused by %s", event.exception, exc_info=True)
    await message.answer(
        "An error occurred while processing your request. Please try again."
    )


@dp.callback_query()
async def handle_callback(query: types.CallbackQuery) -> None:
    if query.message is None:
        return

    technical_analysis_text = textwrap.dedent(
        """
        **Start Analyzing!**

        To begin your analysis, simply type the symbol of the coin you're interested in (e.g., BTC, ETH, etc.) and 
        we'll provide you with detailed insights✨

        _Example: /ta bnb_
        """
    )
    market_analysis_text = textwrap.dedent(
        """
        **Market Analyze!**

        To analyze the market, simply type the symbol of the coin you're interested in (e.g., BTC, ETH, etc.) and 
        we'll provide you with detailed insights✨

        _Example: /analyze bnb_
        """
    )
    moving_average_text = textwrap.dedent(
        """
        **Moving Average!**

        Type the coin symbol you want to analyze (e.g., BTC, ETH, etc.) We'll provide an in-depth analysis of its 
        price action, trend patterns, and potential market movements based on Moving Averages and other technical 
        indicators. 🚥

        _Example: /ma bnb_
        """
    )
    fear_greed_text = textwrap.dedent(
        """
        **Fear & Greed!**
        
        The Fear & Greed Index is a tool that helps you gauge the market sentiment. It's a great way to understand
        the market's mood and make better decisions. 🧭
        
        _Example: /fg_
        """
    )
    help_text = textwrap.dedent(
        """
        **Help 🤷‍♂️**

        ERC-AI is your intelligent assistant designed to help you better understand the market✨

        Featured:
        Market Analyze 📌 
        Moving Average 🚥
        Fear & Greed 🧭 
        Help 🤷‍♂️

        If you need help, type /help to view a full list of commands and capabilities.
        """
    )

    data = query.data
    if data == "technical_analyze":
        await query.message.answer(
            telegramify_markdown.markdownify(technical_analysis_text),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    elif data == "market_analyze":
        await query.message.answer(
            telegramify_markdown.markdownify(market_analysis_text),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    elif data == "moving_average":
        await query.message.answer(
            telegramify_markdown.markdownify(moving_average_text),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    elif data == "fear_greed":
        await query.message.answer(
            telegramify_markdown.markdownify(fear_greed_text),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    elif data == "help":
        await query.message.answer(
            telegramify_markdown.markdownify(help_text),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    await query.answer()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    username = message.from_user.username if message.from_user else "User"
    text = textwrap.dedent(f"""    
        Welcome **{username}** To ERC-AI

        ERC-AI is your intelligent assistant designed to help you better understand the market✨

        Featured:
        Market Analyze 📌 
        Moving Average 🚥
        Fear & Greed 🧭 
        Help 🤷‍♂️

        If you need help, type /help to view a full list of commands and capabilities.""")

    converted = telegramify_markdown.markdownify(
        text,
    )

    await message.answer(
        converted, reply_markup=inline_keyboards, parse_mode=ParseMode.MARKDOWN_V2
    )


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    text = textwrap.dedent(
        """
        *Available Commands:*
        /start - Start the bot.
        /analyze <coin> - Analyze the intrinsic value of the selected coin.
        /ta <coin> - Capture and analyze a 1-month candlestick chart.
        /ma <coin> - Perform Moving Averages Analysis on the selected coin.
        /fg - Perform Fear & Greed analysis.
        """
    )

    converted = telegramify_markdown.markdownify(
        text,
    )

    await message.answer(converted, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message(Command("analyze"))
async def command_analyze_handler(message: Message) -> None:
    if message.text is None:
        return

    args = message.text.split()
    if len(args) > 1:
        coin_name = args[1]

        res = load_json("cmc_list.json")

        if res is None:
            await message.answer("Coin not found")
            return

        finder = CoinFinder(res["data"])
        coin = finder.find_coin(coin_name)

        if coin is None:
            await message.answer("Coin not found")
            return

        loading_msg = await message.answer(f"Analyzing {coin['name']}...")

        result = MarketAnalysisCrew(coin=coin["slug"]).crew().kickoff()

        converted = telegramify_markdown.markdownify(
            str(result),
        )

        await loading_msg.edit_text(converted, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await message.answer("Please provide the coin symbol.")


@dp.message(Command("ta"))
async def command_ta_handler(message: Message) -> None:
    if message.text is None:
        return

    args = message.text.split()
    if len(args) > 1:
        coin_name = args[1]

        res = load_json("cmc_list.json")

        if res is None:
            await message.answer("Coin not found")
            return

        finder = CoinFinder(res["data"])
        coin = finder.find_coin(coin_name)

        if coin is None:
            await message.answer("Coin not found")
            return

        loading_msg = await message.answer(
            f"Performing technical analysis for {coin['name']}..."
        )

        result = TechnicalAnalysisCrew(coin=coin["symbol"]).crew().kickoff()

        image_path = os.path.join(os.path.dirname(__file__), "coin_screenshot.jpeg")
        if os.path.exists(image_path):
            photo = types.FSInputFile(path=image_path)
        else:
            photo = None

        converted = telegramify_markdown.markdownify(
            str(result),
        )

        await loading_msg.edit_text("Analysis complete. Check the image below.")
        if photo:
            await message.answer_photo(photo=photo)
        await message.answer(converted, parse_mode=ParseMode.MARKDOWN_V2)

        # remove the image
        if os.path.exists(image_path):
            os.remove(image_path)
    else:
        await message.answer("Please provide the coin symbol.")


@dp.message(Command("ma"))
async def command_ma_handler(message: Message) -> None:
    if message.text is None:
        return

    args = message.text.split()
    if len(args) > 1:
        coin_name = args[1]

        res = load_json("cmc_list.json")

        if res is None:
            await message.answer("Coin not found")
            return

        finder = CoinFinder(res["data"])
        coin = finder.find_coin(coin_name)

        if coin is None:
            await message.answer("Coin not found")
            return

        loading_msg = await message.answer(
            f"Performing moving average analysis for {coin['name']}..."
        )
        result = MovingAverageCrew(coin=coin["symbol"]).crew().kickoff()

        image_path = os.path.join(os.path.dirname(__file__), "sma.jpeg")
        if os.path.exists(image_path):
            photo = types.FSInputFile(path=image_path)
        else:
            photo = None

        converted = telegramify_markdown.markdownify(
            str(result),
        )

        await loading_msg.edit_text("Analysis complete. Check the image below.")
        if photo:
            await message.answer_photo(photo=photo)
        await message.answer(converted, parse_mode=ParseMode.MARKDOWN_V2)

        # remove the image
        if os.path.exists(image_path):
            os.remove(image_path)
    else:
        await message.answer("Please provide the coin symbol.")


@dp.message(Command("fg"))
async def command_fg_handler(message: Message) -> None:
    loading_msg = await message.answer("Performing Fear & Greed analysis...")
    result = FGIndexCrew().crew().kickoff()

    image_path = os.path.join(os.path.dirname(__file__), "fg.jpeg")
    if os.path.exists(image_path):
        photo = types.FSInputFile(path=image_path)
    else:
        photo = None

    converted = telegramify_markdown.markdownify(
        str(result),
    )

    await loading_msg.edit_text("Analysis complete. Check the image below.")
    if photo:
        await message.answer_photo(photo=photo)
    await message.answer(converted, parse_mode=ParseMode.MARKDOWN_V2)

    if os.path.exists(image_path):
        os.remove(image_path)


async def main() -> None:
    agentops.init()

    if TELEGRAM_TOKEN is None:
        raise ValueError("Telegram token is not provided.")

    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
