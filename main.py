# import os
# import requests
# from dotenv import load_dotenv
# import chainlit as cl


# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Define a mapping of coin symbols to their names and IDs
# COIN_MAP = {
#     "BTC": ["BTC", "BITCOIN"],
#     "ETH": ["ETH", "ETHEREUM"],
#     "DOGE": ["DOGE", "DOGECOIN"],
#     "SOL": ["SOL", "SOLANA"],
#     "ADA": ["ADA", "CARDANO"],
#     "XRP": ["XRP", "RIPPLE"],
#     "MATIC": ["MATIC", "POLYGON"],
#     "BNB": ["BNB", "BINANCE", "BINANCE COIN"]
# }

# COIN_EMOJIS = {
#     "BTC": "🟠",
#     "ETH": "🟣",
#     "DOGE": "🐶",
#     "SOL": "🌞",
#     "ADA": "🔷",
#     "XRP": "💧",
#     "MATIC": "🔺",
#     "BNB": "🟡"
# }

# COIN_IDS = {
#     "BTC": "90",
#     "ETH": "80",
#     "DOGE": "2",
#     "SOL": "48543",
#     "ADA": "257",
#     "XRP": "58",
#     "MATIC": "3890",
#     "BNB": "2710"
# }

# def detect_coin(user_input: str) -> str | None:
#     user_input = user_input.upper()
#     for symbol, keywords in COIN_MAP.items():
#         if any(keyword in user_input for keyword in keywords):
#             return symbol
#     return None

# def fetch_price(symbol: str) -> str:
#     coin_id = COIN_IDS.get(symbol.upper())
#     emoji = COIN_EMOJIS.get(symbol.upper(), "💰")
#     if not coin_id:
#         return "❌ Unsupported coin. Try Bitcoin or Ethereum."

#     try:
#         url = f"https://api.coinlore.net/api/ticker/?id={coin_id}"
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()[0]

#         name = data["name"]
#         symbol = data["symbol"]
#         price = float(data["price_usd"])
#         change_percent = float(data["percent_change_24h"])
#         price_change = price * (change_percent / 100)
#         market_cap = float(data["market_cap_usd"])


#         # Trend icon
#         trend_icon = "📈" if change_percent >= 0 else "📉"
#         sign = "+" if price_change >= 0 else "–"

#         return (
#             f"{emoji} **{name}** ({symbol}) is currently priced at **${price:,.4f} USD**. {trend_icon}\n"
#             f"{trend_icon} **24h Change:** **{sign}${abs(price_change):,.4f} ({change_percent:+.2f}%)**\n"
#             f"**💼 Market Cap:** **${market_cap:,.0f} USD**"
#         )

#     except Exception as e:
#         return f"⚠️ Error fetching price: {str(e)}"

# @cl.on_chat_start
# async def start():
#     await cl.Message(
#         content=
#          "👋 **Welcome to CryptoDataAgent!**\n\n"
#             "💡 You can ask me about the latest crypto prices using natural language. For example:\n"
#             "- *What's the price of Bitcoin?*\n"
#             "- *Show me the current ETH rate*\n"
#             "- *Tell me how much Dogecoin is worth*\n"
#             "- *Give me the value of Solana or ADA*\n\n"
#             "Just ask, and I'll fetch the latest price for you! 🚀"
#     ).send()


# @cl.on_message
# async def handle_user(message: cl.Message):
#     user_input = message.content.strip()
#     symbol = detect_coin(user_input)

#     if symbol:
#         reply = fetch_price(symbol)
#     else:
#         reply = "🤖 Please mention Bitcoin or Ethereum to get the current price."

#     await cl.Message(content=reply).send()

import os
import requests
from dotenv import load_dotenv
import chainlit as cl
from datetime import datetime

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Coin mappings
COIN_MAP = {
    "BTC": ["BTC", "BITCOIN"],
    "ETH": ["ETH", "ETHEREUM"],
    "DOGE": ["DOGE", "DOGECOIN"],
    "SOL": ["SOL", "SOLANA"],
    "ADA": ["ADA", "CARDANO"],
    "XRP": ["XRP", "RIPPLE"],
    "MATIC": ["MATIC", "POLYGON"],
    "BNB": ["BNB", "BINANCE", "BINANCE COIN"]
}

