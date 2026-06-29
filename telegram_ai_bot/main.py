import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# We will reuse the moneymaker AI engine for the bot's intelligence.
# Adding parent directory to sys.path to import moneymaker modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from money_maker.core.ai_engine import AIEngine

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MAX_FREE_CREDITS = 3

# In-memory database for tracking user credits
# In a real app, use PostgreSQL or SQLite
user_credits = {}

# Initialize AI Engine
ai_engine = AIEngine()


def get_user_credits(user_id: int) -> int:
    """Get remaining credits for a user."""
    if user_id not in user_credits:
        user_credits[user_id] = MAX_FREE_CREDITS
    return user_credits[user_id]


def consume_credit(user_id: int) -> bool:
    """Consume a credit. Returns True if successful, False if out of credits."""
    credits = get_user_credits(user_id)
    if credits > 0:
        user_credits[user_id] -= 1
        return True
    return False


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    user = update.effective_user
    credits = get_user_credits(user.id)
    
    welcome_message = (
        f"👋 Hello {user.first_name}!\n\n"
        f"I am your Premium AI Assistant. I can help you write code, draft emails, answer questions, and solve problems.\n\n"
        f"🎁 You have {credits} free messages remaining.\n"
        f"Type /help to see all commands."
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    help_text = (
        "🤖 *Premium AI Assistant Commands*\n\n"
        "/start - Welcome message and status\n"
        "/help - Show this help message\n"
        "/buy - Purchase a premium subscription\n"
        "/credits - Check your remaining balance\n\n"
        "Just send me any message to chat!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /buy command (Mock monetization)."""
    buy_text = (
        "💎 *Upgrade to Premium*\n\n"
        "Unlock unlimited AI access and priority processing speed.\n\n"
        "💳 *Subscription Options:*\n"
        "• 1 Month: $9.99\n"
        "• 1 Year: $89.99 (Save 25%)\n\n"
        "👉 [Click here to pay securely via Stripe (Mock Link)](#)\n\n"
        "*(Once paid, your account will be upgraded instantly)*"
    )
    await update.message.reply_text(buy_text, parse_mode="Markdown")


async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /credits command."""
    user_id = update.effective_user.id
    credits = get_user_credits(user_id)
    await update.message.reply_text(f"🔋 You have {credits} free messages remaining.\nUse /buy to get unlimited access.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages and route to AI."""
    user_id = update.effective_user.id
    text = update.message.text

    # Check credits
    if not consume_credit(user_id):
        await update.message.reply_text(
            "🚫 *Out of Free Credits!*\n\n"
            "You have used all your free messages. Please upgrade to continue using the AI.\n"
            "Type /buy to view subscription options.",
            parse_mode="Markdown"
        )
        return

    remaining = get_user_credits(user_id)
    
    # Send "typing" action to Telegram
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Use our MoneyMaker AIEngine to generate a response
        # We'll use the generate_content method as a generic chat response for now
        response = ai_engine._client.chat.completions.create(
            model=ai_engine.model,
            messages=[{"role": "user", "content": text}],
            max_tokens=500
        ).choices[0].message.content
        
        # Append a small credit reminder
        if remaining > 0:
            footer = f"\n\n_({remaining} free messages left)_"
        else:
            footer = f"\n\n_(This was your last free message! Type /buy)_"
            
        await update.message.reply_text(response + footer, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Sorry, I encountered an error processing your request.\nError: {e}")
        # Refund the credit on error
        user_credits[user_id] += 1


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and send a telegram message to notify the developer."""
    print(f"Exception while handling an update: {context.error}")


def main():
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN is not set in the .env file.")
        print("Please message @BotFather on Telegram to get a token.")
        return

    print("🤖 Starting Telegram AI Bot...")
    
    # Create the Application and pass it your bot's token.
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("buy", buy_command))
    app.add_handler(CommandHandler("credits", credits_command))

    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add error handler
    app.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    print("✅ Bot is running! Press Ctrl-C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
