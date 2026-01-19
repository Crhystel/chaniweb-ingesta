import time
import requests
import logging
import os

API_URL = os.getenv("API_URL", "http://backend:8000/ingest/")
HEALTH_URL = os.getenv("API_URL", "http://backend:8000/products/").replace("/ingest/", "/products/")

def wait_for_backend():
    logging.info(f"🔍 Esperando backend en: {HEALTH_URL}")
    for _ in range(10):
        try:
            r = requests.get(HEALTH_URL, timeout=5)
            if r.status_code == 200:
                logging.info("Backend operativo.")
                return True
        except:
            pass
        time.sleep(3)
    logging.error("Backend no responde.")
    return False

def send_to_backend(products):
    if not products: return
    try:
        r = requests.post(API_URL, json=products)
        if r.status_code in [200, 201]:
            logging.info(f"Enviados {len(products)} productos al backend.")
        else:
            logging.error(f"Error Backend ({r.status_code}): {r.text}")
    except Exception as e:
        logging.error(f"Error enviando datos: {e}")