COIN_EMOJIS = {
    "BTC": "🟠",
    "ETH": "🟣",
    "DOGE": "🐶",
    "SOL": "🌞",
    "ADA": "🔷",
    "XRP": "💧",
    "MATIC": "🔺",
    "BNB": "🟡"
}

COIN_IDS = {
    "BTC": "90",
    "ETH": "80",
    "DOGE": "2",
    "SOL": "48543",
    "ADA": "257",
    "XRP": "58",
    "MATIC": "3890",
    "BNB": "2710"
}


def detect_all_coins(user_input: str) -> list[str]:
    user_input = user_input.upper()
    detected = []
    for symbol, keywords in COIN_MAP.items():
        if any(keyword in user_input for keyword in keywords):
            detected.append(symbol)
    return list(set(detected)) 


def fetch_price(symbol: str) -> str:
    coin_id = COIN_IDS.get(symbol.upper())
    emoji = COIN_EMOJIS.get(symbol.upper(), "💰")
    if not coin_id:
        return f"❌ Unsupported coin: {symbol}"

    try:
        url = f"https://api.coinlore.net/api/ticker/?id={coin_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()[0]

        name = data["name"]
        symbol = data["symbol"]
        price = float(data["price_usd"])
        change_percent = float(data["percent_change_24h"])
        price_change = price * (change_percent / 100)
        market_cap = float(data["market_cap_usd"])

        high = price * 1.03
        low = price * 0.97
        
        trend_icon = "📈" if change_percent >= 0 else "📉"
        sign = "+" if price_change >= 0 else "–"
        last_updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

        return (
            f"{emoji} **{name}** ({symbol}) is currently priced at **${price:,.4f} USD**. {trend_icon}\n"
            f"{trend_icon} **24h Change:** **{sign}${abs(price_change):,.4f} ({change_percent:+.2f}%)**\n"
            f"📈 **High (est.):** ${high:,.4f} | 📉 **Low (est.):** ${low:,.4f}\n"
            f"💼 **Market Cap:** **${market_cap:,.0f} USD**\n"
            f"🕒 **Last updated:** {last_updated}"
        )

    except Exception as e:
        return f"⚠️ Error fetching price for {symbol}: {str(e)}"


@cl.on_chat_start
async def start():
    await cl.Message(
        content=
        "👋 **Welcome to CryptoDataAgent!**\n\n"
        "💡 You can ask about the latest crypto prices like:\n"
        "- *What's the price of Bitcoin?*\n"
        "- *Show me ETH and DOGE prices*\n"
        "- *Give me the value of ADA, MATIC, and XRP*\n\n"
        "🔧 Type `/help` for more instructions. 🚀"
    ).send()


@cl.on_message
async def handle_user(message: cl.Message):
    user_input = message.content.strip()

    # Help command
    if user_input.lower() == "/help":
        reply = (
            "🛠️ **CryptoDataAgent Commands:**\n\n"
            "- 🔎 *Ask for price info:* e.g., *What’s the price of ETH?*\n"
            "- 💬 *Ask multiple coins at once:* *BTC, ETH, DOGE*\n"
            "- 💡 *Supported Coins:* BTC, ETH, SOL, ADA, XRP, DOGE, MATIC, BNB\n"
            "- 📌 *Use `/help`* to see this message again\n\n"
            "✨ *More features coming soon!*"
        )
        await cl.Message(content=reply).send()
        return

    # Detect coins in the message
    symbols = detect_all_coins(user_input)

    if symbols:
        reply = "\n\n".join([fetch_price(sym) for sym in symbols])
    else:
        reply = (
            "🤖 I couldn't detect any supported coins in your message.\n"
            "✅ Try asking about: BTC, ETH, SOL, ADA, XRP, DOGE, MATIC, BNB.\n"
            "ℹ️ Example: *What's the price of Ethereum and Solana?*"
        )

    await cl.Message(content=reply).send()
