# ==========================
# CONFIGURAÇÕES DO BOT
# ==========================

TOKEN = "COLE_SEU_NOVO_TOKEN_AQUI"

ADMIN_ID = 8129683840

# ==========================
# PIX
# ==========================

PIX = "86244512-5d01-47d9-a417-e5197252fab3"

# ==========================
# GRUPO VIP
# ==========================

LINK_GRUPO = "https://t.me/+gjl7eVe68e9jYzgx"

# ==========================
# PLANOS
# ==========================

PLANOS = {
    "mensal": {
        "nome": "🥉 Mensal",
        "dias": 30,
        "valor": "12,99"
    },

    "trimestral": {
        "nome": "🥈 Trimestral",
        "dias": 90,
        "valor": "15,99"
    },

    "anual": {
        "nome": "🥇 Anual",
        "dias": 365,
        "valor": "29,90"
    }
}

# ==========================
# MENSAGENS
# ==========================

MENSAGEM_BEM_VINDO = """
🔥 Bem-vindo ao Clube Premium!

Aqui você encontra conteúdos exclusivos para membros.

Escolha uma opção abaixo para continuar.
"""

INSTRUCOES_PIX = """
💳 COMO PAGAR

1️⃣ Clique em "Copiar PIX"

2️⃣ Abra o aplicativo do seu banco.

3️⃣ Entre em PIX.

4️⃣ Escolha "PIX Copia e Cola".

5️⃣ Cole o código.

6️⃣ Confirme o pagamento.

Depois clique em:

📸 Enviar comprovante
"""

STATUS_AGUARDANDO = """
⏳ Seu comprovante foi recebido.

Nossa equipe irá verificar o pagamento.

Assim que aprovado, seu acesso será liberado automaticamente.
"""

ACESSO_LIBERADO = f"""
🎉 Pagamento aprovado!

Seu acesso foi liberado.

👇 Entre agora:

{LINK_GRUPO}

Bom proveito!
"""
