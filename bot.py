from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8827706497:AAGSvKalbSw5-udm5X7-K8vp-kEGJrZ_oXs"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
🔥 Bem-vindo ao Clube Premium!

Tenha acesso a conteúdos exclusivos para membros.

Escolha uma opção:
"""

    botoes = [
        [InlineKeyboardButton("📚 Ver planos", callback_data="planos")]
    ]

    await update.message.reply_text(
        texto,
        reply_markup=InlineKeyboardMarkup(botoes)
    )


async def clique(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "planos":

        texto = """
⭐ Planos do Clube Premium

🥉 Mensal
📅 30 dias
💰 R$ 12,99

🥈 Trimestral
📅 90 dias
💰 R$ 15,99

🥇 Anual
📅 365 dias
💰 R$ 29,90

Escolha seu plano:
"""

        botoes = [
            [InlineKeyboardButton("🥉 Mensal", callback_data="mensal")],
            [InlineKeyboardButton("🥈 Trimestral", callback_data="trimestral")],
            [InlineKeyboardButton("🥇 Anual", callback_data="anual")]
        ]

        await query.edit_message_text(
            texto,
            reply_markup=InlineKeyboardMarkup(botoes)
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(clique))

print("Bot iniciado!")

app.run_polling()