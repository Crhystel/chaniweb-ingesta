import requests
import time

API_URL = "http://backend:8000/productos"

mock_data = [
    {"name": "Arroz Conejo 1kg", "price": 1.20, "unit": "kg", "quantity": 1.0, "source": "Supermaxi"},
    {"name": "Arroz Conejo 500g", "price": 0.70, "unit": "gr", "quantity": 500.0, "source": "Mi Comisariato"},
    {"name": "Leche Entera 1L", "price": 0.95, "unit": "lt", "quantity": 1.0, "source": "Aki"},
    {"name": "Aceite Palma 900ml", "price": 2.50, "unit": "ml", "quantity": 900.0, "source": "Supermaxi"}
]

def run_ingesta():
    print("Iniciando Ingesta de Datos...")
    for item in mock_data:
        try:
            response = requests.post(API_URL, json=item)
            if response.status_code == 200:
                print(f"Insertado: {item['name']} desde {item['source']}")
        except Exception as e:
            print(f"Error conectando al backend: {e}")

if __name__ == "__main__":
    time.sleep(5) # Esperar a que el backend suba
    run_ingesta()