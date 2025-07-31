from flask import Flask, request, render_template
from playwright.sync_api import sync_playwright
import re

app = Flask(__name__)

def extract_tiktok_info(product_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(product_url, timeout=60000)
            page.wait_for_timeout(5000)
            html = page.content()

            product_id = re.search(r'"product_id":"?(\d+)"?', html)
            sku_id = re.search(r'"sku_id":"?(\d+)"?', html)
            seller_id = re.search(r'"seller_id":"?(\d+)"?', html)

            if product_id and sku_id and seller_id:
                return {
                    "product_id": product_id.group(1),
                    "sku_id": sku_id.group(1),
                    "seller_id": seller_id.group(1)
                }
            else:
                return None
        finally:
            browser.close()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form.get("url")
        info = extract_tiktok_info(url)
        if info:
            checkout_url = f"https://www.tiktok.com/view/fe_tiktok_ecommerce_in_web/order_submit/index.html?sku_id={info['sku_id']}&product_id={info['product_id']}&quantity=1&seller_id={info['seller_id']}"
            result = {
                "checkout_url": checkout_url,
                "product_id": info["product_id"],
                "sku_id": info["sku_id"],
                "seller_id": info["seller_id"]
            }
        else:
            result = {"error": "Failed to extract the product info. Make sure the link is a full product page."}
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)