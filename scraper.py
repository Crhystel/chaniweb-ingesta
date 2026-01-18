import requests
import os
import time
import redis
import json
from concurrent.futures import ThreadPoolExecutor
import threading

REDIS_URL = os.getenv("REDIS_URL")
API_URL = os.getenv("API_URL")

# Conexión a Redis para colas
redis_client = redis.from_url(REDIS_URL)

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
    """Publica un producto a la cola Redis"""
    try:
        redis_client.lpush('products_queue', json.dumps(product))
        print(f" Publicado: {product['name']} a la cola")
    except Exception as e:
        print(f" Error publicando {product['name']}: {e}")

def load_data_async():
    """Carga datos usando colas Redis (comunicación asíncrona)"""
    print(" Iniciando carga asíncrona de datos...")
    
    # Publicar todos los productos a la cola
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(publish_to_queue, item) for item in mock_inventory]
        
        for future in futures:
            future.result()
    
    print(f" {len(mock_inventory)} productos encolados exitosamente")

def load_data_sync():
    """Mantiene compatibilidad con HTTP directo (fallback)"""
    print(f" Enviando datos por HTTP a {API_URL}...")
    for item in mock_inventory:
        try:
            res = requests.post(API_URL, json=item, timeout=5)
            if res.status_code == 200:
                print(f" HTTP: {item['name']} cargado.")
            else:
                print(f" HTTP Error {res.status_code}: {item['name']}")
        except Exception as e:
            print(f" HTTP Error: {e}")

if __name__ == "__main__":
    time.sleep(10)  # Esperar a que Redis esté listo
    
    # Intentar comunicación asíncrona primero
    try:
        load_data_async()
    except Exception as e:
        print(f" Fallo en modo asíncrono: {e}")
        print(" Usando modo síncrono como fallback...")
        load_data_sync()