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


async def inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

    await query.edit_message_text(texto)

    await query.message.reply_text(
        f"""
💳 CÓDIGO PIX

Copie a chave abaixo:

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
                "🔎 Verificar status",
                callback_data="status"
            )
        ]
    ]

    await query.message.reply_text(
        "Após realizar o pagamento, clique em **📸 Enviar comprovante**.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(botoes)
    )


async def pedir_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        """
📸 Envie agora uma FOTO do comprovante do PIX.

⚠️ Envie a imagem completa.

Assim que recebermos, ela ficará aguardando confirmação.
"""
    )async def minha_assinatura(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    cliente = buscar_cliente(
        query.from_user.id
    )

    if cliente:

        plano = cliente[5] if cliente[5] else "Nenhum"

        status = cliente[6] if cliente[6] else "INATIVO"

        texto = f"""
👤 Minha assinatura

📦 Plano: {plano}

📋 Status: {status}
"""

    else:

        texto = """
❌ Você ainda não possui assinatura.
"""

    await query.edit_message_text(texto)


async def receber_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.photo:

        await update.message.reply_text(
            "❌ Envie uma FOTO do comprovante."
        )
        return

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
✅ Comprovante recebido com sucesso!

⏳ Seu pagamento foi enviado para análise.

Normalmente a confirmação acontece em poucos minutos.

Você pode acompanhar o andamento clicando no botão abaixo.
""",
        reply_markup=InlineKeyboardMarkup(botoes)
    )


async def verificar_status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    cliente = buscar_cliente(
        query.from_user.id
    )

    if cliente and cliente[6] == "ATIVO":

        texto = f"""
🎉 Pagamento aprovado!

✅ Sua assinatura está ativa.

Aproveite todo o conteúdo exclusivo.
"""

    else:

        texto = """
⏳ Ainda não identificamos a aprovação do pagamento.

Caso você já tenha enviado o comprovante, aguarde alguns minutos enquanto realizamos a conferência.

Assim que aprovado, seu acesso será liberado automaticamente.
"""

    await query.edit_message_text(texto)
