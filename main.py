from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "HEAD"])
def index():
    result = {}
    if request.method == "POST":
        try:
            url = request.form["url"]
            # Dummy placeholder logic – update later to scrape TikTok
            result["checkout_url"] = url
            result["product_id"] = "123456"
            result["sku_id"] = "654321"
            result["seller_id"] = "999999"
        except Exception as e:
            result["error"] = str(e)
    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
