import time
import logging
import requests
from playwright.sync_api import sync_playwright
from scrapers.base_scraper import BaseScraper
from utils.backend_utils import send_to_backend

URL_CATEGORIAS = "https://app.frecuento.com/categories/?image_quality=100"
URL_PRODUCTOS = "https://app.frecuento.com/products/"

# 🔍 Solo estas categorías nos interesan
CATEGORIAS_OBJETIVO = {
    "leche": "Leche",
    "arroz": "Arroz",
    "aceite": "Aceite",
    "azúcar": "Azúcar"
}


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

    def categoria_valida(self, nombre):
        """Devuelve el nombre normalizado si la categoría es de interés."""
        n = nombre.lower()
        for palabra, etiqueta in CATEGORIAS_OBJETIVO.items():
            if palabra in n:
                return etiqueta
        return None

    def format_product(self, p, cat_name):
        """Transforma el producto al formato esperado por el backend."""
        precio = p.get('amount_total') or p.get('price') or 0
        img = ""
        if p.get('images'):
            img = p['images'][0]
        elif p.get('media'):
            img = p['media'][0].get('url')

        return {
            "supermarket": "Mi Comisariato",
            "external_id": str(p.get('id')),
            "name": p.get('name', ''),       # usamos slug_name
            "price": float(precio),
            "image_url": img,
            "category": cat_name,                 # ya normalizada
            "unit": "unidad",
            "quantity": 1,
            "source": "frecuento"
        }

    def run_scraper_once(self):
        """Ejecuta una sola pasada del scraping."""
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
                nombre_categoria = i.get('name', '').lower()
                categoria_filtrada = self.categoria_valida(nombre_categoria)
                if i.get('id') and categoria_filtrada:
                    # guardamos categoría válida con nombre normalizado
                    cats.append({
                        "id": i['id'],
                        "name": categoria_filtrada
                    })
                if i.get('children'): extraer(i['children'])
                if i.get('subcategories'): extraer(i['subcategories'])
        
        raiz = data if isinstance(data, list) else data.get('data', [])
        extraer(raiz)
        logging.info(f"{len(cats)} categorías válidas encontradas.")

        total = 0
        for cat in cats:
            logging.info(f"Procesando categoría: {cat['name']}")
            start, limit = 0, 20  # límite grande por si queremos buscar más luego
            productos_extraidos = 0

            params = {"category": cat['id'], "stock": "true", "start": start, "limit": limit}
            try:
                r = requests.get(URL_PRODUCTOS, headers=headers, params=params)
                if r.status_code != 200:
                    continue
                d = r.json()
                items = d.get('results') or d.get('products') or []
                if not items:
                    continue

                for p in items:
                    if productos_extraidos >= 2:
                        break  # solo 2 productos por categoría

                    producto = self.format_product(p, cat['name'])
                    send_to_backend(producto)
                    productos_extraidos += 1
                    total += 1
                    logging.info(f"   -> Enviado producto: {producto['name']}")
                    time.sleep(0.2)  # pequeña pausa entre envíos

                time.sleep(1)
            except Exception as e:
                logging.error(f"Error productos {cat['name']}: {e}")
                continue

        logging.info(f"🏁 Finalizado Frecuento ({total} productos).")

    def run(self):
        """Ejecuta el scraper una sola vez cada hora."""
        while True:
            self.run_scraper_once()
            logging.info("Esperando 1 hora para la próxima ejecución...")
            time.sleep(3600)
