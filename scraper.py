import logging
import time
from scrapers.frecuente_scraper import FrecuentoScraper
from scrapers.aki_scraper import AkiScraper
from utils.backend_utils import wait_for_backend

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    if wait_for_backend():
        while True:
            AkiScraper().safe_run()
            FrecuentoScraper().safe_run()
            logging.info("💤 Durmiendo 1 hora...")
            time.sleep(3600)
