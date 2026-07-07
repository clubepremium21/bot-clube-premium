from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook-infinitepay", methods=["POST"])
def infinitepay_webhook():
    dados = request.json

    print("Pagamento recebido:")
    print(dados)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(port=5000)