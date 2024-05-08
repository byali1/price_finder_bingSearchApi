from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# User Agents
user_agents = {
    "vatanbilgisayar.com": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "trendyol.com": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "amazon.com.tr": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "incehesap.com": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "akakce.com": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "apple.com": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "teknosa.com": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "hepsiburada.com": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "n11.com": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "mediamarkt.com.tr": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",

}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    api_key = "API_KEY"
    results = search_product(query, api_key)
    products = scrape_product_info(results)
    return jsonify(products)

@app.route('/get_price', methods=['POST'])
def get_price():
    url = request.form['url']
    price = scrape_price(url)
    return jsonify({'price': price})

def search_product(query, api_key):
    url = f"https://api.bing.microsoft.com/v7.0/search?q={query}&responseFilter=Webpages&count=10"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def scrape_product_info(search_results):
    products = []
    if 'webPages' in search_results:
        web_pages = search_results['webPages']['value']
        for page in web_pages:
            name = page['name']
            url = page['url']
            products.append({'name': name, 'url': url})
    return products

def scrape_price(url):
    user_agent = user_agents.get(url, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0")
    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')


    if "vatanbilgisayar.com" in url:
        return scrape_price_from_vatan(soup)
    elif "trendyol.com" in url:
        return scrape_price_from_trendyol(soup)
    elif "amazon.com.tr" in url:
        return scrape_price_from_amazon(soup)
    elif "incehesap.com" in url:
        return scrape_price_from_incehesap(soup)
    elif "akakce.com" in url:
        return scrape_price_from_akakce(soup)
    elif "teknosa.com" in url:
        return scrape_price_from_teknosa(soup)
    elif "hepsiburada.com" in url:
        return scrape_price_from_hepsiburada(soup)
    elif "n11.com" in url:
        return scrape_price_from_n(soup)
    else:
        pass


# Özel site fiyat çekme fonksiyonları
def scrape_price_from_vatan(soup):
    price_tag = soup.find('span', class_='product-list__price')
    if price_tag:
        price_text = price_tag.text.strip()
        price_text = price_text.replace('TL', '').replace('.', '').replace(',', '.')
        try:
            price = float(price_text)
            return price
        except ValueError:
            return None
    return None


def scrape_price_from_trendyol(soup):
    price_tag = soup.find('div', class_='prc-box-dscntd')
    if price_tag:
        price_text = price_tag.text.strip()
        price_text = price_text.replace('TL', '').replace('.', '').replace(',', '.')
        try:
            price = float(price_text)
            return price
        except ValueError:
            return None

    alternative_price_tag = soup.find('span', class_='prc-dsc')
    if alternative_price_tag:
        alternative_price_text = alternative_price_tag.text.strip()
        # Fiyatı uygun formatta düzenleyin
        alternative_price_text = alternative_price_text.replace('TL', '').replace('.', '').replace(',', '.')
        try:
            alternative_price = float(alternative_price_text)
            return alternative_price
        except ValueError:
            pass

    return None


def scrape_price_from_teknosa(soup):
    price_tag = soup.find('div', class_='pdp-prices')
    if price_tag:
        price_text = price_tag.text.strip()
        price_text = price_text.replace('TL', '').replace('.', '').replace(',', '.')
        try:
            price = float(price_text)
            return price
        except ValueError:
            return None

    alternative_price_tag = soup.find('div', class_='prd-prices')
    if alternative_price_tag:
        alternative_price_text = alternative_price_tag.text.strip()

        alternative_price_text = alternative_price_text.replace('TL', '').replace('.', '').replace(',', '.')
        try:
            alternative_price = float(alternative_price_text)
            return alternative_price
        except ValueError:
            pass

    return None


def scrape_price_from_amazon(soup):
    price_tag = soup.find('span', class_='a-price-whole')
    if price_tag:
        price_text = price_tag.text.strip()
        price_text = price_text.replace('TL', '').replace('.', '').replace(',', '.')
        try:
            price = float(price_text)
            return price
        except ValueError:
            return None
    return None


def scrape_price_from_incehesap(soup):
    price_tag = soup.find('div', class_='price')
    if price_tag:
        price_text = price_tag.text.strip()
        price_text = price_text.replace('TL', '').replace('.', '').replace(',', '.')
        try:
            price = float(price_text)
            return price
        except ValueError:
            return None
    return None


def scrape_price_from_apple(soup):
    price_tag = soup.find('span', class_='rc-prices-fullprice')
    if price_tag:
        price_text = price_tag.get_text.split()
        price_text = price_text.replace('TL', '').replace('.', '').replace(',', '.')
        try:
            price = float(price_text)
            return price
        except ValueError:
            return None
    return None


def scrape_price_from_akakce(soup):
    price_tag = soup.find('span', class_='pt_v8')
    if price_tag:
        price_text = price_tag.text.strip()
        price_text = price_text.replace('TL', '').replace('.', '').replace(',', '.')
        try:
            price = float(price_text)
            return price
        except ValueError:
            return None
    return None

def scrape_price_from_hepsiburada(soup):
    price_tag = soup.find('del', class_='price-old')
    if price_tag:
        price_text = price_tag.text.strip()
        price_text = price_text.replace('TL', '').replace('.', '').replace(',', '.')
        try:
            price = float(price_text)
            return price
        except ValueError:
            return None
    return None

def scrape_price_from_n(soup):
    product_real_price_input = soup.find('input', {'id': 'productRealPrice', 'data-price': True})
    if product_real_price_input:
        price_text = product_real_price_input['data-price']
        price_text = price_text.replace(' TL', '').replace('.', '').replace(',', '.')
        try:
            price = float(price_text)
            return price
        except ValueError:
            return None
    return None

if __name__ == "__main__":
    app.run(debug=True)
