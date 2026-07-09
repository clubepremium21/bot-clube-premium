from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import ADMIN_ID

from database import (
    buscar_cliente,
    alterar_status,
    listar_clientes,
    buscar_comprovantes_pendentes,
    alterar_status_comprovante
)


LINK_GRUPO = "COLOQUE_AQUI_O_LINK_DO_GRUPO"


async def enviar_painel_admin(update, context):

    if update.effective_user.id != ADMIN_ID:
        return

    texto = """
👤 PAINEL ADMINISTRATIVO

Escolha uma opção:
"""

    botoes = [
        [
            InlineKeyboardButton(
                "📊 Ver membros",
                callback_data="listar_clientes"
            )
        ],
        [
            InlineKeyboardButton(
                "📸 Ver comprovantes",
                callback_data="ver_comprovantes"
            )
        ]
    ]

    await update.message.reply_text(
        texto,
        reply_markup=InlineKeyboardMarkup(botoes)
    )


async def enviar_comprovante_admin(context, telegram_id, file_id, id_comprovante):

    botoes = [
        [
            InlineKeyboardButton(
                "✅ Aprovar",
                callback_data=f"aprovar_{telegram_id}_{id_comprovante}"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Recusar",
                callback_data=f"recusar_{telegram_id}_{id_comprovante}"
            )
        ]
    ]

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=file_id,
        caption=f"""
📸 NOVO COMPROVANTE

Usuário:
{telegram_id}

Aguardando análise.
""",
        reply_markup=InlineKeyboardMarkup(botoes)
    )


async def aprovar_pagamento(update, context):

    query = update.callback_query
    await query.answer()

    dados = query.data.split("_")

    telegram_id = int(dados[1])
    id_comprovante = int(dados[2])

    alterar_status(
        telegram_id,
        "ATIVO"
    )

    alterar_status_comprovante(
        id_comprovante,
        "APROVADO"
    )

    await context.bot.send_message(
        chat_id=telegram_id,
        text=f"""
🎉 Pagamento aprovado!

✅ Sua assinatura está ativa.

Acesse o grupo pelo link:

{LINK_GRUPO}
"""
    )

    await query.edit_message_caption(
        caption="✅ Pagamento aprovado e acesso enviado."
    )


async def recusar_pagamento(update, context):

    query = update.callback_query
    await query.answer()

    dados = query.data.split("_")

    telegram_id = int(dados[1])
    id_comprovante = int(dados[2])

    alterar_status_comprovante(
        id_comprovante,
        "RECUSADO"
    )

    await context.bot.send_message(
        chat_id=telegram_id,
        text="""
❌ Comprovante recusado.

Entre em contato caso tenha ocorrido algum problema.
"""
    )

    await query.edit_message_caption(
        caption="❌ Comprovante recusado."
    )


async def listar_comprovantes(update, context):

    comprovantes = buscar_comprovantes_pendentes()

    for comprovante in comprovantes:

        await enviar_comprovante_admin(
            context,
            comprovante[1],
            comprovante[2],
            comprovante[0]
        )


async def aprovar_usuario(telegram_id):

    alterar_status(
        telegram_id,
        "ATIVO"
    )


async def bloquear_usuario(telegram_id):

    alterar_status(
        telegram_id,
        "BLOQUEADO"
    )


async def consultar_usuario(telegram_id):

    return buscar_cliente(
        telegram_id
    )
