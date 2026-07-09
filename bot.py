from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)


TOKEN = "8827706497:AAFWnSccUhwyVCnNuRoMLQIn1htLzFhKU2Y"

SEU_ID = 8129683840

PIX = "86244512-5d01-47d9-a417-e5197252fab3"

LINK_GRUPO = "https://t.me/+gjl7eVe68e9jYzgx"


# Guarda quem enviou comprovante
usuarios_comprovante = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
🔥 BEM-VINDO AO CLUBE PREMIUM 🔥

✨ Acesso exclusivo para membros.

Tenha acesso ao conteúdo premium reservado para assinantes.

💎 Escolha seu plano:
"""

    botoes = [
        [InlineKeyboardButton("💎 Ver planos", callback_data="planos")]
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
💎 PLANOS PREMIUM

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
            "mensal": "🥉 Plano Mensal\n💰 R$ 12,99",
            "trimestral": "🥈 Plano Trimestral\n💰 R$ 15,99",
            "anual": "🥇 Plano Anual\n💰 R$ 29,90"
        }


        context.user_data["plano"] = query.data


        texto = f"""
{planos[query.data]}


💳 COMO PAGAR:

1️⃣ Clique em copiar código PIX.

2️⃣ Abra o aplicativo do seu banco.

3️⃣ Escolha PIX Copia e Cola.

4️⃣ Cole o código.

5️⃣ Confirme o pagamento.


Após pagar envie o comprovante.
"""


        botoes = [
            [InlineKeyboardButton("📋 Código PIX", callback_data="pix")],
            [InlineKeyboardButton("📸 Enviar comprovante", callback_data="comprovante")],
            [InlineKeyboardButton("🔎 Verificar status", callback_data="status")]
        ]


        await query.edit_message_text(
            texto,
            reply_markup=InlineKeyboardMarkup(botoes)
        )



    elif query.data == "pix":

        await query.edit_message_text(
            f"""
📋 CÓDIGO PIX:

{PIX}

Copie e cole no aplicativo do seu banco.
"""
        )



    elif query.data == "comprovante":

        await query.edit_message_text(
            """
📸 Envie agora o comprovante de pagamento.

Após recebermos, iremos verificar e liberar seu acesso.
"""
        )

        context.user_data["aguardando_comprovante"] = True



    elif query.data == "status":

        await query.edit_message_text(
            """
⏳ STATUS:

Seu pagamento está aguardando confirmação.

Assim que for confirmado seu acesso será liberado.
"""
        )




async def receber_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("aguardando_comprovante"):

        usuario = update.message.from_user

        usuarios_comprovante[usuario.id] = usuario


        await update.message.forward(SEU_ID)


        botoes = [
            [
                InlineKeyboardButton(
                    "✅ Liberar acesso",
                    callback_data=f"liberar_{usuario.id}"
                )
            ]
        ]


        await context.bot.send_message(
            chat_id=SEU_ID,
            text=f"""
📸 NOVO COMPROVANTE

Nome:
{usuario.first_name}

ID:
{usuario.id}

Clique para liberar:
""",
            reply_markup=InlineKeyboardMarkup(botoes)
        )


        await update.message.reply_text(
            """
✅ Comprovante enviado!

Aguarde a confirmação do pagamento.
"""
        )

        context.user_data["aguardando_comprovante"] = False




async def liberar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    if query.from_user.id != SEU_ID:
        return


    usuario_id = int(query.data.replace("liberar_", ""))


    await context.bot.send_message(
        chat_id=usuario_id,
        text=f"""
🎉 PAGAMENTO CONFIRMADO!

Seu acesso foi liberado.

Clique no link abaixo:

🔓 {LINK_GRUPO}
"""
    )


    await query.edit_message_text(
        "✅ Acesso liberado com sucesso!"
    )




app = Application.builder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(
        clique,
        pattern="^(planos|mensal|trimestral|anual|pix|comprovante|status)$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        liberar,
        pattern="^liberar_"
    )
)


app.add_handler(
    MessageHandler(
        filters.PHOTO,
        receber_comprovante
    )
)


print("Bot iniciado!")

app.run_polling()
