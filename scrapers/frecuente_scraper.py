import time
import logging
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from scrapers.base_scraper import BaseScraper
from utils.backend_utils import send_to_backend

PALABRAS_CLAVE_COMIDA = ["despensa", "alimentos", "arroz", "aceite", "atun", "leche", "carnes", "pollo", "bebidas", "huevos", "queso", "frutas", "verduras"]
PALABRAS_EXCLUIDAS = ["mascotas", "hogar", "electro", "escolar"]

URL_CATEGORIAS = "https://app.frecuento.com/categories/?image_quality=100"
URL_PRODUCTOS = "https://app.frecuento.com/products/"

class FrecuentoScraper(BaseScraper):

    def obtener_headers_auth(self):
        logging.info("Obteniendo cookies desde Frecuento...")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.goto("https://www.frecuento.com/", timeout=60000)
                time.sleep(5)
                cookies = context.cookies()
                cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
                browser.close()
                return {
                    "authority": "app.frecuento.com",
                    "accept": "application/json, text/plain, */*",
                    "user-agent": "Mozilla/5.0",
                    "cookie": cookie_str,
                    "origin": "https://www.frecuento.com",
                    "referer": "https://www.frecuento.com/"
                }
        except Exception as e:
            logging.error(f"Error Playwright: {e}")
            return None

    def es_comida(self, nombre):
        n = nombre.lower()
        if any(x in n for x in PALABRAS_EXCLUIDAS):
            return False
        return any(x in n for x in PALABRAS_CLAVE_COMIDA)

    def run(self):
        headers = self.obtener_headers_auth()
        if not headers:
            return
        
        logging.info("Descargando categorías...")
        try:
            r = requests.get(URL_CATEGORIAS, headers=headers)
            data = r.json()
        except Exception as e:
            logging.error(f"Error categorías: {e}")
            return

        cats = []
        def extraer(items):
            for i in items:
                if i.get('id') and self.es_comida(i.get('name', '')):
                    cats.append(i)
                if i.get('children'): extraer(i['children'])
                if i.get('subcategories'): extraer(i['subcategories'])
        
        raiz = data if isinstance(data, list) else data.get('data', [])
        extraer(raiz)
        logging.info(f"{len(cats)} categorías encontradas.")

        total = 0
        for cat in cats:
            logging.info(f"Procesando {cat['name']}")
            start, limit = 0, 50
            while True:
                params = {"category": cat['id'], "stock": "true", "start": start, "limit": limit}
                try:
                    r = requests.get(URL_PRODUCTOS, headers=headers, params=params)
                    if r.status_code != 200: break
                    d = r.json()
                    items = d.get('results') or d.get('products') or []
                    if not items: break

                    batch = []
                    for p in items:
                        precio = p.get('amount_total') or p.get('price') or 0
                        img = ""
                        if p.get('images'): img = p['images'][0]
                        elif p.get('media'): img = p['media'][0].get('url')

                        batch.append({
                            "supermarket": "Mi Comisariato",
                            "external_id": str(p.get('id')),
                            "name": p.get('name'),
                            "price": float(precio),
                            "image_url": img,
                            "category": cat['name']
                        })
                    if batch:
                        send_to_backend(batch)
                        total += len(batch)
                        logging.info(f"   -> {len(batch)} productos enviados.")
                    start += limit
                    time.sleep(1)
                except Exception as e:
                    logging.error(f"Error productos {cat['name']}: {e}")
                    break
        logging.info(f"🏁 Finalizado Frecuento ({total} productos).")
