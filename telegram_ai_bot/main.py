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
# Initialize database
from .database import init_db, get_user, consume_credit, add_credits
init_db()

# Initialize AI Engine
ai_engine = AIEngine()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    user = update.effective_user
    user_data = get_user(user.id)
    credits = user_data["credits"]
    
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
    user_id = update.effective_user.id
    # In a production app, you would create a Stripe Checkout Session via API here:
    # stripe.checkout.Session.create(
    #     client_reference_id=str(user_id),
    #     success_url="https://t.me/YourBotName",
    #     ...
    # )
    # And then a web server handles the Stripe Webhook to call database.upgrade_user(user_id)
    buy_text = (
        "💎 *Upgrade to Premium*\n\n"
        "Unlock unlimited AI access and priority processing speed.\n\n"
        "💳 *Subscription Options:*\n"
        "• 1 Month: $9.99\n"
        "• 1 Year: $89.99 (Save 25%)\n\n"
        f"👉 [Click here to pay securely via Stripe (https://buy.stripe.com/test_premium?client_reference_id={user_id})](#)\n\n"
        "*(Once paid, our webhook will upgrade your account instantly)*"
    )
    await update.message.reply_text(buy_text, parse_mode="Markdown")


async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /credits command."""
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    if user_data["is_premium"]:
        await update.message.reply_text("💎 You have an active Premium Subscription (Unlimited).")
    else:
        await update.message.reply_text(f"🔋 You have {user_data['credits']} free messages remaining.\nUse /buy to get unlimited access.")


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

    user_data = get_user(user_id)
    remaining = user_data["credits"]
    is_premium = user_data["is_premium"]
    
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
        if is_premium:
            footer = ""
        elif remaining > 0:
            footer = f"\n\n_({remaining} free messages left)_"
        else:
            footer = f"\n\n_(This was your last free message! Type /buy)_"
            
        await update.message.reply_text(response + footer, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Sorry, I encountered an error processing your request.\nError: {e}")
        # Refund the credit on error
        add_credits(user_id, 1)


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
