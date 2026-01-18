import requests
import os
import time
import redis
import json
from concurrent.futures import ThreadPoolExecutor
import threading

# Variables de entorno con valores por defecto
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
API_URL = os.getenv("API_URL", "http://backend:8000/productos")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "3"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))

# Conexión a Redis para colas
try:
    redis_client = redis.from_url(REDIS_URL)
    redis_client.ping()  # Verificar conexión
    print(f" Conectado a Redis: {REDIS_URL}")
except Exception as e:
    print(f" Error conectando a Redis: {e}")
    exit(1)

mock_inventory = [
    {"name": "Arroz", "price": 1.25, "unit": "kg", "quantity": 1, "source": "Supermaxi"},
    {"name": "Arroz", "price": 0.65, "unit": "g", "quantity": 500, "source": "Aki"},
    {"name": "Arroz", "price": 1.10, "unit": "kg", "quantity": 1, "source": "Tía"},
    {"name": "Leche", "price": 0.90, "unit": "lt", "quantity": 1, "source": "Supermaxi"},
    {"name": "Leche", "price": 0.85, "unit": "lt", "quantity": 1, "source": "Aki"},
    {"name": "Leche", "price": 0.95, "unit": "lt", "quantity": 1, "source": "Tía"},
    {"name": "Aceite", "price": 2.50, "unit": "ml", "quantity": 900, "source": "Supermaxi"},
    {"name": "Aceite", "price": 2.80, "unit": "ml", "quantity": 900, "source": "Aki"},
    {"name": "Azúcar", "price": 1.80, "unit": "kg", "quantity": 1, "source": "Supermaxi"},
    {"name": "Azúcar", "price": 1.65, "unit": "kg", "quantity": 1, "source": "Aki"}
]

def publish_to_queue(product):
    """Publica un producto a la cola Redis con reintentos"""
    for attempt in range(RETRY_ATTEMPTS):
        try:
            redis_client.lpush('products_queue', json.dumps(product))
            print(f" Publicado: {product['name']} ({product['source']}) a la cola")
            return True
        except Exception as e:
            print(f" Intento {attempt + 1}/{RETRY_ATTEMPTS} publicando {product['name']}: {e}")
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY)
    return False

def load_data_async():
    """Carga datos usando colas Redis (comunicación asíncrona)"""
    print(" Iniciando carga asíncrona de datos...")
    
    # Publicar todos los productos a la cola en paralelo
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(publish_to_queue, item) for item in mock_inventory]
        
        # Esperar a que todos terminen
        results = [future.result() for future in futures]
    
    successful = sum(results)
    print(f" {successful}/{len(mock_inventory)} productos encolados exitosamente")
    return successful

def load_data_sync():
    """Mantiene compatibilidad con HTTP directo (fallback)"""
    print(f" Enviando datos por HTTP a {API_URL}...")
    successful = 0
    for item in mock_inventory:
        for attempt in range(RETRY_ATTEMPTS):
            try:
                res = requests.post(API_URL, json=item, timeout=10)
                if res.status_code == 200:
                    print(f" HTTP: {item['name']} ({item['source']}) cargado.")
                    successful += 1
                    break
                else:
                    print(f" HTTP Error {res.status_code}: {item['name']}")
            except Exception as e:
                print(f" HTTP Error (intento {attempt + 1}): {e}")
                if attempt < RETRY_ATTEMPTS - 1:
                    time.sleep(RETRY_DELAY)
    
    print(f" {successful}/{len(mock_inventory)} productos cargados vía HTTP")
    return successful

if __name__ == "__main__":
    startup_delay = int(os.getenv("STARTUP_DELAY", "10"))
    print(f" Esperando {startup_delay}s para que los servicios estén listos...")
    time.sleep(startup_delay)
    
    # Intentar comunicación asíncrona primero
    try:
        successful = load_data_async()
        if successful == len(mock_inventory):
            print(" Todos los productos cargados exitosamente vía Redis")
        else:
            print(" Algunos productos fallaron, intentando fallback HTTP...")
            load_data_sync()
    except Exception as e:
        print(f" Fallo en modo asíncrono: {e}")
        print(" Usando modo síncrono como fallback...")
        load_data_sync()