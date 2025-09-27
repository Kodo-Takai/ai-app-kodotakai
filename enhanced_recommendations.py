#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Recomendaciones Mejorado con Google Maps Places API
Integra IA con datos reales de Google Maps para recomendaciones turísticas
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

from google_maps_client import GoogleMapsPlacesClient, PlacesDataExporter, PlaceDetails
from hotel_recommendations import HotelRecommendationSystem

class EnhancedTourismRecommendationSystem:
    """Sistema de recomendaciones turísticas mejorado con Google Maps"""
    
    def __init__(self, google_maps_api_key: str):
        """
        Inicializa el sistema mejorado
        
        Args:
            google_maps_api_key: Clave de API de Google Maps
        """
        self.google_maps_client = GoogleMapsPlacesClient(google_maps_api_key)
        self.data_exporter = PlacesDataExporter(self.google_maps_client)
        self.hotel_system = HotelRecommendationSystem()
        
        # Configuración de tipos de lugares turísticos
        self.tourism_types = {
            'restaurants': 'restaurant',
            'hotels': 'lodging', 
            'attractions': 'tourist_attraction',
            'museums': 'museum',
            'parks': 'park',
            'shopping': 'shopping_mall',
            'nightlife': 'night_club'
        }
        
        # Ciudades principales de Colombia
        self.colombian_cities = {
            'bogota': {'lat': '4.6097', 'lng': '-74.0817', 'name': 'Bogotá'},
            'medellin': {'lat': '6.2442', 'lng': '-75.5812', 'name': 'Medellín'},
            'cali': {'lat': '3.4516', 'lng': '-76.5320', 'name': 'Cali'},
            'cartagena': {'lat': '10.3910', 'lng': '-75.4794', 'name': 'Cartagena'},
            'barranquilla': {'lat': '10.9685', 'lng': '-74.7813', 'name': 'Barranquilla'},
            'bucaramanga': {'lat': '7.1193', 'lng': '-73.1227', 'name': 'Bucaramanga'}
        }
    
    def search_tourism_places(self, city: str, place_type: str, 
                            query: str = None, limit: int = 8) -> List[Dict[str, Any]]:
        """
        Busca lugares turísticos en una ciudad específica (optimizado a 8 lugares máximo)
        
        Args:
            city: Nombre de la ciudad
            place_type: Tipo de lugar (restaurants, hotels, attractions, etc.)
            query: Consulta específica (opcional)
            limit: Número máximo de resultados (máximo 8)
            
        Returns:
            Lista de lugares encontrados
        """
        if city not in self.colombian_cities:
            print(f"❌ Ciudad '{city}' no reconocida")
            return []
        
        city_info = self.colombian_cities[city]
        location = f"{city_info['lat']},{city_info['lng']}"
        
        # Determinar tipo de lugar para Google Places
        google_type = self.tourism_types.get(place_type, 'tourist_attraction')
        
        # Construir consulta
        if not query:
            if place_type == 'restaurants':
                query = f"restaurantes {city_info['name']}"
            elif place_type == 'hotels':
                query = f"hoteles {city_info['name']}"
            elif place_type == 'attractions':
                query = f"lugares turísticos {city_info['name']}"
            else:
                query = f"{place_type} {city_info['name']}"
        
        print(f"🔍 Buscando {place_type} en {city_info['name']}...")
        
        # Realizar búsqueda optimizada
        results = self.google_maps_client.text_search(
            query=query,
            location=location,
            radius=20000,  # 20km
            type_filter=google_type
        )
        
        # Ya está limitado a 8 en el cliente
        return results
    
    def get_enhanced_place_details(self, place_ids: List[str]) -> List[PlaceDetails]:
        """
        Obtiene detalles completos de múltiples lugares (optimizado)
        
        Args:
            place_ids: Lista de IDs de lugares (máximo 8)
            
        Returns:
            Lista de detalles de lugares
        """
        print(f"📊 Obteniendo detalles de {len(place_ids)} lugares (optimizado)...")
        return self.google_maps_client.batch_place_details(place_ids)
    
    def generate_ai_recommendations(self, user_preferences: Dict[str, Any], 
                                  city: str = 'bogota') -> Dict[str, Any]:
        """
        Genera recomendaciones usando IA + Google Maps
        
        Args:
            user_preferences: Preferencias del usuario
            city: Ciudad para buscar
            limit: Número de recomendaciones por categoría
            
        Returns:
            Recomendaciones estructuradas
        """
        print(f"🤖 Generando recomendaciones IA para {city}...")
        
        recommendations = {
            'city': self.colombian_cities[city]['name'],
            'generated_at': datetime.now().isoformat(),
            'categories': {}
        }
        
        # Buscar en diferentes categorías
        categories_to_search = ['restaurants', 'attractions', 'hotels']
        
        for category in categories_to_search:
            print(f"\n🔍 Buscando {category}...")
            
            # Buscar lugares (limitado a 8)
            places = self.search_tourism_places(
                city=city,
                place_type=category,
                limit=8
            )
            
            if not places:
                continue
            
            # Obtener IDs de lugares
            place_ids = [place.get('place_id') for place in places if place.get('place_id')]
            
            if not place_ids:
                continue
            
            # Obtener detalles
            place_details = self.get_enhanced_place_details(place_ids)
            
            # Filtrar y rankear por IA
            filtered_places = self._filter_by_ai_preferences(place_details, user_preferences)
            
            recommendations['categories'][category] = {
                'total_found': len(places),
                'ai_filtered': len(filtered_places),
                'places': filtered_places[:5]  # Top 5
            }
        
        return recommendations
    
    def _filter_by_ai_preferences(self, places: List[PlaceDetails], 
                                 user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filtra lugares usando preferencias del usuario y IA
        
        Args:
            places: Lista de lugares
            user_preferences: Preferencias del usuario
            
        Returns:
            Lugares filtrados y rankeados
        """
        filtered_places = []
        
        for place in places:
            # Calcular score de compatibilidad
            compatibility_score = self._calculate_compatibility_score(place, user_preferences)
            
            if compatibility_score > 0.3:  # Umbral mínimo
                place_data = {
                    'name': place.name,
                    'address': place.address,
                    'rating': place.rating,
                    'price_level': place.price_level,
                    'types': place.types,
                    'photos': place.photos,
                    'phone': place.phone_number,
                    'website': place.website,
                    'opening_hours': place.opening_hours,
                    'reviews': place.reviews,
                    'geometry': place.geometry,
                    'business_status': place.business_status,
                    'ai_score': compatibility_score,
                    'match_reasons': self._get_ai_match_reasons(place, user_preferences)
                }
                filtered_places.append(place_data)
        
        # Ordenar por score de IA
        filtered_places.sort(key=lambda x: x['ai_score'], reverse=True)
        return filtered_places
    
    def _calculate_compatibility_score(self, place: PlaceDetails, 
                                     user_preferences: Dict[str, Any]) -> float:
        """
        Calcula score de compatibilidad usando IA
        
        Args:
            place: Detalles del lugar
            user_preferences: Preferencias del usuario
            
        Returns:
            Score de compatibilidad (0-1)
        """
        score = 0.0
        
        # Score por rating
        if place.rating >= user_preferences.get('min_rating', 3.0):
            rating_score = (place.rating - user_preferences.get('min_rating', 3.0)) / 2.0
            score += min(rating_score, 0.4)  # Máximo 40% del score
        
        # Score por precio
        max_price_level = user_preferences.get('max_price_level', 3)
        if place.price_level <= max_price_level:
            price_score = (max_price_level - place.price_level) / max_price_level
            score += price_score * 0.3  # 30% del score
        
        # Score por tipo de lugar
        preferred_types = user_preferences.get('preferred_types', [])
        if any(tipo in place.types for tipo in preferred_types):
            score += 0.2  # 20% del score
        
        # Score por reviews (calidad)
        if place.reviews and len(place.reviews) >= 3:
            avg_review_rating = sum(r.get('rating', 0) for r in place.reviews) / len(place.reviews)
            if avg_review_rating >= 4.0:
                score += 0.1  # 10% del score
        
        return min(score, 1.0)
    
    def _get_ai_match_reasons(self, place: PlaceDetails, 
                            user_preferences: Dict[str, Any]) -> List[str]:
        """
        Genera razones de por qué el lugar coincide con el usuario
        
        Args:
            place: Detalles del lugar
            user_preferences: Preferencias del usuario
            
        Returns:
            Lista de razones
        """
        reasons = []
        
        if place.rating >= user_preferences.get('min_rating', 3.0):
            reasons.append(f"Rating alto ({place.rating}/5)")
        
        if place.price_level <= user_preferences.get('max_price_level', 3):
            price_labels = ['Gratis', 'Económico', 'Moderado', 'Caro', 'Muy caro']
            reasons.append(f"Precio {price_labels[place.price_level] if place.price_level < len(price_labels) else 'Accesible'}")
        
        if place.reviews and len(place.reviews) >= 3:
            reasons.append(f"Bien valorado ({len(place.reviews)} reseñas)")
        
        if place.business_status == 'OPERATIONAL':
            reasons.append("Actualmente abierto")
        
        return reasons[:3]
    
    def export_recommendations_to_json(self, recommendations: Dict[str, Any], 
                                     filename: str = None) -> Dict[str, Any]:
        """
        Exporta recomendaciones a JSON con datos de Google Maps
        
        Args:
            recommendations: Recomendaciones generadas
            filename: Nombre del archivo
            
        Returns:
            Datos exportados estructurados
        """
        export_data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "source": "IA Turística Colombia + Google Maps Places API",
                "version": "2.0",
                "total_categories": len(recommendations.get('categories', {})),
                "total_places": sum(
                    len(cat.get('places', [])) 
                    for cat in recommendations.get('categories', {}).values()
                )
            },
            "recommendations": recommendations
        }
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Recomendaciones exportadas a: {filename}")
        
        return export_data
    
    def get_user_recommendations(self, user_id: int, city: str = 'bogota') -> Dict[str, Any]:
        """
        Obtiene recomendaciones personalizadas para un usuario
        
        Args:
            user_id: ID del usuario
            city: Ciudad para buscar
            
        Returns:
            Recomendaciones personalizadas
        """
        # Obtener preferencias del usuario del sistema de hoteles
        if user_id <= len(self.hotel_system.users):
            user = self.hotel_system.users[user_id - 1]
            
            # Convertir preferencias a formato compatible
            user_preferences = {
                'min_rating': user['preferences']['min_rating'],
                'max_price_level': 3 if user['budget_range'] == 'económico' else 
                                 4 if user['budget_range'] == 'medio' else 5,
                'travel_style': user['travel_style'],
                'preferred_types': self._get_preferred_types_by_style(user['travel_style'])
            }
            
            # Generar recomendaciones
            recommendations = self.generate_ai_recommendations(user_preferences, city)
            
            # Agregar información del usuario
            recommendations['user_info'] = {
                'user_id': user_id,
                'name': user['name'],
                'travel_style': user['travel_style'],
                'budget_range': user['budget_range']
            }
            
            return recommendations
        
        return {}
    
    def _get_preferred_types_by_style(self, travel_style: str) -> List[str]:
        """
        Obtiene tipos de lugares preferidos según el estilo de viaje
        
        Args:
            travel_style: Estilo de viaje del usuario
            
        Returns:
            Lista de tipos preferidos
        """
        style_mapping = {
            'cultural': ['museum', 'art_gallery', 'tourist_attraction'],
            'aventura': ['park', 'tourist_attraction', 'natural_feature'],
            'relajado': ['spa', 'park', 'restaurant'],
            'familiar': ['park', 'tourist_attraction', 'restaurant'],
            'negocios': ['restaurant', 'lodging', 'shopping_mall']
        }
        
        return style_mapping.get(travel_style, ['tourist_attraction', 'restaurant'])

def main():
    """Función principal de demostración"""
    print("🇨🇴 Sistema de Recomendaciones Turísticas Mejorado")
    print("🤖 IA + Google Maps Places API")
    print("="*60)
    
    # Verificar API key
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("❌ Error: No se encontró GOOGLE_MAPS_API_KEY")
        print("💡 Configura tu API key con: export GOOGLE_MAPS_API_KEY='tu_api_key'")
        return
    
    # Inicializar sistema
    system = EnhancedTourismRecommendationSystem(api_key)
    
    # Ejemplo de recomendaciones para diferentes usuarios
    cities = ['bogota', 'medellin', 'cartagena']
    
    for city in cities:
        print(f"\n🏙️ Generando recomendaciones para {city.upper()}...")
        
        # Generar para usuario 1 (cultural)
        recommendations = system.get_user_recommendations(1, city)
        
        if recommendations:
            # Exportar a JSON
            filename = f"recommendations_{city}_user1.json"
            system.export_recommendations_to_json(recommendations, filename)
            
            print(f"✅ Recomendaciones generadas para {city}")
            print(f"📊 Categorías: {list(recommendations.get('categories', {}).keys())}")
    
    print("\n✅ Sistema de recomendaciones completado")
    print("📁 Revisa los archivos JSON generados para ver los resultados")

if __name__ == "__main__":
    main()
