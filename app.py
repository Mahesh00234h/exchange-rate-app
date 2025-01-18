from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Your API key for the ExchangeRate API
API_KEY = "api key"
BASE_URL = "https://v6.exchangerate-api.com/v6"

@app.route("/")
def index():
    # Fetch available currencies
    response = requests.get(f"{BASE_URL}/{API_KEY}/latest/USD")
    data = response.json()
    if data["result"] == "success":
        currencies = data["conversion_rates"]
        currency_list = list(currencies.keys())  # List of currency codes
    else:
        currency_list = []

    # Pass currency_list to the HTML template
    return render_template("index.html", currencies=currency_list)

@app.route("/convert", methods=["POST"])
def convert():
    try:
        from_currency = request.form.get("from_currency").upper()
        to_currency = request.form.get("to_currency").upper()
        amount = float(request.form.get("amount"))

        # Fetch exchange rates
        response = requests.get(f"{BASE_URL}/{API_KEY}/latest/{from_currency}")
        data = response.json()

        if data["result"] == "success":
            rate = data["conversion_rates"].get(to_currency)
            if not rate:
                return jsonify({"error": f"Currency {to_currency} not found!"}), 400

            converted_amount = rate * amount
            return jsonify({
                "from_currency": from_currency,
                "to_currency": to_currency,
                "amount": amount,
                "converted_amount": round(converted_amount, 2),
                "rate": rate
            })
        else:
            return jsonify({"error": "Failed to fetch exchange rates."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
