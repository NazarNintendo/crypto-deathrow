import io
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from dotenv import load_dotenv
from telegram import Update, InputFile
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()

DAYS_IN_YEAR = 365
STATUS_QUO = "Status Quo"


class Result:
    def __init__(
            self,
            status_quo_return: np.float64,
            highest_potential_return: np.float64,
            best_platform: str,
            picture_bytes: bytes
    ) -> None:
        self.status_quo_return = status_quo_return
        self.highest_potential_return = highest_potential_return
        self.best_platform = best_platform
        self.picture_bytes = picture_bytes

    def __str__(self) -> str:
        return (
            f"✨ *Optimization Result* ✨\n\n"
            f"💼 *Status Quo Return:* `${self.status_quo_return:.2f}`\n"
            f"🚀 *Highest Projected Return:* `${self.highest_potential_return:.2f}`\n\n"
            f"🏆 *Best Platform:* `{self.best_platform}`\n\n"
            f"💡 _Ready to maximize your returns?_"
        )


def optimize_funds(platforms: np.ndarray, balances: np.ndarray, APRs: np.ndarray, transfer_fee_matrix: np.ndarray) -> Result:
    # --------------- CALCULATION ---------------

    daily_APRs = APRs / DAYS_IN_YEAR
    total_balance = np.sum(balances)
    status_quo_return = np.sum(balances * daily_APRs)

    applicable_fees = transfer_fee_matrix * (balances > 0)[:, np.newaxis]
    transfer_costs = np.sum(applicable_fees, axis=0)
    net_balances = total_balance - transfer_costs
    potential_returns = net_balances * daily_APRs

    x = [STATUS_QUO, *platforms]
    y = [status_quo_return, *potential_returns]

    highest_return_idx = np.argmax(y)
    highest_potential_return = y[highest_return_idx]
    best_platform = x[highest_return_idx]

    result = status_quo_return, highest_potential_return, best_platform

    # --------------- PLOTTING ---------------

    plt.figure(figsize=(10, 6))
    sns.set(style="darkgrid")
    plt.style.use("dark_background")
    plt.rcParams.update({"grid.linewidth": 0.5, "grid.alpha": 0.5})
    barplot = sns.barplot(x=x, y=y, palette='viridis', hue=x, legend=False)
    barplot.set_title("Projected Returns after Consolidating Funds", fontsize=18, fontweight='bold')
    barplot.set_ylabel("Projected Return ($) daily", fontsize=14, fontweight='bold')
    barplot.set_xlabel("Platform", fontsize=14, fontweight='bold')

    def get_font_size(idx: int) -> tuple[int, int]:
        if idx == highest_return_idx:
            return 36
        else:
            return 20

    for idx, i in enumerate(barplot.containers):
        size = get_font_size(idx)
        barplot.bar_label(i, label_type='center', fmt='%.2f', color='white', size=size, weight='bold')

    sns_figure = barplot.get_figure()
    buf = io.BytesIO()
    sns_figure.savefig(buf, format='png')
    buf.seek(0)
    picture_bytes = buf.read()
    barplot.clear()

    return Result(*result, picture_bytes)


async def start(update: Update, context):
    await update.message.reply_text(
        "👋 *Hello there\!*\n\n"
        "I'm here to help you optimize your funds\! 🚀✨\n\n"
        "📥 Send me your platforms, balances, APRs, and transfer fee matrix in JSON format\.\n\n"
        "💡 Here's an example to get you started:\n"
        "```json\n"
        "{\n"
        "  \"platforms\": [\"Platform1\", \"Platform2\", \"Platform3\"],\n"
        "  \"balances\": [1234.56, 7890.12, 3456.78],\n"
        "  \"APRs\": [0.12, 0.34, 0.56],\n"
        "  \"transfer_fee_matrix\": [\n"
        "    [0, 1.5, 2.0],\n"
        "    [1.5, 0, 1.8],\n"
        "    [2.0, 1.8, 0]\n"
        "  ]\n"
        "}\n"
        "```\n"
        "📊 Let's crunch some numbers and find the best platform for you\! 🏆",
        parse_mode=ParseMode.MARKDOWN_V2
    )


async def handle_message(update: Update, context):
    try:
        data = json.loads(update.message.text)
        platforms = data["platforms"]
        balances = np.array(data["balances"])
        APRs = np.array(data["APRs"])
        transfer_fee_matrix = np.array(data["transfer_fee_matrix"])

        result = optimize_funds(platforms, balances, APRs, transfer_fee_matrix)

        await update.message.reply_text(str(result), parse_mode=ParseMode.MARKDOWN_V2)
        await update.message.reply_photo(photo=InputFile(result.picture_bytes, filename="result.png"))
    except Exception as e:
        await context.bot.send_message(update.effective_chat.id, f"An error occurred: {e}")


def main():
    bot_api_token = os.getenv("BOT_TOKEN")

    application = Application.builder().token(bot_api_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
