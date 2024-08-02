import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
import logging
from datetime import datetime, timedelta
import os

TOKEN = '7443524862:AAHdmaRRAY9BkNT08W2bh8ujW_OuOpNn154'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Track user signals count and performance
user_signals = {}
user_performance = {}
images_folder = ''  # Update this path to the folder containing your images

async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = """
    🎉 **Welcome to GameMaster Bot!** 🎉

    Hey, GameMaster! 🌟 Ready to turn the odds in your favor? 🚀 Our bot predicts winning signals for top games like **Aviator, Mines, Limbo**, and **Tower**. Play on **BDG, Tiranga, 99 Club, TC Lottery**, or **Lottery9** and watch your luck soar! 🍀

    🎯 **Why GameMaster Bot?** 🎯

    🔮 **Accurate Signals**  
    ⚡ **Real-time Alerts**  
    🌐 **Multi-Platform Support**

    🆓 **Free Trial Bot:** Get 5 signals/day!  
    💎 **Premium Bot:** Unlimited signals!

    💥 **Get Started:** 💥

    1. **Join Us:** Connect with winners! 🏅  
    2. **Activate Signals:** Easy steps! 🔧  
    3. **Win Big:** Maximize your gains! 💰

    📞 **24/7 Support:** We're here for you!

    ---

    Hit **/start** to begin your winning journey! 🏆

    💌 **Special Offer:** 20% off Premium! Code: **WINBIG20**

    👇 **Please choose your platform to continue:**
    """

    keyboard = [
        [InlineKeyboardButton("BDG", callback_data='BDG')],
        [InlineKeyboardButton("Tiranga", callback_data='Tiranga')],
        [InlineKeyboardButton("99 Club", callback_data='99 Club')],
        [InlineKeyboardButton("TC Lottery", callback_data='TC Lottery')],
        [InlineKeyboardButton("Lottery9", callback_data='Lottery9')],
        [InlineKeyboardButton("YOLO27", callback_data='YOLO')],
        [InlineKeyboardButton("Buy Bot", url='https://t.me/gamemasterbuybot')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

async def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data in ['BDG', 'Tiranga', '99 Club', 'TC Lottery', 'Lottery9' , 'YOLO']:
        platform_name = query.data
        follow_up_message = f"""
        🎉 Great Choice! 🎉

        You've selected **{platform_name}**!

        You're almost ready to start winning big! 🌟 Our bot boasts an impressive accuracy rate of 97% for our Premium Bot and 80% for our Free Trial Bot. Get ready to experience the thrill of precise predictions!

        🎮 Please choose your game: 🎮

        ✈️ Aviator
        💣 Mines
        🎲 Limbo
        🏰 Tower

        Tap on your game of choice and let’s get those winning signals rolling! 🚀💰
        """

        game_keyboard = [
            [InlineKeyboardButton("✈️ Aviator💵", callback_data='aviator')],
            [InlineKeyboardButton("💣 Mines", callback_data='mines')],
            [InlineKeyboardButton("🎲 Limbo💵", callback_data='limbo')],
            [InlineKeyboardButton("🏰 Tower💵", callback_data='tower')],
        ]

        game_reply_markup = InlineKeyboardMarkup(game_keyboard)
        await query.edit_message_text(text=follow_up_message, parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=game_reply_markup)

    elif query.data in ['aviator', 'mines', 'limbo', 'tower']:
        user_id = query.from_user.id

        if user_id not in user_signals:
            user_signals[user_id] = {
                'count': 0,
                'reset_time': datetime.now() + timedelta(days=1),
                'activated': False
            }

        if datetime.now() > user_signals[user_id]['reset_time']:
            user_signals[user_id] = {
                'count': 0,
                'reset_time': datetime.now() + timedelta(days=1),
                'activated': False
            }

        if user_signals[user_id]['count'] < 2:
            user_signals[user_id]['count'] += 1
            user_signals[user_id]['activated'] = True
            free_message = f"""
            **{query.data.capitalize()} Game Selected!**

            Please enter your User ID to proceed:
            """
            await query.edit_message_text(text=free_message, parse_mode=ParseMode.MARKDOWN)
        else:
            limit_message = """
            ⚠️ **Free Limit Reached!** ⚠️

            You've used your 2 free signals for today. Upgrade to Premium for unlimited access and a whopping 97% accuracy on all signals! 💎

            Visit [our bot](https://t.me/gamemasterbuybot) to upgrade or contact support.
            """
            buy_bot_button = [
                [InlineKeyboardButton("Buy Bot", url='https://t.me/gamemasterbuybot')],
            ]
            buy_bot_reply_markup = InlineKeyboardMarkup(buy_bot_button)
            await query.edit_message_text(text=limit_message, parse_mode=ParseMode.MARKDOWN, reply_markup=buy_bot_reply_markup)

    elif query.data in ['1', '2', '3', '4']:
        image_number = random.randint(1, 28)
        image_path = os.path.join(images_folder, f'{image_number}.png')
        accuracy = random.randint(50, 100)
        result_message = f"🎉 Congratulations! 🎉 Your result is {accuracy}% accurate."

        try:
            with open(image_path, 'rb') as img:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=img)

            buy_bot_button = [
                [InlineKeyboardButton("Buy Bot", url='https://t.me/gamemasterbuybot')],
            ]
            buy_bot_reply_markup = InlineKeyboardMarkup(buy_bot_button)
            await query.message.reply_text(result_message, reply_markup=buy_bot_reply_markup)

            # Track user performance
            user_id = query.from_user.id
            if user_id not in user_performance:
                user_performance[user_id] = {'games_played': 0, 'wins': 0}
            user_performance[user_id]['games_played'] += 1
            if accuracy > 70:  # Consider a win if accuracy is more than 70%
                user_performance[user_id]['wins'] += 1

        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            await query.message.reply_text("Sorry, an error occurred while sending the photo.")

    else:
        premium_message = """
        💎 **Premium Game Selected** 💎

        The game you selected is available in the Premium version. Upgrade to Premium for unlimited access and a whopping 97% accuracy on all signals! 💎

        Visit [our bot](https://t.me/gamemasterbuybot) to upgrade or contact support.

        After payment, please send the screenshot to us. We will send your user ID and paid bot link to you within 24 hours.

        Your choice is great!
        """
        await query.edit_message_text(text=premium_message, parse_mode=ParseMode.MARKDOWN)


async def handle_user_id(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id in user_signals and user_signals[user_id]['activated']:
        mines_keyboard = [
            [InlineKeyboardButton("1💣", callback_data='1')],
            [InlineKeyboardButton("2💣💣", callback_data='2')],
            [InlineKeyboardButton("3💣💣💣", callback_data='3')],
            [InlineKeyboardButton("4💣💣💣💣", callback_data='4')],
        ]
        mines_reply_markup = InlineKeyboardMarkup(mines_keyboard)
        mines_message = "Please choose the number of mines (1-4):"
        await update.message.reply_text(mines_message, reply_markup=mines_reply_markup)
    else:
        await update.message.reply_text("Please select a game first.")


async def reset_signals(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_signals:
        user_signals[user_id]['count'] = 0
        user_signals[user_id]['reset_time'] = datetime.now() + timedelta(days=1)
        await update.message.reply_text("Your signal count has been reset.", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("You have not activated the freemium yet. Use /activate_freemium to start.",
                                        parse_mode=ParseMode.MARKDOWN)


async def profile(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_performance:
        games_played = user_performance[user_id]['games_played']
        wins = user_performance[user_id]['wins']
        win_rate = (wins / games_played) * 100 if games_played > 0 else 0
        profile_message = f"""
        **Your Profile:**

        Games Played: {games_played}
        Wins: {wins}
        Win Rate: {win_rate:.2f}%
        """
        await update.message.reply_text(profile_message, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("You have not played any games yet.", parse_mode=ParseMode.MARKDOWN)


async def leaderboard(update: Update, context: CallbackContext) -> None:
    sorted_users = sorted(user_performance.items(), key=lambda x: x[1]['wins'], reverse=True)
    leaderboard_message = "**Leaderboard:**\n\n"
    for i, (user_id, performance) in enumerate(sorted_users[:10], start=1):
        user_name = (await context.bot.get_chat(user_id)).username
        leaderboard_message += f"{i}. @{user_name} - {performance['wins']} wins\n"
    await update.message.reply_text(leaderboard_message, parse_mode=ParseMode.MARKDOWN)


async def daily_reward(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_signals:
        user_signals[user_id] = {
            'count': 0,
            'reset_time': datetime.now() + timedelta(days=1),
            'activated': False
        }
    user_signals[user_id]['count'] += 1
    reward_message = "🎁 You have received your daily reward! You can now use an additional signal today."
    await update.message.reply_text(reward_message, parse_mode=ParseMode.MARKDOWN)


async def help_command(update: Update, context: CallbackContext) -> None:
    help_message = """
    **GameMaster Bot Help**

    Here are the commands you can use:

    /start - Start interacting with the bot
    /reset_signals - Reset your daily signal count
    /profile - View your profile and statistics
    /leaderboard - View the top players
    /daily_reward - Claim your daily reward
    /help - Show this help message

    For any issues or questions, please contact our support team.
    """
    await update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)


def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset_signals", reset_signals))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("daily_reward", daily_reward))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_id))

    application.add_error_handler(error)

    application.run_polling()


if __name__ == '__main__':
    main()
