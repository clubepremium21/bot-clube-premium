from datetime import datetime, timedelta

from database import (
    atualizar_plano,
    alterar_status,
)


def registrar_plano(telegram_id, plano):
    """
    Salva o plano escolhido pelo usuário.
    """
    atualizar_plano(telegram_id, plano)


def aprovar_pagamento(telegram_id, plano):

    dias = {
        "mensal": 30,
        "trimestral": 90,
        "anual": 365
    }

    hoje = datetime.now()

    vencimento = hoje + timedelta(days=dias.get(plano, 30))

    alterar_status(telegram_id, "ATIVO")

    return {
        "status": "ATIVO",
        "inicio": hoje.strftime("%d/%m/%Y"),
        "vencimento": vencimento.strftime("%d/%m/%Y")
    }


def rejeitar_pagamento(telegram_id):

    alterar_status(telegram_id, "RECUSADO")


def assinatura_ativa(cliente):

    if cliente is None:
        return False

    if len(cliente) < 8:
        return False

    if cliente[5] != "ATIVO":
        return False

    try:
        vencimento = datetime.strptime(cliente[7], "%d/%m/%Y")
    except Exception:
        return False

    return vencimento >= datetime.now()


def dias_restantes(cliente):

    if cliente is None:
        return 0

    try:
        vencimento = datetime.strptime(cliente[7], "%d/%m/%Y")
    except Exception:
        return 0

    dias = (vencimento - datetime.now()).days

    if dias < 0:
        return 0

    return dias
