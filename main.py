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
TELEGRAM_BOT_TOKEN = "8880704616:AAFQMTk0TMj7sManEPdoJIbCOK9UoKZO-JM"
GEMINI_API_KEY = "AQ.Ab8RN6JLYs5EMt7zqgCdWUzmqVgpmzM8V1FPBgJnSbN4nJWIwg"

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# --- START COMMAND & MAIN MENU ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name if update.effective_user else "বন্ধু"
    welcome_text = (
        f"السلام عليكم {user_name}! 👋\n\n"
        f"স্বাগতম **সুনামগঞ্জ জেলা জরুরি হেল্পলাইন ও এআই** বোটে! 🚨\n"
        f"আমি আপনার ২৪/৭ ডিজিটাল সহকারী। নিচের বাটনগুলো ব্যবহার করুন অথবা সরাসরি নির্দিষ্ট কমান্ড লিখে তথ্য জানুন:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🚨 জরুরি হটলাইন ও সেবা", callback_data='emergency')],
        [InlineKeyboardButton("🚒 ফায়ার সার্ভিস স্টেশনসমূহ", callback_data='fire_service')],
        [InlineKeyboardButton("🏥 হাসপাতাল ও অ্যাম্বুলেন্স", callback_data='hospital')],
        [InlineKeyboardButton("⚡ পল্লী বিদ্যুৎ অভিযোগ কেন্দ্র", callback_data='pally_biddyut')],
        [InlineKeyboardButton("👮 পুলিশ প্রশাসন ও ওিসি নম্বর", callback_data='police_info')],
        [InlineKeyboardButton("🤖 এআই অ্যাসিস্ট্যান্ট (Gemini AI)", callback_data='ai_help')]
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
            "🚨 **সুনামগঞ্জ জেলা - জরুরি হেল্পলাইন নম্বরসমূহ** 🚨\n\n"
            "📞 জাতীয় জরুরি সেবা (পুলিশ/ফায়ার সার্ভিস/অ্যাম্বুলেন্স): `999`\n"
            "📞 সরকারি তথ্য ও সেবা: `333`\n"
            "📞 স্বাস্থ্য বাতায়ন (চিকিৎসা পরামর্শ): `16263`"
        )
    elif query.data == 'fire_service':
        text = (
            "🚒 **ফায়ার সার্ভিস ও সিভিল ডিফেন্স স্টেশনসমূহ** 🚒\n\n"
            "• সুনামগঞ্জ সদর ফায়ার স্টেশন: `01901-023698`\n"
            "• ছাতক ফায়ার স্টেশন: `01901-023700`\n"
            "• জগন্নাথপুর ফায়ার স্টেশন: `01901-023704`\n"
            "• শান্তিগঞ্জ ফায়ার স্টেশন: `01901-023706`\n"
            "• দিরাই ফায়ার স্টেশন: `01901-023708`\n"
            "• বিশ্বম্ভরপুর ফায়ার স্টেশন: `01901-023710`"
        )
    elif query.data == 'hospital':
        text = (
            "🏥 **সরকারি হাসপাতাল ও অ্যাম্বুলেন্স সেবা** 🏥\n\n"
            "• জেলা সদর হাসপাতাল (জরুরি): `01718-630887`, `02996600225`\n"
            "• ছাতক উপজেলা স্বাস্থ্য কমপ্লেক্স: `01730-324773`\n"
            "• দোয়ারাবাজার উপজেলা স্বাস্থ্য কমপ্লেক্স: `01730-324774`\n"
            "• তাহিরপুর উপজেলা স্বাস্থ্য কমপ্লেক্স: `01730-324779`\n"
            "• জগন্নাথপুর উপজেলা স্বাস্থ্য কমপ্লেক্স: `01730-324775`\n"
            "• দিরাই উপজেলা স্বাস্থ্য কমপ্লেক্স: `01730-324776`\n"
            "• জামালগঞ্জ উপজেলা স্বাস্থ্য কমপ্লেক্স: `01730-324778`"
        )
    elif query.data == 'pally_biddyut':
        text = (
            "⚡ **পল্লী বিদ্যুৎ সমিতি (অভিযোগ ও হটলাইন)** ⚡\n\n"
            "• জেলা সদর দপ্তর অভিযোগ কেন্দ্র: `01769-401854`\n"
            "• দোয়ারাবাজার সাব-জোনাল অফিস: `01769-407809`\n"
            "• ছাতক জোনাল অফিস: `01769-401865`\n"
            "• বিশ্বম্ভরপুর অভিযোগ কেন্দ্র: `01769-401856`\n"
            "• দিরাই অভিযোগ কেন্দ্র: `01769-401860`\n"
            "• জগন্নাথপুর অভিযোগ কেন্দ্র: `01769-401862`\n"
            "• শান্তিগঞ্জ অভিযোগ কেন্দ্র: `01769-401864`\n"
            "• তাহিরপুর অভিযোগ কেন্দ্র: `01769-401858`\n"
            "• জামালগঞ্জ সাব-জোনাল অফিস: `01704-109080`"
        )
    elif query.data == 'police_info':
        text = (
            "👮 **সুনামগঞ্জ জেলা পুলিশ প্রশাসন ও থানা সমূহের তালিকা** 👮\n\n"
            "• পুলিশ সুপার (SP): `01320-120700`\n"
            "• জেলা পুলিশ কন্ট্রোল রুম: `01320-121699`\n"
            "• জেলা ডিবি পুলিশ (ওসি-১): `01320-121102`\n\n"
            "📌 **নির্দিষ্ট থানার তথ্য দেখতে কমান্ড ব্যবহার করুন:**\n"
            "👉 `/sadar` (সদর থানা ও ওসি/ডিউটি অফিসার)\n"
            "👉 `/dowarabাজার` বা `/dowara` (দোয়ারাবাজার থানা)\n"
            "👉 `/chhatak` (ছাতক থানা)\n"
            "👉 `/jagannathpur` (জগন্নাথপুর থানা)\n"
            "👉 `/bishwambharpur` (বিশ্বম্ভরপুর থানা)\n"
            "👉 `/dirai` (দিরাই থানা)\n"
            "👉 `/shalla` (শাল্লা থানা)\n"
            "👉 `/shanthiganj` (শান্তিগঞ্জ থানা)\n"
            "👉 `/tahirpur` (তাহিরপুর থানা)\n"
            "👉 `/jamalganj` (জামালগঞ্জ থানা)\n"
            "👉 `/dharmapasha` (ধর্মপাশা থানা)\n"
            "👉 `/madhyanagar` (মধ্যনগর থানা)"
        )
    elif query.data == 'ai_help':
        text = (
            "🤖 **Gemini এআই সহকারী:**\n\n"
            "আপনার যেকোনো প্রশ্ন (পড়াশোনা, প্রযুক্তি, সাধারণ জ্ঞান ইত্যাদি) মেসেজ বক্সে লিখে পাঠান। এআই তাৎক্ষণিক উত্তর দেবে।"
        )
    
    keyboard = [[InlineKeyboardButton("⬅️ মূল মেনু (Main Menu)", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query.data == 'main_menu':
        await start(update, context)
    else:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# --- SPECIFIC POLICE STATION COMMANDS ---
async def sadar_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **সুনামগঞ্জ সদর থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-120790`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-120795`", parse_mode='Markdown'
    )

async def dowara_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **দোয়ারাবাজার থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-120920`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-120925`", parse_mode='Markdown'
    )

async def chhatak_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **ছাতক থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-120816`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-120821`", parse_mode='Markdown'
    )

