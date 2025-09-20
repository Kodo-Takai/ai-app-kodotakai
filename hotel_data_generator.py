#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de datos fake para hoteles en Colombia
Crea datos de prueba realistas para el sistema de recomendaciones
"""

import json
import random
from datetime import datetime
from pathlib import Path

class HotelDataGenerator:
    def __init__(self):
        self.hotel_names = [
            "Hotel Plaza Sincelejo", "Hotel Sucre Real", "Hotel Costa Caribe",
            "Hotel Colonial", "Hotel Los Almendros", "Hotel San Francisco",
            "Hotel El Dorado", "Hotel La Casona", "Hotel Mar y Sol",
            "Hotel El Mirador", "Hotel Las Palmas", "Hotel Central",
            "Hotel El Refugio", "Hotel Vista Hermosa", "Hotel La Estrella"
        ]
        
        self.cities = ["Sincelejo", "Coveñas", "Tolú", "San Onofre", "Galeras"]
        
        self.amenities = [
            "WiFi gratuito", "Piscina", "Restaurante", "Gimnasio", "Spa",
            "Estacionamiento", "Aire acondicionado", "TV por cable", "Desayuno incluido",
            "Servicio de habitaciones", "Recepción 24h", "Lavandería", "Bar"
        ]
        
        self.hotel_categories = ["Económico", "Medio", "Lujo", "Boutique", "Ecológico"]
        
        self.room_types = ["Sencilla", "Doble", "Suite", "Familiar", "Ejecutiva"]

    def generate_hotel_data(self, num_hotels=20):
        """Genera datos fake de hoteles"""
        hotels = []
        
        for i in range(num_hotels):
            hotel = {
                "id": i + 1,
                "name": random.choice(self.hotel_names),
                "city": random.choice(self.cities),
                "category": random.choice(self.hotel_categories),
                "rating": round(random.uniform(3.0, 5.0), 1),
                "price_per_night": random.randint(50000, 500000),
                "amenities": random.sample(self.amenities, random.randint(3, 8)),
                "room_types": random.sample(self.room_types, random.randint(2, 4)),
                "total_rooms": random.randint(20, 150),
                "available_rooms": random.randint(5, 50),
                "location": {
                    "latitude": round(random.uniform(9.0, 10.0), 6),
                    "longitude": round(random.uniform(-75.0, -74.0), 6),
                    "address": f"Calle {random.randint(1, 100)} #{random.randint(1, 50)}-{random.randint(10, 99)}"
                },
                "contact": {
                    "phone": f"+57 {random.randint(300, 399)} {random.randint(1000000, 9999999)}",
                    "email": f"info@hotel{i+1}.com"
                },
                "description": f"Hotel {random.choice(['moderno', 'tradicional', 'elegante', 'acogedor'])} en {random.choice(self.cities)} con {random.choice(['vistas al mar', 'jardines tropicales', 'arquitectura colonial', 'diseño contemporáneo'])}",
                "created_at": datetime.now().isoformat()
            }
            hotels.append(hotel)
        
        return hotels

    def generate_user_profiles(self, num_users=10):
        """Genera perfiles de usuarios fake"""
        users = []
        
        travel_styles = ["cultural", "aventura", "relajado", "familiar", "negocios"]
        budget_ranges = ["económico", "medio", "alto"]
        
        for i in range(num_users):
            user = {
                "user_id": i + 1,
                "name": f"Usuario {i + 1}",
                "age": random.randint(18, 65),
                "travel_style": random.choice(travel_styles),
                "budget_range": random.choice(budget_ranges),
                "preferences": {
                    "amenities": random.sample(self.amenities, random.randint(2, 5)),
                    "room_type": random.choice(self.room_types),
                    "max_price": random.randint(100000, 600000),
                    "min_rating": round(random.uniform(3.0, 4.5), 1)
                },
                "location_preferences": random.sample(self.cities, random.randint(1, 3)),
                "created_at": datetime.now().isoformat()
            }
            users.append(user)
        
        return users

    def generate_booking_history(self, users, hotels, num_bookings=50):
        """Genera historial de reservas fake"""
        bookings = []
        
        for i in range(num_bookings):
            user = random.choice(users)
            hotel = random.choice(hotels)
            
            booking = {
                "booking_id": i + 1,
                "user_id": user["user_id"],
                "hotel_id": hotel["id"],
                "check_in": datetime.now().strftime("%Y-%m-%d"),
                "check_out": datetime.now().strftime("%Y-%m-%d"),
                "nights": random.randint(1, 7),
                "guests": random.randint(1, 4),
                "total_price": hotel["price_per_night"] * random.randint(1, 7),
                "rating_given": random.randint(1, 5),
                "review": random.choice([
                    "Excelente servicio y ubicación",
                    "Muy cómodo y limpio",
                    "Personal muy amable",
                    "Buen precio por la calidad",
                    "Recomendado para familias"
                ]),
                "created_at": datetime.now().isoformat()
            }
            bookings.append(booking)
        
        return bookings

    def save_fake_data(self, output_file="data/fake_hotel_data.json"):
        """Genera y guarda todos los datos fake"""
        print("🏨 Generando datos fake de hoteles...")
        
        # Crear directorio si no existe
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Generar datos
        hotels = self.generate_hotel_data(20)
        users = self.generate_user_profiles(10)
        bookings = self.generate_booking_history(users, hotels, 50)
        
        # Crear estructura completa
        fake_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_hotels": len(hotels),
                "total_users": len(users),
                "total_bookings": len(bookings),
                "description": "Datos fake generados para pruebas del sistema de recomendaciones de hoteles"
            },
            "hotels": hotels,
            "users": users,
            "bookings": bookings
        }
        
        # Guardar archivo
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fake_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Datos fake guardados en: {output_file}")
        print(f"📊 Resumen:")
        print(f"   - Hoteles: {len(hotels)}")
        print(f"   - Usuarios: {len(users)}")
        print(f"   - Reservas: {len(bookings)}")
        
        return fake_data

if __name__ == "__main__":
    generator = HotelDataGenerator()
    fake_data = generator.save_fake_data()
    
    print("\n🎯 Ejemplo de hotel generado:")
    print(json.dumps(fake_data["hotels"][0], indent=2, ensure_ascii=False))



