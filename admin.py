from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import ADMIN_ID

from database import (
    buscar_cliente,
    alterar_status,
    buscar_comprovantes_pendentes,
    alterar_status_comprovante
)


LINK_GRUPO = "https://t.me/+gjl7eVe68e9jYzgx"


async def enviar_painel_admin(update, context):

    if update.effective_user.id != ADMIN_ID:
        return


    botoes = [
        [
            InlineKeyboardButton(
                "📸 Ver comprovantes",
                callback_data="ver_comprovantes"
            )
        ]
    ]


    await update.message.reply_text(
        """
👤 PAINEL ADMINISTRATIVO

Escolha uma opção:
""",
        reply_markup=InlineKeyboardMarkup(botoes)
    )



async def enviar_comprovante_admin(context, telegram_id, file_id):

    botoes = [
        [
            InlineKeyboardButton(
                "✅ Aprovar",
                callback_data=f"aprovar_{telegram_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Recusar",
                callback_data=f"recusar_{telegram_id}"
            )
        ]
    ]


    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=file_id,
        caption=f"""
📸 NOVO COMPROVANTE

🆔 ID:
{telegram_id}

Aguardando confirmação.
""",
        reply_markup=InlineKeyboardMarkup(botoes)
    )



async def aprovar_pagamento(update, context):

    query = update.callback_query

    await query.answer()


    dados = query.data.split("_")

    telegram_id = int(dados[1])


    alterar_status(
        telegram_id,
        "ATIVO"
    )


    await context.bot.send_message(
        chat_id=telegram_id,
        text=f"""
🎉 Pagamento aprovado!

✅ Sua assinatura está ativa.

🔗 Acesse o grupo:

{LINK_GRUPO}
"""
    )


    await query.edit_message_caption(
        caption="✅ Pagamento aprovado. Link enviado ao cliente."
    )



async def recusar_pagamento(update, context):

    query = update.callback_query

    await query.answer()


    dados = query.data.split("_")

    telegram_id = int(dados[1])


    alterar_status(
        telegram_id,
        "BLOQUEADO"
    )


    await context.bot.send_message(
        chat_id=telegram_id,
        text="""
❌ Pagamento recusado.

Entre em contato para verificar.
"""
    )


    await query.edit_message_caption(
        caption="❌ Pagamento recusado."
    )



async def listar_comprovantes(update, context):

    comprovantes = buscar_comprovantes_pendentes()


    for comprovante in comprovantes:

        await enviar_comprovante_admin(
            context,
            comprovante[1],
            comprovante[2]
        )



async def consultar_usuario(telegram_id):

    return buscar_cliente(
        telegram_id
    )
