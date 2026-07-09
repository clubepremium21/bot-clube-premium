from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import (
    MENSAGEM_BEM_VINDO,
    PLANOS,
    PIX,
    INSTRUCOES_PIX
)

from database import (
    cadastrar_cliente,
    atualizar_plano,
    salvar_comprovante,
    buscar_cliente
)


async def receber_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE):

    foto = update.message.photo[-1]

    salvar_comprovante(
        update.effective_user.id,
        foto.file_id,
        str(update.message.date)
    )

    botoes = [
        [
            InlineKeyboardButton(
                "🔎 Verificar status",
                callback_data="status"
            )
        ]
    ]

    await update.message.reply_text(
        """
✅ Comprovante enviado!

⏳ Seu pagamento está aguardando confirmação.

Você pode acompanhar o status abaixo:
""",
        reply_markup=InlineKeyboardMarkup(botoes)
    )

    usuario = update.effective_user

    cadastrar_cliente(
        usuario.id,
        usuario.first_name,
        usuario.username
    )

    botoes = [
        [
            InlineKeyboardButton(
                "💎 Ver planos",
                callback_data="planos"
            )
        ],
        [
            InlineKeyboardButton(
                "👤 Minha assinatura",
                callback_data="minha_assinatura"
            )
        ]
    ]

    await update.message.reply_text(
        MENSAGEM_BEM_VINDO,
        reply_markup=InlineKeyboardMarkup(botoes)
    )


async def menu_planos(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    texto = "💎 PLANOS DISPONÍVEIS\n\n"

    botoes = []

    for chave, plano in PLANOS.items():

        texto += (
            f"{plano['nome']}\n"
            f"📅 {plano['dias']} dias\n"
            f"💰 R$ {plano['valor']}\n\n"
        )

        botoes.append(
            [
                InlineKeyboardButton(
                    plano["nome"],
                    callback_data=f"plano_{chave}"
                )
            ]
        )

    await query.edit_message_text(
        texto,
        reply_markup=InlineKeyboardMarkup(botoes)
    )


async def escolher_plano(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    plano = query.data.replace(
        "plano_",
        ""
    )

    atualizar_plano(
        query.from_user.id,
        plano
    )


    texto = f"""
{PLANOS[plano]['nome']}

💰 Valor:
R$ {PLANOS[plano]['valor']}

{INSTRUCOES_PIX}
"""


    await query.edit_message_text(
        texto
    )


    await query.message.reply_text(
        f"""
💳 CÓDIGO PIX

Copie o código abaixo:

{PIX}
"""
    )


    botoes = [
        [
            InlineKeyboardButton(
                "📸 Enviar comprovante",
                callback_data="comprovante"
            )
        ],
        [
            InlineKeyboardButton(
                "🔎 Ver status",
                callback_data="status"
            )
        ]
    ]


    await query.message.reply_text(
        "Após realizar o pagamento, envie o comprovante.",
        reply_markup=InlineKeyboardMarkup(botoes)
    )



async def minha_assinatura(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    cliente = buscar_cliente(
        query.from_user.id
    )


    if cliente:

        texto = f"""
👤 Minha assinatura

Plano:
{cliente[5]}

Status:
{cliente[6]}
"""

    else:

        texto = """
Você ainda não possui cadastro.
"""


    await query.edit_message_text(
        texto
    )



async def receber_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE):

    foto = update.message.photo[-1]


    salvar_comprovante(
        update.effective_user.id,
        foto.file_id,
        str(update.message.date)
    )


    await update.message.reply_text(
        """
✅ Comprovante recebido.

Aguarde a confirmação.
"""
    )



async def verificar_status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    cliente = buscar_cliente(
        query.from_user.id
    )


    if cliente and cliente[6] == "ATIVO":

        texto = """
✅ Sua assinatura está ativa.
"""

    else:

        texto = """
⏳ Pagamento aguardando confirmação.
"""


    await query.edit_message_text(
        texto
    )
