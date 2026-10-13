import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from google import genai

# Enable Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "7769910515:AAFYC51mP05N5jVIn00C3IeI6v0qO190_eI"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # এখানে আপনার আসল Gemini API Key বসাবেন

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# --- START COMMAND & MAIN MENU ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"السلام عليكم {user_name}! 👋\n\n"
        f"স্বাগতম **Kamran AI Help BD** বোটে!\n"
        f"আমি আপনার ২৪/৭ অল-ইন-ওয়ান সহকারী। নিচের যেকোনো বাটন চাপুন অথবা সরাসরি যেকোনো প্রশ্ন লিখে পাঠান:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🚨 জরুরি সেবাসমূহ (Emergency)", callback_data='emergency')],
        [InlineKeyboardButton("📶 ওয়াইফাই হেল্প (Wi-Fi Guide)", callback_data='wifi')],
        [InlineKeyboardButton("🤖 এআই অ্যাসিস্ট্যান্ট (Gemini AI)", callback_data='ai_help')],
        [InlineKeyboardButton("👨‍💻 ডেভলপার তথ্য (Developer)", callback_data='developer')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# --- BUTTON CLICK HANDLER ---
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'emergency':
        text = (
            "🚨 **জরুরি সেবাসমূহ (বাংলাদেশ):**\n\n"
            "• **জাতীয় জরুরি সেবা (পুলিশ, ফায়ার সার্ভিস, অ্যাম্বুলেন্স):** 999\n"
            "• **নারী ও শিশু নির্যাতন প্রতিরোধ সেল:** 109\n"
            "• **সরকারি তথ্য ও সেবা সহায়তা:** 333\n"
            "• **দুর্নীতি দমন কমিশন (দুদক):** 106\n"
            "• **দুর্যোগের আগাম বার্তা ও সহায়তা:** 1090\n\n"
            "💡 যেকোনো অনাকাঙ্ক্ষিত পরিস্থিতিতে সরাসরি ওপরের নম্বরগুলোতে কল করুন।"
        )
    elif query.data == 'wifi':
        text = (
            "📶 **ওয়াইফাই সমস্যার সমাধান গাইড:**\n\n"
            "১. **ইন্টারনেট কানেকশন না থাকলে:** রাউটার ও অনু (ONU) এর পাওয়ার সুইচ বন্ধ করে ২ মিনিট পর আবার চালু করুন (Restart)।\n"
            "২. **ইন্টারনেট স্পিড কম থাকলে:** রাউটারে কতগুলো ডিভাইস কানেক্টেড আছে চেক করুন এবং অপ্রয়োজনীয় ডিভাইস ডিসকানেক্ট করুন।\n"
            "৩. **ওয়াইফাই পাসওয়ার্ড/লগইন সমস্যা:** রাউটারের পেছনে থাকা রিসেট বাটন ১০ সেকেন্ড চেপে ধরে পুনরায় সেটআপ করুন অথবা আপনার আইএসপি (ISP) প্রোভাইডারের সাথে যোগাযোগ করুন।"
        )
    elif query.data == 'ai_help':
        text = (
            "🤖 **Gemini এআই সহকারী:**\n\n"
            "আপনার যেকোনো প্রশ্ন (পড়াশোনা, প্রযুক্তি, সাধারণ জ্ঞান, অনুবাদ ইত্যাদি) মেসেজ বক্সে লিখে পাঠান। এআই দ্রুত সঠিক উত্তর প্রদান করবে।"
        )
    elif query.data == 'developer':
        text = (
            "👨‍💻 **ডেভলপার ও ক্রিয়েটর ক্রেডিট:**\n\n"
            "• **বটের নাম:** Kamran AI Help BD\n"
            "• **নির্মাতা:** Kamran Hasan (کامران حسن)\n"
            "• **লক্ষ্য:** ২৪ ঘণ্টা বিনামূল্যে বাংলা ভাষায় জরুরি ও আধুনিক এআই সেবা প্রদান করা।"
        )
    
    keyboard = [[InlineKeyboardButton("⬅️ মূল মেনু (Main Menu)", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query.data == 'main_menu':
        await start(update, context)
    else:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# --- AI TEXT CHAT HANDLER ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.chat.send_action("typing")
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
        )
        ai_reply = response.text
        await update.message.reply_text(ai_reply)
    except Exception as e:
        await update.message.reply_text("দুঃখিত, কোনো যান্ত্রিক সমস্যা হয়েছে। অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।")

# --- MAIN EXECUTION ---
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
