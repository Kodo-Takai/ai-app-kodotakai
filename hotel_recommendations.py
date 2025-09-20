#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Recomendaciones de Hoteles con IA
Utiliza datos fake para generar recomendaciones personalizadas
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from hotel_data_generator import HotelDataGenerator
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

class HotelRecommendationSystem:
    def __init__(self):
        self.data_file = "data/fake_hotel_data.json"
        self.models_dir = Path("models/hotel_recommendations")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Cargar o generar datos
        self.hotels = []
        self.users = []
        self.bookings = []
        self.load_data()
        
        # Modelos
        self.recommendation_model = None
        self.label_encoders = {}
        
    def load_data(self):
        """Carga datos fake o los genera si no existen"""
        if Path(self.data_file).exists():
            print("📂 Cargando datos existentes...")
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.hotels = data["hotels"]
                self.users = data["users"]
                self.bookings = data["bookings"]
        else:
            print("🔄 Generando datos fake...")
            generator = HotelDataGenerator()
            data = generator.save_fake_data(self.data_file)
            self.hotels = data["hotels"]
            self.users = data["users"]
            self.bookings = data["bookings"]
    
    def prepare_features(self):
        """Prepara características para el modelo de recomendaciones"""
        print("🔧 Preparando características...")
        
        # Características de hoteles
        hotel_features = []
        for hotel in self.hotels:
            features = [
                hotel["rating"],
                hotel["price_per_night"] / 100000,  # Normalizar precio
                len(hotel["amenities"]),
                hotel["total_rooms"],
                hotel["available_rooms"] / hotel["total_rooms"] if hotel["total_rooms"] > 0 else 0,
                1 if "Piscina" in hotel["amenities"] else 0,
                1 if "WiFi gratuito" in hotel["amenities"] else 0,
                1 if "Restaurante" in hotel["amenities"] else 0,
                1 if "Spa" in hotel["amenities"] else 0,
                1 if hotel["category"] == "Lujo" else 0,
                1 if hotel["category"] == "Económico" else 0
            ]
            hotel_features.append(features)
        
        # Características de usuarios
        user_features = []
        for user in self.users:
            features = [
                user["age"] / 100,  # Normalizar edad
                1 if user["travel_style"] == "cultural" else 0,
                1 if user["travel_style"] == "aventura" else 0,
                1 if user["travel_style"] == "relajado" else 0,
                1 if user["travel_style"] == "familiar" else 0,
                1 if user["travel_style"] == "negocios" else 0,
                1 if user["budget_range"] == "económico" else 0,
                1 if user["budget_range"] == "medio" else 0,
                1 if user["budget_range"] == "alto" else 0,
                user["preferences"]["min_rating"],
                user["preferences"]["max_price"] / 100000
            ]
            user_features.append(features)
        
        return np.array(hotel_features), np.array(user_features)
    
    def train_recommendation_model(self):
        """Entrena el modelo de recomendaciones"""
        print("🤖 Entrenando modelo de recomendaciones...")
        
        hotel_features, user_features = self.prepare_features()
        
        # Crear datos de entrenamiento sintéticos
        X = []
        y = []
        
        for user_idx, user in enumerate(self.users):
            for hotel_idx, hotel in enumerate(self.hotels):
                # Combinar características de usuario y hotel
                combined_features = np.concatenate([
                    user_features[user_idx],
                    hotel_features[hotel_idx]
                ])
                
                # Simular rating basado en compatibilidad
                user_pref = user_features[user_idx]
                hotel_feat = hotel_features[hotel_idx]
                
                # Calcular compatibilidad
                price_compatibility = 1 - abs(user_pref[-1] - hotel_feat[1]) / max(user_pref[-1], hotel_feat[1])
                rating_compatibility = 1 - abs(user_pref[-2] - hotel_feat[0]) / 5.0
                style_compatibility = np.dot(user_pref[1:6], [1, 1, 1, 1, 1]) / 5.0
                
                # Rating sintético basado en compatibilidad
                synthetic_rating = (price_compatibility * 0.4 + 
                                  rating_compatibility * 0.3 + 
                                  style_compatibility * 0.3) * 5
                
                # Agregar ruido
                synthetic_rating += np.random.normal(0, 0.5)
                synthetic_rating = np.clip(synthetic_rating, 1, 5)
                
                X.append(combined_features)
                y.append(synthetic_rating)
        
        X = np.array(X)
        y = np.array(y)
        
        # Entrenar modelo
        self.recommendation_model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        self.recommendation_model.fit(X, y)
        
        # Guardar modelo
        model_path = self.models_dir / "hotel_recommendation_model.pkl"
        joblib.dump(self.recommendation_model, model_path)
        print(f"✅ Modelo guardado en: {model_path}")
    
    def load_model(self):
        """Carga el modelo entrenado"""
        model_path = self.models_dir / "hotel_recommendation_model.pkl"
        if model_path.exists():
            self.recommendation_model = joblib.load(model_path)
            print("📂 Modelo cargado exitosamente")
            return True
        return False
    
    def get_hotel_recommendations(self, user_id, limit=5):
        """Obtiene recomendaciones de hoteles para un usuario"""
        if not self.recommendation_model:
            if not self.load_model():
                print("🔄 Entrenando modelo...")
                self.train_recommendation_model()
        
        user = self.users[user_id - 1]  # user_id es 1-indexed
        hotel_features, user_features = self.prepare_features()
        
        # Obtener características del usuario
        user_feat = user_features[user_id - 1]
        
        # Calcular scores para todos los hoteles
        recommendations = []
        for hotel_idx, hotel in enumerate(self.hotels):
            # Combinar características
            combined_features = np.concatenate([user_feat, hotel_features[hotel_idx]])
            
            # Predecir score
            score = self.recommendation_model.predict([combined_features])[0]
            
            # Aplicar filtros del usuario
            if (hotel["price_per_night"] <= user["preferences"]["max_price"] and
                hotel["rating"] >= user["preferences"]["min_rating"] and
                hotel["available_rooms"] > 0):
                
                recommendation = {
                    "hotel_id": hotel["id"],
                    "name": hotel["name"],
                    "city": hotel["city"],
                    "category": hotel["category"],
                    "rating": hotel["rating"],
                    "price_per_night": hotel["price_per_night"],
                    "amenities": hotel["amenities"][:5],  # Top 5 amenities
                    "score": float(score),
                    "match_reasons": self._get_match_reasons(user, hotel, score)
                }
                recommendations.append(recommendation)
        
        # Ordenar por score y tomar los mejores
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:limit]
    
    def _get_match_reasons(self, user, hotel, score):
        """Genera razones de por qué el hotel coincide con el usuario"""
        reasons = []
        
        if hotel["rating"] >= user["preferences"]["min_rating"]:
            reasons.append(f"Rating alto ({hotel['rating']}/5)")
        
        if hotel["price_per_night"] <= user["preferences"]["max_price"]:
            reasons.append("Precio dentro del presupuesto")
        
        if user["travel_style"] == "familiar" and "Piscina" in hotel["amenities"]:
            reasons.append("Ideal para familias (tiene piscina)")
        
        if user["travel_style"] == "negocios" and "WiFi gratuito" in hotel["amenities"]:
            reasons.append("Perfecto para negocios (WiFi gratuito)")
        
        if user["travel_style"] == "relajado" and "Spa" in hotel["amenities"]:
            reasons.append("Ideal para relajarse (tiene spa)")
        
        return reasons[:3]  # Máximo 3 razones
    
    def print_recommendations_json(self, user_id, limit=5):
        """Imprime las recomendaciones en formato JSON en consola"""
        recommendations = self.get_hotel_recommendations(user_id, limit)
        
        # Crear estructura de respuesta
        response = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "user_info": {
                "name": self.users[user_id - 1]["name"],
                "travel_style": self.users[user_id - 1]["travel_style"],
                "budget_range": self.users[user_id - 1]["budget_range"]
            },
            "recommendations": recommendations,
            "metadata": {
                "total_hotels_analyzed": len(self.hotels),
                "recommendations_returned": len(recommendations),
                "model_version": "1.0"
            }
        }
        
        # Imprimir JSON formateado
        print("\n" + "="*60)
        print("🏨 RECOMENDACIONES DE HOTELES - IA TURÍSTICA COLOMBIA")
        print("="*60)
        print(json.dumps(response, indent=2, ensure_ascii=False))
        print("="*60)
        
        return response

def main():
    """Función principal para demostrar el sistema"""
    print("🇨🇴 Sistema de Recomendaciones de Hoteles - IA Turística")
    print("="*60)
    
    # Inicializar sistema
    system = HotelRecommendationSystem()
    
    # Generar recomendaciones para diferentes usuarios
    for user_id in range(1, 4):  # Usuarios 1, 2, 3
        print(f"\n🎯 Generando recomendaciones para Usuario {user_id}...")
        system.print_recommendations_json(user_id, limit=3)
        print("\n" + "-"*60)

if __name__ == "__main__":
    main()