async def jagannathpur_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **জগন্নাথপুর থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-120842`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-120847`", parse_mode='Markdown'
    )

async def bishwambharpur_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **বিশ্বম্ভরপুর থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-120894`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-120899`", parse_mode='Markdown'
    )

async def dirai_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **দিরাই থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-120946`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-120951`", parse_mode='Markdown'
    )

async def shalla_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **শাল্লা থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-120972`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-120977`", parse_mode='Markdown'
    )

async def shanthiganj_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **শান্তিগঞ্জ থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-121076`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-121081`", parse_mode='Markdown'
    )

async def tahirpur_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **তাহিরপুর থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-120868`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-120873`", parse_mode='Markdown'
    )

async def jamalganj_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **জামালগঞ্জ থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-120998`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-121003`", parse_mode='Markdown'
    )

async def dharmapasha_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **ধর্মপাশা থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-121024`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-121029`", parse_mode='Markdown'
    )

async def madhyanagar_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏛️ **মধ্যনগর থানা তথ্য:**\n\n"
        "• ওসি (Officer in Charge): `01320-121050`\n"
        "• ডিউটি অফিসার (জরুরি): `01320-121055`", parse_mode='Markdown'
    )

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
    
    # General Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    # Specific Police Station Commands
    app.add_handler(CommandHandler("sadar", sadar_station))
    app.add_handler(CommandHandler("dowara", dowara_station))
    app.add_handler(CommandHandler("chhatak", chhatak_station))
    app.add_handler(CommandHandler("jagannathpur", jagannathpur_station))
    app.add_handler(CommandHandler("bishwambharpur", bishwambharpur_station))
    app.add_handler(CommandHandler("dirai", dirai_station))
    app.add_handler(CommandHandler("shalla", shalla_station))
    app.add_handler(CommandHandler("shanthiganj", shanthiganj_station))
    app.add_handler(CommandHandler("tahirpur", tahirpur_station))
    app.add_handler(CommandHandler("jamalganj", jamalganj_station))
    app.add_handler(CommandHandler("dharmapasha", dharmapasha_station))
    app.add_handler(CommandHandler("madhyanagar", madhyanagar_station))
    
    # AI Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
