from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8827706497:AAGSvKalbSw5-udm5X7-K8vp-kEGJrZ_oXs"

PIX = "86244512-5d01-47d9-a417-e5197252fab3"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
🔥 BEM-VINDO AO CLUBE PREMIUM 🔥

✨ Um espaço exclusivo para membros.

Tenha acesso a conteúdos especiais e uma área reservada para assinantes.

🔒 Área privada
⭐ Conteúdo exclusivo
💎 Acesso premium

Escolha seu plano abaixo:
"""

    botoes = [
        [InlineKeyboardButton("💎 Ver planos disponíveis", callback_data="planos")]
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
💎 PLANOS DE ACESSO PREMIUM

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


    elif query.data in ["mensal", "trimestral", "anual"]:

        planos = {
            "mensal": "🥉 ACESSO MENSAL PREMIUM\n\n📅 30 dias\n💰 R$ 12,99",
            "trimestral": "🥈 ACESSO TRIMESTRAL PREMIUM\n\n📅 90 dias\n💰 R$ 15,99",
            "anual": "🥇 ACESSO ANUAL PREMIUM\n\n📅 365 dias\n💰 R$ 29,90"
        }

        texto = f"""
{planos[query.data]}


💳 COMO REALIZAR O PAGAMENTO

1️⃣ Clique em "Copiar código PIX".

2️⃣ Abra o aplicativo do seu banco.

3️⃣ Entre na opção PIX.

4️⃣ Escolha "PIX Copia e Cola".

5️⃣ Cole o código copiado.

6️⃣ Confira o valor e confirme o pagamento.


✅ Depois do pagamento, clique em:

🔎 Verificar status


Escolha uma opção:
"""

        botoes = [
            [InlineKeyboardButton("📋 Copiar código PIX", callback_data="pix")],
            [InlineKeyboardButton("🔎 Verificar status", callback_data="status")]
        ]

        await query.edit_message_text(
            texto,
            reply_markup=InlineKeyboardMarkup(botoes)
        )


    elif query.data == "pix":

        await query.edit_message_text(
            f"""
📋 CÓDIGO PIX

{PIX}


Após realizar o pagamento, volte ao bot e clique em:

🔎 Verificar status


Obrigado por escolher o Clube Premium.
"""
        )


    elif query.data == "status":

        await query.edit_message_text(
            """
⏳ STATUS DO PAGAMENTO

Seu pagamento ainda está aguardando confirmação.

Assim que for confirmado, seu acesso será liberado.

Obrigado pela paciência.
"""
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(clique))

print("Bot iniciado!")

app.run_polling()
