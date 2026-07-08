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


    elif query.data == "mensal":

        await query.edit_message_text(
            """
🥉 Plano Mensal

💰 Valor: R$ 12,99

PIX:
86244512-5d01-47d9-a417-e5197252fab3

Após o pagamento, aguarde a confirmação da liberação do acesso.
"""
        )


    elif query.data == "trimestral":

        await query.edit_message_text(
            """
🥈 Plano Trimestral

💰 Valor: R$ 15,99

PIX:
86244512-5d01-47d9-a417-e5197252fab3

Após o pagamento, aguarde a confirmação da liberação do acesso.
"""
        )


    elif query.data == "anual":

        await query.edit_message_text(
            """
🥇 Plano Anual

💰 Valor: R$ 29,90

PIX:
86244512-5d01-47d9-a417-e5197252fab3

Após o pagamento, aguarde a confirmação da liberação do acesso.
"""
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(clique))

print("Bot iniciado!")

app.run_polling()
