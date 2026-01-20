import os, time, redis, json

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
redis_client = redis.from_url(REDIS_URL)

food_items = [
    # --- GRUPO 1: ARROZ Y GRANOS ---
    {"name": "Arroz Diana Blanco", "price": 1.18, "unit": "kg", "quantity": 1, "source": "Supermaxi", "image_url": "https://i5.walmartimages.com/seo/Arroz-Diana-Blanco-1000g-35-27-oz-Premium-White-Rice-from-Colombia_cfbf88cb-679f-4c93-a9f5-5fe715bcdefe.a2f1430e4555d66d83ed9f6d47c8f13a.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF", "features": ["Grano largo", "Vitamina A", "99% Entero"]},
    {"name": "Arroz Diana Blanco", "price": 1.25, "unit": "kg", "quantity": 1, "source": "Aki", "image_url": "https://i5.walmartimages.com/seo/Arroz-Diana-Blanco-1000g-35-27-oz-Premium-White-Rice-from-Colombia_cfbf88cb-679f-4c93-a9f5-5fe715bcdefe.a2f1430e4555d66d83ed9f6d47c8f13a.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF", "features": ["Grano largo", "Vitamina A", "99% Entero"]},
    {"name": "Arroz Diana Blanco", "price": 1.20, "unit": "kg", "quantity": 1, "source": "Mi Comisariato", "image_url": "https://i5.walmartimages.com/seo/Arroz-Diana-Blanco-1000g-35-27-oz-Premium-White-Rice-from-Colombia_cfbf88cb-679f-4c93-a9f5-5fe715bcdefe.a2f1430e4555d66d83ed9f6d47c8f13a.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF", "features": ["Grano largo", "Vitamina A", "99% Entero"]},

    {"name": "Arroz Conejo", "price": 1.35, "unit": "kg", "quantity": 1, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/07/7862126580186-1-6.png", "features": ["Grano seleccionado", "Envejecido", "Súper extra"]},
    {"name": "Arroz Conejo", "price": 1.30, "unit": "kg", "quantity": 1, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/07/7862126580186-1-6.png", "features": ["Grano seleccionado", "Envejecido", "Súper extra"]},
    {"name": "Arroz Conejo", "price": 1.28, "unit": "kg", "quantity": 1, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/07/7862126580186-1-6.png", "features": ["Grano seleccionado", "Envejecido", "Súper extra"]},

    {"name": "Lenteja Facundo", "price": 1.10, "unit": "g", "quantity": 425, "source": "Supermaxi", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/mesnestra-lenteja.png", "features": ["Grano seco", "Sin impurezas", "Alto hierro"]},
    {"name": "Lenteja Facundo", "price": 1.15, "unit": "g", "quantity": 425, "source": "Aki", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/mesnestra-lenteja.png", "features": ["Grano seco", "Sin impurezas", "Alto hierro"]},
    {"name": "Lenteja Facundo", "price": 1.05, "unit": "g", "quantity": 425, "source": "Mi Comisariato", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/mesnestra-lenteja.png", "features": ["Grano seco", "Sin impurezas", "Alto hierro"]},

    {"name": "Garbanzos Facundo", "price": 1.45, "unit": "g", "quantity": 425, "source": "Supermaxi", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/vc-garbanzo.png", "features": ["Grano tierno", "Para ensaladas", "Proteína vegetal"]},
    {"name": "Garbanzos Facundo", "price": 1.40, "unit": "g", "quantity": 425, "source": "Aki", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/vc-garbanzo.png", "features": ["Grano tierno", "Para ensaladas", "Proteína vegetal"]},
    {"name": "Garbanzos Facundo", "price": 1.50, "unit": "g", "quantity": 425, "source": "Mi Comisariato", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/vc-garbanzo.png", "features": ["Grano tierno", "Para ensaladas", "Proteína vegetal"]},

    # --- GRUPO 2: LÁCTEOS Y DERIVADOS ---
    {"name": "Leche Toni Entera", "price": 1.05, "unit": "lt", "quantity": 1, "source": "Supermaxi", "image_url": "https://statics.tipti.market/product-media/5d26de77-da1a-4a6a-a487-08281f51d250.jpg", "features": ["Tetra Pak", "Fortificada", "100% Leche"]},
    {"name": "Leche Toni Entera", "price": 1.08, "unit": "lt", "quantity": 1, "source": "Aki", "image_url": "https://statics.tipti.market/product-media/5d26de77-da1a-4a6a-a487-08281f51d250.jpg", "features": ["Tetra Pak", "Fortificada", "100% Leche"]},
    {"name": "Leche Toni Entera", "price": 1.00, "unit": "lt", "quantity": 1, "source": "Mi Comisariato", "image_url": "https://statics.tipti.market/product-media/5d26de77-da1a-4a6a-a487-08281f51d250.jpg", "features": ["Tetra Pak", "Fortificada", "100% Leche"]},

    {"name": "Leche Vita Entera", "price": 0.92, "unit": "lt", "quantity": 1, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/06/7861029404780-1-10.jpg", "features": ["En funda", "Tradicional", "Fresca"]},
    {"name": "Leche Vita Entera", "price": 0.90, "unit": "lt", "quantity": 1, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/06/7861029404780-1-10.jpg", "features": ["En funda", "Tradicional", "Fresca"]},
    {"name": "Leche Vita Entera", "price": 0.95, "unit": "lt", "quantity": 1, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/06/7861029404780-1-10.jpg", "features": ["En funda", "Tradicional", "Fresca"]},

    {"name": "Yogurt Persa Galón", "price": 4.20, "unit": "lt", "quantity": 2, "source": "Supermaxi", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/112299_G.jpg", "features": ["Sabor fresa", "Con trozos", "Probiótico"]},
    {"name": "Yogurt Persa Galón", "price": 3.95, "unit": "lt", "quantity": 2, "source": "Aki", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/112299_G.jpg", "features": ["Sabor fresa", "Con trozos", "Probiótico"]},
    {"name": "Yogurt Persa Galón", "price": 4.10, "unit": "lt", "quantity": 2, "source": "Mi Comisariato", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/112299_G.jpg", "features": ["Sabor fresa", "Con trozos", "Probiótico"]},

    # --- GRUPO 3: PROTEÍNAS (CARNE, POLLO, HUEVOS, JAMÓN) ---
    {"name": "Pollo Entero Mr. Pollo", "price": 8.10, "unit": "kg", "quantity": 2.2, "source": "Supermaxi", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/58142_M.jpg", "features": ["Fresco", "Sin vísceras", "Alto rendimiento"]},
    {"name": "Pollo Entero Mr. Pollo", "price": 8.50, "unit": "kg", "quantity": 2.2, "source": "Aki", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/58142_M.jpg", "features": ["Fresco", "Sin vísceras", "Alto rendimiento"]},
    {"name": "Pollo Entero Mr. Pollo", "price": 7.95, "unit": "kg", "quantity": 2.2, "source": "Mi Comisariato", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/58142_M.jpg", "features": ["Fresco", "Sin vísceras", "Alto rendimiento"]},

    {"name": "Huevos Indaves (12 ud)", "price": 1.95, "unit": "unidad", "quantity": 12, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7861022900036-1-2.jpg", "features": ["Frescura garantizada", "Grandes", "Proteína"]},
    {"name": "Huevos Indaves (12 ud)", "price": 2.10, "unit": "unidad", "quantity": 12, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7861022900036-1-2.jpg", "features": ["Frescura garantizada", "Grandes", "Proteína"]},
    {"name": "Huevos Indaves (12 ud)", "price": 2.00, "unit": "unidad", "quantity": 12, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7861022900036-1-2.jpg", "features": ["Frescura garantizada", "Grandes", "Proteína"]},

    {"name": "Jamón de Espalda Juris", "price": 2.80, "unit": "g", "quantity": 250, "source": "Supermaxi", "image_url": "https://www.eureka.com.ec/clasica/5687-large_default/jamon-de-espalda-tipo-i-juris-200-g.jpg", "features": ["Económico", "Rebanado", "Sabor ahumado"]},
    {"name": "Jamón de Espalda Juris", "price": 2.65, "unit": "g", "quantity": 250, "source": "Aki", "image_url": "https://www.eureka.com.ec/clasica/5687-large_default/jamon-de-espalda-tipo-i-juris-200-g.jpg", "features": ["Económico", "Rebanado", "Sabor ahumado"]},
    {"name": "Jamón de Espalda Juris", "price": 2.75, "unit": "g", "quantity": 250, "source": "Mi Comisariato", "image_url": "https://www.eureka.com.ec/clasica/5687-large_default/jamon-de-espalda-tipo-i-juris-200-g.jpg", "features": ["Económico", "Rebanado", "Sabor ahumado"]},

    {"name": "Carne Molida Especial", "price": 3.90, "unit": "kg", "quantity": 0.5, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/68406-1-3.jpg", "features": ["90% Magra", "Res fresca", "Ideal hamburguesas"]},
    {"name": "Carne Molida Especial", "price": 3.75, "unit": "kg", "quantity": 0.5, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/68406-1-3.jpg", "features": ["90% Magra", "Res fresca", "Ideal hamburguesas"]},
    {"name": "Carne Molida Especial", "price": 3.85, "unit": "kg", "quantity": 0.5, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/68406-1-3.jpg", "features": ["90% Magra", "Res fresca", "Ideal hamburguesas"]},

    # --- GRUPO 4: ENLATADOS ---
    {"name": "Atún Real en Aceite", "price": 1.55, "unit": "g", "quantity": 170, "source": "Supermaxi", "image_url": "https://distribuidoralatinoandina.com/media/2021/09/REA020.jpg", "features": ["Lomitos", "Omega 3", "Abre fácil"]},
    {"name": "Atún Real en Aceite", "price": 1.45, "unit": "g", "quantity": 170, "source": "Aki", "image_url": "https://distribuidoralatinoandina.com/media/2021/09/REA020.jpg", "features": ["Lomitos", "Omega 3", "Abre fácil"]},
    {"name": "Atún Real en Aceite", "price": 1.60, "unit": "g", "quantity": 170, "source": "Mi Comisariato", "image_url": "https://distribuidoralatinoandina.com/media/2021/09/REA020.jpg", "features": ["Lomitos", "Omega 3", "Abre fácil"]},

    {"name": "Sardinas Real Tomate", "price": 1.10, "unit": "g", "quantity": 155, "source": "Supermaxi", "image_url": "https://www.aki.com.ec/wp-content/uploads/2025/08/7862100602002-1-4.jpg", "features": ["En salsa de tomate", "Calcio", "Listo para comer"]},
    {"name": "Sardinas Real Tomate", "price": 1.20, "unit": "g", "quantity": 155, "source": "Aki", "image_url": "https://www.aki.com.ec/wp-content/uploads/2025/08/7862100602002-1-4.jpg", "features": ["En salsa de tomate", "Calcio", "Listo para comer"]},
    {"name": "Sardinas Real Tomate", "price": 1.05, "unit": "g", "quantity": 155, "source": "Mi Comisariato", "image_url": "https://www.aki.com.ec/wp-content/uploads/2025/08/7862100602002-1-4.jpg", "features": ["En salsa de tomate", "Calcio", "Listo para comer"]},

    # --- GRUPO 5: DESPENSA Y CONDIMENTOS ---
    {"name": "Spaghetti Don Vittorio", "price": 0.82, "unit": "g", "quantity": 400, "source": "Supermaxi", "image_url": "https://www.eureka.com.ec/clasica/1010-large_default/fideo-spaghetti-don-vittorio-400-g.jpg", "features": ["Trigo durum", "No se pega", "Al dente"]},
    {"name": "Spaghetti Don Vittorio", "price": 0.85, "unit": "g", "quantity": 400, "source": "Aki", "image_url": "https://www.eureka.com.ec/clasica/1010-large_default/fideo-spaghetti-don-vittorio-400-g.jpg", "features": ["Trigo durum", "No se pega", "Al dente"]},
    {"name": "Spaghetti Don Vittorio", "price": 0.78, "unit": "g", "quantity": 400, "source": "Mi Comisariato", "image_url": "https://www.eureka.com.ec/clasica/1010-large_default/fideo-spaghetti-don-vittorio-400-g.jpg", "features": ["Trigo durum", "No se pega", "Al dente"]},

    {"name": "Fideo Lucchetti Tallarín", "price": 0.70, "unit": "g", "quantity": 400, "source": "Supermaxi", "image_url": "https://i5.walmartimages.cl/asr/a0afe1e9-2bf2-4dd4-9ede-6cdaa8fff339.51f4e5e79d47ad6b577440c19aedcd01.jpeg", "features": ["Suave", "Rápida cocción", "Familiar"]},
    {"name": "Fideo Lucchetti Tallarín", "price": 0.65, "unit": "g", "quantity": 400, "source": "Aki", "image_url": "https://i5.walmartimages.cl/asr/a0afe1e9-2bf2-4dd4-9ede-6cdaa8fff339.51f4e5e79d47ad6b577440c19aedcd01.jpeg", "features": ["Suave", "Rápida cocción", "Familiar"]},
    {"name": "Fideo Lucchetti Tallarín", "price": 0.68, "unit": "g", "quantity": 400, "source": "Mi Comisariato", "image_url": "https://i5.walmartimages.cl/asr/a0afe1e9-2bf2-4dd4-9ede-6cdaa8fff339.51f4e5e79d47ad6b577440c19aedcd01.jpeg", "features": ["Suave", "Rápida cocción", "Familiar"]},

    {"name": "Comino Molido Ile", "price": 0.45, "unit": "g", "quantity": 30, "source": "Supermaxi", "image_url": "https://www.comisariatoeconomico.com/wp-content/uploads/2025/01/7861021200427.jpg", "features": ["Puro", "Aromático", "Sazón ecuatoriana"]},
    {"name": "Comino Molido Ile", "price": 0.55, "unit": "g", "quantity": 30, "source": "Aki", "image_url": "https://www.comisariatoeconomico.com/wp-content/uploads/2025/01/7861021200427.jpg", "features": ["Puro", "Aromático", "Sazón ecuatoriana"]},
    {"name": "Comino Molido Ile", "price": 0.40, "unit": "g", "quantity": 30, "source": "Mi Comisariato", "image_url": "https://www.comisariatoeconomico.com/wp-content/uploads/2025/01/7861021200427.jpg", "features": ["Puro", "Aromático", "Sazón ecuatoriana"]},

    {"name": "Pimienta Negra Ile", "price": 0.60, "unit": "g", "quantity": 30, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/12/7861021200533-1-15.jpg", "features": ["Molida", "Picante suave", "Condimento"]},
    {"name": "Pimienta Negra Ile", "price": 0.58, "unit": "g", "quantity": 30, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/12/7861021200533-1-15.jpg", "features": ["Molida", "Picante suave", "Condimento"]},
    {"name": "Pimienta Negra Ile", "price": 0.65, "unit": "g", "quantity": 30, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/12/7861021200533-1-15.jpg", "features": ["Molida", "Picante suave", "Condimento"]},

    {"name": "Vinagre Blanco Ile", "price": 0.85, "unit": "ml", "quantity": 500, "source": "Supermaxi", "image_url": "https://www.comisariatoeconomico.com/wp-content/uploads/2025/01/VINILE200.jpg", "features": ["Para ensaladas", "Acidez controlada", "Multiuso"]},
    {"name": "Vinagre Blanco Ile", "price": 0.75, "unit": "ml", "quantity": 500, "source": "Aki", "image_url": "https://www.comisariatoeconomico.com/wp-content/uploads/2025/01/VINILE200.jpg", "features": ["Para ensaladas", "Acidez controlada", "Multiuso"]},
    {"name": "Vinagre Blanco Ile", "price": 0.80, "unit": "ml", "quantity": 500, "source": "Mi Comisariato", "image_url": "https://www.comisariatoeconomico.com/wp-content/uploads/2025/01/VINILE200.jpg", "features": ["Para ensaladas", "Acidez controlada", "Multiuso"]},

    {"name": "Cubitos Maggi Gallina", "price": 0.90, "unit": "unidad", "quantity": 6, "source": "Supermaxi", "image_url": "https://www.eureka.com.ec/clasica/910-large_default/caldo-de-gallina-en-cubo-maggi-120-g-12-x-10-g.jpg", "features": ["Sabor concentrado", "X6 unidades", "Sazón rápida"]},
    {"name": "Cubitos Maggi Gallina", "price": 1.05, "unit": "unidad", "quantity": 6, "source": "Aki", "image_url": "https://www.eureka.com.ec/clasica/910-large_default/caldo-de-gallina-en-cubo-maggi-120-g-12-x-10-g.jpg", "features": ["Sabor concentrado", "X6 unidades", "Sazón rápida"]},
    {"name": "Cubitos Maggi Gallina", "price": 0.85, "unit": "unidad", "quantity": 6, "source": "Mi Comisariato", "image_url": "https://www.eureka.com.ec/clasica/910-large_default/caldo-de-gallina-en-cubo-maggi-120-g-12-x-10-g.jpg", "features": ["Sabor concentrado", "X6 unidades", "Sazón rápida"]},

    {"name": "Pasta de Ajo Ile", "price": 1.20, "unit": "g", "quantity": 100, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7861021206061-1-5.jpg", "features": ["Ajo puro", "Sin conservantes", "Listo para usar"]},
    {"name": "Pasta de Ajo Ile", "price": 1.10, "unit": "g", "quantity": 100, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7861021206061-1-5.jpg", "features": ["Ajo puro", "Sin conservantes", "Listo para usar"]},
    {"name": "Pasta de Ajo Ile", "price": 1.25, "unit": "g", "quantity": 100, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7861021206061-1-5.jpg", "features": ["Ajo puro", "Sin conservantes", "Listo para usar"]},

    # --- GRUPO 6: ACEITES, HARINAS Y MÁS ---
    {"name": "Aceite La Favorita", "price": 2.75, "unit": "ml", "quantity": 900, "source": "Supermaxi", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/117350741_M.jpg", "features": ["Girasol", "Cero colesterol", "Vitamina E"]},
    {"name": "Aceite La Favorita", "price": 2.65, "unit": "ml", "quantity": 900, "source": "Aki", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/117350741_M.jpg", "features": ["Girasol", "Cero colesterol", "Vitamina E"]},
    {"name": "Aceite La Favorita", "price": 2.70, "unit": "ml", "quantity": 900, "source": "Mi Comisariato", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/117350741_M.jpg", "features": ["Girasol", "Cero colesterol", "Vitamina E"]},

    {"name": "Aceite Palma de Oro", "price": 2.40, "unit": "ml", "quantity": 1000, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/06/7861002513126-1-4.jpg", "features": ["Vegetal", "Económico", "Rendidor"]},
    {"name": "Aceite Palma de Oro", "price": 2.45, "unit": "ml", "quantity": 1000, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/06/7861002513126-1-4.jpg", "features": ["Vegetal", "Económico", "Rendidor"]},
    {"name": "Aceite Palma de Oro", "price": 2.35, "unit": "ml", "quantity": 1000, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/06/7861002513126-1-4.jpg", "features": ["Vegetal", "Económico", "Rendidor"]},

    {"name": "Mantequilla Girasol", "price": 1.70, "unit": "g", "quantity": 250, "source": "Supermaxi", "image_url": "https://www.lafabril.com.ec/wp-content/uploads/2017/07/margarina-girasol-01.png", "features": ["Con sal", "Vitamina A y D", "Cremosa"]},
    {"name": "Mantequilla Girasol", "price": 1.65, "unit": "g", "quantity": 250, "source": "Aki", "image_url": "https://www.lafabril.com.ec/wp-content/uploads/2017/07/margarina-girasol-01.png", "features": ["Con sal", "Vitamina A y D", "Cremosa"]},
    {"name": "Mantequilla Girasol", "price": 1.75, "unit": "g", "quantity": 250, "source": "Mi Comisariato", "image_url": "https://www.lafabril.com.ec/wp-content/uploads/2017/07/margarina-girasol-01.png", "features": ["Con sal", "Vitamina A y D", "Cremosa"]},

    {"name": "Harina Ya Multiuso", "price": 1.10, "unit": "kg", "quantity": 1, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861025522303-1-7.jpg", "features": ["Trigo fortificado", "Multiuso", "Sin leudante"]},
    {"name": "Harina Ya Multiuso", "price": 1.05, "unit": "kg", "quantity": 1, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861025522303-1-7.jpg", "features": ["Trigo fortificado", "Multiuso", "Sin leudante"]},
    {"name": "Harina Ya Multiuso", "price": 1.15, "unit": "kg", "quantity": 1, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861025522303-1-7.jpg", "features": ["Trigo fortificado", "Multiuso", "Sin leudante"]},

    {"name": "Azúcar San Carlos", "price": 1.30, "unit": "kg", "quantity": 1, "source": "Supermaxi", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/42702_G.jpg", "features": ["Blanca refinada", "Extra pura", "Postres"]},
    {"name": "Azúcar San Carlos", "price": 1.25, "unit": "kg", "quantity": 1, "source": "Aki", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/42702_G.jpg", "features": ["Blanca refinada", "Extra pura", "Postres"]},
    {"name": "Azúcar San Carlos", "price": 1.35, "unit": "kg", "quantity": 1, "source": "Mi Comisariato", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/42702_G.jpg", "features": ["Blanca refinada", "Extra pura", "Postres"]},

    # --- GRUPO 7: BEBIDAS Y SNACKS ---
    {"name": "Café Buen Día", "price": 3.30, "unit": "g", "quantity": 100, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/05/7707211630493-1.jpg", "features": ["Instantáneo", "Aroma intenso", "Puro"]},
    {"name": "Café Buen Día", "price": 3.45, "unit": "g", "quantity": 100, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/05/7707211630493-1.jpg", "features": ["Instantáneo", "Aroma intenso", "Puro"]},
    {"name": "Café Buen Día", "price": 3.20, "unit": "g", "quantity": 100, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/05/7707211630493-1.jpg", "features": ["Instantáneo", "Aroma intenso", "Puro"]},

    {"name": "Café Nescafé Tradición", "price": 3.80, "unit": "g", "quantity": 100, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/08/7891000431832-1-3.jpg", "features": ["Granulado", "Estandar mundial", "Sabor clásico"]},
    {"name": "Café Nescafé Tradición", "price": 3.65, "unit": "g", "quantity": 100, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/08/7891000431832-1-3.jpg", "features": ["Granulado", "Estandar mundial", "Sabor clásico"]},
    {"name": "Café Nescafé Tradición", "price": 3.75, "unit": "g", "quantity": 100, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/08/7891000431832-1-3.jpg", "features": ["Granulado", "Estandar mundial", "Sabor clásico"]},

    {"name": "Coca Cola Original 3L", "price": 2.95, "unit": "lt", "quantity": 3, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861024630634-1-3.jpg", "features": ["Original", "Familiar", "Refrescante"]},
    {"name": "Coca Cola Original 3L", "price": 3.10, "unit": "lt", "quantity": 3, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861024630634-1-3.jpg", "features": ["Original", "Familiar", "Refrescante"]},
    {"name": "Coca Cola Original 3L", "price": 3.00, "unit": "lt", "quantity": 3, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861024630634-1-3.jpg", "features": ["Original", "Familiar", "Refrescante"]},

    {"name": "Pan Supán Blanco", "price": 2.05, "unit": "g", "quantity": 550, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861009944275-1-11.jpg", "features": ["Suave", "Con calcio", "Sandwiches"]},
    {"name": "Pan Supán Blanco", "price": 2.15, "unit": "g", "quantity": 550, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861009944275-1-11.jpg", "features": ["Suave", "Con calcio", "Sandwiches"]},
    {"name": "Pan Supán Blanco", "price": 1.95, "unit": "g", "quantity": 550, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861009944275-1-11.jpg", "features": ["Suave", "Con calcio", "Sandwiches"]},

    {"name": "Pan Bimbo Artesano", "price": 2.50, "unit": "g", "quantity": 500, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861009944343-1-13.jpg", "features": ["Tipo artesanal", "Grosor especial", "Premium"]},
    {"name": "Pan Bimbo Artesano", "price": 2.40, "unit": "g", "quantity": 500, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861009944343-1-13.jpg", "features": ["Tipo artesanal", "Grosor especial", "Premium"]},
    {"name": "Pan Bimbo Artesano", "price": 2.45, "unit": "g", "quantity": 500, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861009944343-1-13.jpg", "features": ["Tipo artesanal", "Grosor especial", "Premium"]},
    
    # --- GRUPO 8: GRANOS INTEGRALES Y ESPECIALES ---
    {"name": "Arroz Integral Diana", "price": 2.10, "unit": "kg", "quantity": 1, "source": "Supermaxi", "image_url": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12003653/arroz-integral-diana-1.000-g-01.png", "features": ["Alto en fibra", "Natural", "Grano entero"]},
    {"name": "Arroz Integral Diana", "price": 1.95, "unit": "kg", "quantity": 1, "source": "Aki", "image_url": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12003653/arroz-integral-diana-1.000-g-01.png", "features": ["Alto en fibra", "Natural", "Grano entero"]},
    {"name": "Arroz Integral Diana", "price": 2.05, "unit": "kg", "quantity": 1, "source": "Mi Comisariato", "image_url": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12003653/arroz-integral-diana-1.000-g-01.png", "features": ["Alto en fibra", "Natural", "Grano entero"]},

    {"name": "Quinua Real", "price": 3.45, "unit": "g", "quantity": 500, "source": "Supermaxi", "image_url": "https://www.sofiablack.com/3983-medium_default/quinoa-bio-500-gr-quinua-real.jpg", "features": ["Súper alimento", "Lavada", "Orgánica"]},
    {"name": "Quinua Real", "price": 3.60, "unit": "g", "quantity": 500, "source": "Aki", "image_url": "https://www.sofiablack.com/3983-medium_default/quinoa-bio-500-gr-quinua-real.jpg", "features": ["Súper alimento", "Lavada", "Orgánica"]},
    {"name": "Quinua Real", "price": 3.30, "unit": "g", "quantity": 500, "source": "Mi Comisariato", "image_url": "https://www.sofiablack.com/3983-medium_default/quinoa-bio-500-gr-quinua-real.jpg", "features": ["Súper alimento", "Lavada", "Orgánica"]},

    {"name": "Fréjol Rojo Facundo", "price": 1.20, "unit": "g", "quantity": 425, "source": "Supermaxi", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/vc-frejol-rojo-600x600.png", "features": ["Grano seco", "Calidad premium", "Proteína"]},
    {"name": "Fréjol Rojo Facundo", "price": 1.15, "unit": "g", "quantity": 425, "source": "Aki", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/vc-frejol-rojo-600x600.png", "features": ["Grano seco", "Calidad premium", "Proteína"]},
    {"name": "Fréjol Rojo Facundo", "price": 1.25, "unit": "g", "quantity": 425, "source": "Mi Comisariato", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/vc-frejol-rojo-600x600.png", "features": ["Grano seco", "Calidad premium", "Proteína"]},

    {"name": "Fréjol Negro Facundo", "price": 1.10, "unit": "g", "quantity": 425, "source": "Supermaxi", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/vc-frejol-negro.png", "features": ["Ideal para menestras", "Hierro", "Seleccionado"]},
    {"name": "Fréjol Negro Facundo", "price": 1.05, "unit": "g", "quantity": 425, "source": "Aki", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/vc-frejol-negro.png", "features": ["Ideal para menestras", "Hierro", "Seleccionado"]},
    {"name": "Fréjol Negro Facundo", "price": 1.00, "unit": "g", "quantity": 425, "source": "Mi Comisariato", "image_url": "https://www.facundo.com.ec/wp-content/uploads/2020/11/vc-frejol-negro.png", "features": ["Ideal para menestras", "Hierro", "Seleccionado"]},

    # --- GRUPO 9: CARNES Y EMBUTIDOS ---
    {"name": "Lomo de Cerdo", "price": 3.80, "unit": "kg", "quantity": 0.5, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/69037-1-5.jpg", "features": ["Corte magro", "Fresco", "Nacional"]},
    {"name": "Lomo de Cerdo", "price": 3.65, "unit": "kg", "quantity": 0.5, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/69037-1-5.jpg", "features": ["Corte magro", "Fresco", "Nacional"]},
    {"name": "Lomo de Cerdo", "price": 3.50, "unit": "kg", "quantity": 0.5, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/69037-1-5.jpg", "features": ["Corte magro", "Fresco", "Nacional"]},

    {"name": "Chuleta de Cerdo", "price": 3.20, "unit": "kg", "quantity": 0.5, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/66953-1-4.jpg", "features": ["Corte con hueso", "Sabor intenso", "Fresca"]},
    {"name": "Chuleta de Cerdo", "price": 3.10, "unit": "kg", "quantity": 0.5, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/66953-1-4.jpg", "features": ["Corte con hueso", "Sabor intenso", "Fresca"]},
    {"name": "Chuleta de Cerdo", "price": 3.35, "unit": "kg", "quantity": 0.5, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/66953-1-4.jpg", "features": ["Corte con hueso", "Sabor intenso", "Fresca"]},

    {"name": "Tocino Ahumado Plumrose", "price": 3.45, "unit": "g", "quantity": 200, "source": "Supermaxi", "image_url": "https://comisariato.lahabana.ec/wp-content/uploads/2021/05/tocino-ahumado-plumrose-100-gr.jpg", "features": ["Ahumado natural", "Rebanado", "Calidad superior"]},
    {"name": "Tocino Ahumado Plumrose", "price": 3.60, "unit": "g", "quantity": 200, "source": "Aki", "image_url": "https://comisariato.lahabana.ec/wp-content/uploads/2021/05/tocino-ahumado-plumrose-100-gr.jpg", "features": ["Ahumado natural", "Rebanado", "Calidad superior"]},
    {"name": "Tocino Ahumado Plumrose", "price": 3.30, "unit": "g", "quantity": 200, "source": "Mi Comisariato", "image_url": "https://comisariato.lahabana.ec/wp-content/uploads/2021/05/tocino-ahumado-plumrose-100-gr.jpg", "features": ["Ahumado natural", "Rebanado", "Calidad superior"]},

    {"name": "Camarón Pelado", "price": 5.50, "unit": "g", "quantity": 400, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7861002865294-1-3.jpg", "features": ["Exportación", "Desvenado", "Congelado IQF"]},
    {"name": "Camarón Pelado", "price": 5.25, "unit": "g", "quantity": 400, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7861002865294-1-3.jpg", "features": ["Exportación", "Desvenado", "Congelado IQF"]},
    {"name": "Camarón Pelado", "price": 5.10, "unit": "g", "quantity": 400, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7861002865294-1-3.jpg", "features": ["Exportación", "Desvenado", "Congelado IQF"]},

    # --- GRUPO 10: REPOSTERÍA Y MASAS ---
    {"name": "Tortillas de Maíz Mexicanas", "price": 1.75, "unit": "unidad", "quantity": 10, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/12/items2Figm2F1000x10002F7861000170772-1.jpg", "features": ["Sin gluten", "Para tacos", "Sabor original"]},
    {"name": "Tortillas de Maíz Mexicanas", "price": 1.60, "unit": "unidad", "quantity": 10, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/12/items2Figm2F1000x10002F7861000170772-1.jpg", "features": ["Sin gluten", "Para tacos", "Sabor original"]},
    {"name": "Tortillas de Maíz Mexicanas", "price": 1.65, "unit": "unidad", "quantity": 10, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/12/items2Figm2F1000x10002F7861000170772-1.jpg", "features": ["Sin gluten", "Para tacos", "Sabor original"]},

    {"name": "Maicena Duryea", "price": 0.95, "unit": "g", "quantity": 200, "source": "Supermaxi", "image_url": "https://corporacionliderperu.com/50643-home_default/duryea-maizena-bolsa-x-1-kg.jpg", "features": ["Almidón puro", "Para coladas", "Repostería"]},
    {"name": "Maicena Duryea", "price": 0.85, "unit": "g", "quantity": 200, "source": "Aki", "image_url": "https://corporacionliderperu.com/50643-home_default/duryea-maizena-bolsa-x-1-kg.jpg", "features": ["Almidón puro", "Para coladas", "Repostería"]},
    {"name": "Maicena Duryea", "price": 0.90, "unit": "g", "quantity": 200, "source": "Mi Comisariato", "image_url": "https://corporacionliderperu.com/50643-home_default/duryea-maizena-bolsa-x-1-kg.jpg", "features": ["Almidón puro", "Para coladas", "Repostería"]},

    {"name": "Harina de Maíz Sabrosita", "price": 1.10, "unit": "kg", "quantity": 1, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/07/7861029300013-1-16.jpg", "features": ["Maíz amarillo", "Precocida", "Para arepas o tortillas"]},
    {"name": "Harina de Maíz Sabrosita", "price": 1.05, "unit": "kg", "quantity": 1, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/07/7861029300013-1-16.jpg", "features": ["Maíz amarillo", "Precocida", "Para arepas o tortillas"]},
    {"name": "Harina de Maíz Sabrosita", "price": 1.00, "unit": "kg", "quantity": 1, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/07/7861029300013-1-16.jpg", "features": ["Maíz amarillo", "Precocida", "Para arepas o tortillas"]},

    {"name": "Cocoa Nestlé", "price": 2.30, "unit": "g", "quantity": 200, "source": "Supermaxi", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/179904885_G.jpg", "features": ["Pura", "Sin azúcar", "Repostería"]},
    {"name": "Cocoa Nestlé", "price": 2.15, "unit": "g", "quantity": 200, "source": "Aki", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/179904885_G.jpg", "features": ["Pura", "Sin azúcar", "Repostería"]},
    {"name": "Cocoa Nestlé", "price": 2.25, "unit": "g", "quantity": 200, "source": "Mi Comisariato", "image_url": "https://www.supermercadosantamaria.com/documents/10180/10504/179904885_G.jpg", "features": ["Pura", "Sin azúcar", "Repostería"]},

    {"name": "Tapioca Perlas", "price": 0.90, "unit": "g", "quantity": 200, "source": "Supermaxi", "image_url": "https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images/brm/brm11537/y/6.jpg", "features": ["Almidón de yuca", "Natural", "Para postres"]},
    {"name": "Tapioca Perlas", "price": 0.82, "unit": "g", "quantity": 200, "source": "Aki", "image_url": "https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images/brm/brm11537/y/6.jpg", "features": ["Almidón de yuca", "Natural", "Para postres"]},
    {"name": "Tapioca Perlas", "price": 0.88, "unit": "g", "quantity": 200, "source": "Mi Comisariato", "image_url": "https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images/brm/brm11537/y/6.jpg", "features": ["Almidón de yuca", "Natural", "Para postres"]},

    # --- GRUPO 11: PANADERÍA Y GALLETAS ---
    {"name": "Pan Integral Supán", "price": 2.25, "unit": "g", "quantity": 550, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861009944206-1-13.jpg", "features": ["Multicereal", "Alto en fibra", "Suave"]},
    {"name": "Pan Integral Supán", "price": 2.10, "unit": "g", "quantity": 550, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861009944206-1-13.jpg", "features": ["Multicereal", "Alto en fibra", "Suave"]},
    {"name": "Pan Integral Supán", "price": 2.15, "unit": "g", "quantity": 550, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861009944206-1-13.jpg", "features": ["Multicereal", "Alto en fibra", "Suave"]},

    {"name": "Galletas Saladas Amor", "price": 0.95, "unit": "g", "quantity": 150, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/05/7861091158109-1-3.jpg", "features": ["Crunchy", "Para snacks", "Ligeras"]},
    {"name": "Galletas Saladas Amor", "price": 0.85, "unit": "g", "quantity": 150, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/05/7861091158109-1-3.jpg", "features": ["Crunchy", "Para snacks", "Ligeras"]},
    {"name": "Galletas Saladas Amor", "price": 0.90, "unit": "g", "quantity": 150, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/05/7861091158109-1-3.jpg", "features": ["Crunchy", "Para snacks", "Ligeras"]},

    {"name": "Galletas Integrales Tosh", "price": 1.45, "unit": "g", "quantity": 180, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/10/7702025148448-1-2.jpg", "features": ["Multicereal", "Sin azúcar", "Dietéticas"]},
    {"name": "Galletas Integrales Tosh", "price": 1.55, "unit": "g", "quantity": 180, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/10/7702025148448-1-2.jpg", "features": ["Multicereal", "Sin azúcar", "Dietéticas"]},
    {"name": "Galletas Integrales Tosh", "price": 1.40, "unit": "g", "quantity": 180, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/10/7702025148448-1-2.jpg", "features": ["Multicereal", "Sin azúcar", "Dietéticas"]},

    {"name": "Galletas Oreo", "price": 0.65, "unit": "g", "quantity": 100, "source": "Supermaxi", "image_url": "https://mercadomi.com.ec/wp-content/uploads/2024/11/L0100034.jpg", "features": ["Chocolate", "Crema vainilla", "Infaltables"]},
    {"name": "Galletas Oreo", "price": 0.60, "unit": "g", "quantity": 100, "source": "Aki", "image_url": "https://mercadomi.com.ec/wp-content/uploads/2024/11/L0100034.jpg", "features": ["Chocolate", "Crema vainilla", "Infaltables"]},
    {"name": "Galletas Oreo", "price": 0.70, "unit": "g", "quantity": 100, "source": "Mi Comisariato", "image_url": "https://mercadomi.com.ec/wp-content/uploads/2024/11/L0100034.jpg", "features": ["Chocolate", "Crema vainilla", "Infaltables"]},

    # --- GRUPO 12: PASTAS Y FIDEOS ---
    {"name": "Fideo Corto Plumitas", "price": 0.80, "unit": "g", "quantity": 400, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/12/7861026034850-1-14.jpg", "features": ["Para ensaladas", "Trigo durum", "Don Vittorio"]},
    {"name": "Fideo Corto Plumitas", "price": 0.72, "unit": "g", "quantity": 400, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/12/7861026034850-1-14.jpg", "features": ["Para ensaladas", "Trigo durum", "Don Vittorio"]},
    {"name": "Fideo Corto Plumitas", "price": 0.75, "unit": "g", "quantity": 400, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/12/7861026034850-1-14.jpg", "features": ["Para ensaladas", "Trigo durum", "Don Vittorio"]},

    {"name": "Macarrones con Queso Kraft", "price": 1.80, "unit": "g", "quantity": 200, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/06/21000067060-1-5.png", "features": ["Original", "Cheddar", "Instantáneo"]},
    {"name": "Macarrones con Queso Kraft", "price": 1.95, "unit": "g", "quantity": 200, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/06/21000067060-1-5.png", "features": ["Original", "Cheddar", "Instantáneo"]},
    {"name": "Macarrones con Queso Kraft", "price": 1.70, "unit": "g", "quantity": 200, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2025/06/21000067060-1-5.png", "features": ["Original", "Cheddar", "Instantáneo"]},

    {"name": "Lasagna Toscana", "price": 2.50, "unit": "g", "quantity": 500, "source": "Supermaxi", "image_url": "https://statics.tipti.market/product-media/83597fd7-97d3-4df2-a0e7-f43788ec41aa.jpg", "features": ["Precocida", "Semola de trigo", "Ideal para hornear"]},
    {"name": "Lasagna Toscana", "price": 2.35, "unit": "g", "quantity": 500, "source": "Aki", "image_url": "https://statics.tipti.market/product-media/83597fd7-97d3-4df2-a0e7-f43788ec41aa.jpg", "features": ["Precocida", "Semola de trigo", "Ideal para hornear"]},
    {"name": "Lasagna Toscana", "price": 2.45, "unit": "g", "quantity": 500, "source": "Mi Comisariato", "image_url": "https://statics.tipti.market/product-media/83597fd7-97d3-4df2-a0e7-f43788ec41aa.jpg", "features": ["Precocida", "Semola de trigo", "Ideal para hornear"]},

    {"name": "Ramen Instantáneo Maggi", "price": 0.60, "unit": "g", "quantity": 80, "source": "Supermaxi", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7613287029522-1-16.jpg", "features": ["Sabor Pollo", "Listo en 3 min", "Sopa rápida"]},
    {"name": "Ramen Instantáneo Maggi", "price": 0.55, "unit": "g", "quantity": 80, "source": "Aki", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7613287029522-1-16.jpg", "features": ["Sabor Pollo", "Listo en 3 min", "Sopa rápida"]},
    {"name": "Ramen Instantáneo Maggi", "price": 0.65, "unit": "g", "quantity": 80, "source": "Mi Comisariato", "image_url": "https://www.supermaxi.com/wp-content/uploads/2024/08/7613287029522-1-16.jpg", "features": ["Sabor Pollo", "Listo en 3 min", "Sopa rápida"]},

    # --- GRUPO 13: LÁCTEOS Y ENDULZANTES ---
    {"name": "Leche en Polvo Vaquita", "price": 3.80, "unit": "g", "quantity": 380, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861001248098-1-6.jpg", "features": ["Instantánea", "Semidescremada", "Con vitaminas"]},
    {"name": "Leche en Polvo Vaquita", "price": 3.65, "unit": "g", "quantity": 380, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861001248098-1-6.jpg", "features": ["Instantánea", "Semidescremada", "Con vitaminas"]},
    {"name": "Leche en Polvo Vaquita", "price": 3.75, "unit": "g", "quantity": 380, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2024/08/7861001248098-1-6.jpg", "features": ["Instantánea", "Semidescremada", "Con vitaminas"]},

    {"name": "Margarina Girasol", "price": 1.45, "unit": "g", "quantity": 250, "source": "Supermaxi", "image_url": "https://almacenescorsa.com/wp-content/uploads/2023/07/margarina-girasol-490gr.jpg", "features": ["Vegetal", "Para pan", "Económica"]},
    {"name": "Margarina Girasol", "price": 1.35, "unit": "g", "quantity": 250, "source": "Aki", "image_url": "https://almacenescorsa.com/wp-content/uploads/2023/07/margarina-girasol-490gr.jpg", "features": ["Vegetal", "Para pan", "Económica"]},
    {"name": "Margarina Girasol", "price": 1.40, "unit": "g", "quantity": 250, "source": "Mi Comisariato", "image_url": "https://almacenescorsa.com/wp-content/uploads/2023/07/margarina-girasol-490gr.jpg", "features": ["Vegetal", "Para pan", "Económica"]},

    {"name": "Miel de Abeja Nativa", "price": 4.50, "unit": "g", "quantity": 350, "source": "Supermaxi", "image_url": "https://www.schullo.com.ec/780-large_default/miel-de-abeja-330g.jpg", "features": ["100% Pura", "Multifloral", "Envase antigoteo"]},
    {"name": "Miel de Abeja Nativa", "price": 4.65, "unit": "g", "quantity": 350, "source": "Aki", "image_url": "https://www.schullo.com.ec/780-large_default/miel-de-abeja-330g.jpg", "features": ["100% Pura", "Multifloral", "Envase antigoteo"]},
    {"name": "Miel de Abeja Nativa", "price": 4.35, "unit": "g", "quantity": 350, "source": "Mi Comisariato", "image_url": "https://www.schullo.com.ec/780-large_default/miel-de-abeja-330g.jpg", "features": ["100% Pura", "Multifloral", "Envase antigoteo"]},

    {"name": "Panela Molida El Campo", "price": 1.25, "unit": "g", "quantity": 500, "source": "Supermaxi", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/05/7861042555728-1-10.jpg", "features": ["Orgánica", "Endulzante natural", "Artesanal"]},
    {"name": "Panela Molida El Campo", "price": 1.15, "unit": "g", "quantity": 500, "source": "Aki", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/05/7861042555728-1-10.jpg", "features": ["Orgánica", "Endulzante natural", "Artesanal"]},
    {"name": "Panela Molida El Campo", "price": 1.20, "unit": "g", "quantity": 500, "source": "Mi Comisariato", "image_url": "https://supermaxi-225de.kxcdn.com/wp-content/uploads/2025/05/7861042555728-1-10.jpg", "features": ["Orgánica", "Endulzante natural", "Artesanal"]},

    {"name": "Azúcar Morena Valdez", "price": 1.40, "unit": "kg", "quantity": 1, "source": "Supermaxi", "image_url": "https://almacenescorsa.com/wp-content/uploads/2021/07/Azucar-Valdez-Morena-1kg.jpg", "features": ["Cruda", "Menos refinada", "Sabor intenso"]},
    {"name": "Azúcar Morena Valdez", "price": 1.35, "unit": "kg", "quantity": 1, "source": "Aki", "image_url": "https://almacenescorsa.com/wp-content/uploads/2021/07/Azucar-Valdez-Morena-1kg.jpg", "features": ["Cruda", "Menos refinada", "Sabor intenso"]},
    {"name": "Azúcar Morena Valdez", "price": 1.30, "unit": "kg", "quantity": 1, "source": "Mi Comisariato", "image_url": "https://almacenescorsa.com/wp-content/uploads/2021/07/Azucar-Valdez-Morena-1kg.jpg", "features": ["Cruda", "Menos refinada", "Sabor intenso"]},
]

if __name__ == "__main__":
    time.sleep(10) # Esperar a que Redis y DB inicien
    
    print(f"🚀 Enviando {len(food_items)} productos al sistema...")
    for item in food_items:
        redis_client.lpush('products_queue', json.dumps(item))
    print("✅ Proceso de ingesta terminado.")