from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from config import TOKEN

from database import criar_banco

from handlers import (
    inicio,
    menu_planos,
    escolher_plano,
    minha_assinatura,
    pedir_comprovante,
    receber_comprovante,
    verificar_status
)

from admin import enviar_painel_admin


def main():

    criar_banco()

    app = Application.builder().token(TOKEN).build()

    # Comandos
    app.add_handler(
        CommandHandler(
            "start",
            inicio
        )
    )

    app.add_handler(
        CommandHandler(
            "admin",
            enviar_painel_admin
        )
    )

    # Botões
    app.add_handler(
        CallbackQueryHandler(
            menu_planos,
            pattern="^planos$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            escolher_plano,
            pattern="^plano_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            minha_assinatura,
            pattern="^minha_assinatura$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            pedir_comprovante,
            pattern="^comprovante$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            verificar_status,
            pattern="^status$"
        )
    )

    # Recebe fotos (comprovantes)
    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            receber_comprovante
        )
    )

    print("✅ Bot iniciado!")

    app.run_polling()


if __name__ == "__main__":
    main()
