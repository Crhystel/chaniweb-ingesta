import time
import re
import logging
import hashlib
from playwright.sync_api import sync_playwright
from scrapers.base_scraper import BaseScraper
from utils.backend_utils import send_to_backend

AKI_URLS = [
    {"name": "Alacena-Canola", "url": "https://www.aki.com.ec/categoria/alacena/aceites-y-grasas-alacena/canola-aceites-y-grasas-alacena/"},
    {"name": "Alacena-Girasol", "url": "https://www.aki.com.ec/categoria/alacena/aceites-y-grasas-alacena/girasol-aceites-y-grasas-alacena/"},
    {"name": "Alacena-Arroz", "url": "https://www.aki.com.ec/categoria/alacena/arroz-alacena/blanco-arroz-alacena/"},
]

class AkiScraper(BaseScraper):

    def run(self):
        logging.info("Iniciando scraper de AKI (modo Tumbaco)...")
        total_aki = 0
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
                context = browser.new_context(
                    geolocation={"latitude": -0.2133, "longitude": -78.3996},
                    permissions=["geolocation"],
                    locale="es-EC",
                    timezone_id="America/Guayaquil"
                )
                page = context.new_page()

                for cat in AKI_URLS:
                    logging.info(f"AKI: {cat['name']}")
                    try:
                        page.goto(cat['url'], timeout=90000, wait_until="domcontentloaded")
                        time.sleep(5)
                        page.keyboard.press("Escape")

                        product_cards = page.locator('.product').all()
                        if not product_cards:
                            logging.warning(f"Sin productos en {cat['name']}")
                            continue

                        batch = []
                        for card in product_cards:
                            try:
                                name_el = card.locator('.woocommerce-loop-product__title').first
                                name = name_el.inner_text().strip() if name_el.count() > 0 else "Sin Nombre"
                                full_text = card.inner_text()
                                matches = re.findall(r'\$?\s?(\d+[\.,]\d{2})', full_text)
                                price = float(matches[0].replace(',', '.')) if matches else 0
                                img_el = card.locator('img').first
                                img = img_el.get_attribute('src') if img_el.count() > 0 else ""
                                ext_id = f"aki-{hashlib.md5(name.encode()).hexdigest()[:10]}"
                                if price > 0:
                                    batch.append({
                                        "supermarket": "AKI",
                                        "external_id": ext_id,
                                        "name": name,
                                        "price": price,
                                        "image_url": img,
                                        "category": f"AKI-{cat['name']}"
                                    })
                            except:
                                pass

                        if batch:
                            send_to_backend(batch)
                            total_aki += len(batch)
                            logging.info(f"   -> {len(batch)} productos enviados desde {cat['name']}")
                    except Exception as e:
                        logging.error(f"Error AKI {cat['name']}: {e}")

                browser.close()
                logging.info(f"🏁 AKI Finalizado ({total_aki} productos).")

        except Exception as e:
            logging.error(f"Error global AKI: {e}")
