import logging
import importlib

# Configurar logs claros
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Lista de scrapers reales --- #
SCRAPERS = [
    "scrapers.frecuente_scraper",
    "scrapers.mock_scraper",                  
]


def ejecutar_scraper(scraper_mod):
    """Carga dinámicamente y ejecuta un scraper una sola vez."""
    nombre = scraper_mod.split(".")[-1]
    try:
        logging.info(f"Ejecutando {nombre}...")

        # Importa el módulo dinámicamente
        modulo = importlib.import_module(scraper_mod)

        # Convierte el nombre del archivo en el nombre de la clase (ej: frecuente_scraper -> FrecuentoScraper)
        clase_nombre = "".join([p.capitalize() for p in nombre.split("_")])
        clase_scraper = getattr(modulo, clase_nombre)

        # Instancia la clase y ejecuta
        scraper = clase_scraper()
        scraper.run_scraper_once()

        logging.info(f"{nombre} finalizado correctamente.\n")

    except Exception as e:
        logging.error(f"Error en {nombre}: {e}\n")


def main():
    logging.info("🚀 Iniciando ejecución de scrapers...")
    for scraper_mod in SCRAPERS:
        ejecutar_scraper(scraper_mod)
    logging.info("Todos los scrapers ejecutados.")


if __name__ == "__main__":
    main()
