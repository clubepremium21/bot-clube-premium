from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import ADMIN_ID
from database import (
    buscar_cliente,
    alterar_status
)


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
                "🔎 Consultar usuário",
                callback_data="consultar"
            )
        ]
    ]

    await update.message.reply_text(
        texto,
        reply_markup=InlineKeyboardMarkup(botoes)
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

    cliente = buscar_cliente(
        telegram_id
    )

    return cliente
