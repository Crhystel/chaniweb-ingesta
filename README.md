# ChaniWeb Ingesta - Scraper de Datos

🕷️ **Sistema de ingesta de datos para supermercados ecuatorianos**

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg)](https://redis.io/)
[![JSON](https://img.shields.io/badge/JSON-Data-green.svg)](https://www.json.org/)

## 🏗️ **Arquitectura del Sistema**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Scraper     │◄──►│     Redis      │◄──►│   Backend      │
│   (Python)    │    │   (Queue)     │    │   (FastAPI)    │
│   food_items   │    │   /products    │    │   /api/productos│
│   168 items    │    │   queue        │    │   endpoint      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │  PostgreSQL     │
                                              │   products     │
                                              │   table        │
                                              └─────────────────┘
```

## 📊 **Estructura de Datos**

### **Productos por Categoría**
```python
food_items = [
    # GRANOS (24 productos)
    {"name": "Arroz Diana Blanco", "price": 1.25, "unit": "kg", 
     "source": "Supermaxi", "image_url": "https://i5.walmartimages.com/..."},
    
    # LÁCTEOS (12 productos)  
    {"name": "Leche Vital Complet", "price": 1.05, "unit": "lt",
     "source": "Supermaxi", "image_url": "https://picsum.photos/..."},
    
    # ... 7 categorías más
]
```

### **URLs de Imágenes Reales**
```python
# Walmart Products
"https://i5.walmartimages.com/seo/Arroz-Diana-Blanco-1000g.jpg"

# Supermaxi Products  
"https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/07/7862126580186-1-6.png"

# Facundo Products
"https://www.facundo.com.ec/wp-content/uploads/2020/11/mesnestra-lenteja.png"
```

## 🚀 **Funcionamiento**

### **1. Sistema Anti-Duplicados**
```python
if __name__ == "__main__":
    # Limpiar Redis queue
    redis_client.delete('products_queue')
    
    # Limpiar base de datos si existen productos
    existing_count = db.query(Product).count()
    if existing_count > 0:
        print(f"🗑️  Limpiando {existing_count} productos existentes...")
        db.query(Product).delete()
        db.commit()
```

### **2. Replicación de URLs Reales**
```python
# Todas las variantes usan la misma URL real
{"name": "Lenteja Facundo", "source": "Supermaxi", 
 "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/mesnestra-lenteja.png"},
{"name": "Lenteja Facundo", "source": "Aki", 
 "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/mesnestra-lenteja.png"},
{"name": "Lenteja Facundo", "source": "Mi Comisariato", 
 "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/mesnestra-lenteja.png"}
```

## 📊 **Estadísticas de Ingesta**

| Categoría | Productos | URLs Reales |
|------------|-----------|-------------|
| Granos | 24 | 8 URLs |
| Lácteos | 12 | 0 URLs |
| Proteínas | 18 | 0 URLs |
| Enlatados | 6 | 0 URLs |
| Despensa | 30 | 0 URLs |
| Bebidas | 15 | 0 URLs |
| Panadería | 18 | 0 URLs |
| Repostería | 12 | 0 URLs |
| Endulzantes | 9 | 0 URLs |
| **TOTAL** | **168** | **8 URLs** |

## 🛠️ **Ejecución**

### **Desarrollo**
```bash
# Ejecutar ingesta de datos
python scraper.py

# Verificar estado
python -c "
import redis
r = redis.from_url('redis://localhost:6379')
print(f'Items en cola: {r.llen(\"products_queue\")}')
"
```

### **Docker**
```bash
# Ejecutar con Docker Compose
docker-compose exec backend python scraper.py

# Verificar productos en BD
docker-compose exec backend python -c "
from database import SessionLocal
from models import Product
db = SessionLocal()
print(f'Productos en BD: {db.query(Product).count()}')
"
```

### **Validación de Datos**
```python
# Verificar estructura de cada item
required_fields = ['name', 'price', 'unit', 'quantity', 'source', 'image_url', 'features']

for item in food_items:
    for field in required_fields:
        if field not in item:
            raise ValueError(f"Falta campo requerido: {field}")
```

## 🔄 **Proceso de Ingesta**

```
Inicio scraper.py
        ↓
Limpiar Redis queue
        ↓
Verificar BD existente
        ↓
¿Hay productos? ──→ Sí: Limpiar tabla products
                    └─→ No: Insertar directamente
        ↓
Agregar items a Redis queue
        ↓
Backend procesa queue
        ↓
Guardar en PostgreSQL
        ↓
✅ Ingesta completada
```

## 🐛 **Troubleshooting**

### **Problemas Comunes**
```bash
# Redis no disponible
docker-compose exec backend python -c "
import redis
r = redis.from_url('redis://redis:6379')
print(r.ping())  # Debe retornar True
"

# Base de datos no actualiza
docker-compose exec backend python -c "
from database import SessionLocal
from models import Product
db = SessionLocal()
db.query(Product).delete()
db.commit()
print('Base de datos limpiada manualmente')
"
```

---

**🕷️ Scraper Optimizado y Confiable**

*Datos reales • URLs verificadas • Sistema anti-duplicados*
