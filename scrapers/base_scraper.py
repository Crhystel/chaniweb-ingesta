import logging
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """Clase base que define la estructura general de un scraper."""

    @abstractmethod
    def run(self):
        """Método principal para ejecutar el scraping."""
        pass

    def safe_run(self):
        """Ejecuta el scraper con manejo de errores."""
        try:
            self.run()
        except Exception as e:
            logging.error(f"Error en {self.__class__.__name__}: {e}")
