#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración para el Sistema de Recomendaciones Turísticas
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """Configuración del sistema"""
    
    # Google Maps API
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'TU_API_KEY_AQUI')
    
    # Configuración de búsqueda
    SEARCH_CONFIG = {
        'default_radius': 20000,  # 20km
        'max_results_per_category': 20,
        'delay_between_requests': 0.2,  # segundos
        'language': 'es',
        'photo_max_width': 400,
        'photo_max_height': 400
    }
    
    # Ciudades de Colombia
    COLOMBIAN_CITIES = {
        'bogota': {
            'name': 'Bogotá',
            'lat': '4.6097',
            'lng': '-74.0817',
            'department': 'Cundinamarca'
        },
        'medellin': {
            'name': 'Medellín',
            'lat': '6.2442',
            'lng': '-75.5812',
            'department': 'Antioquia'
        },
        'cali': {
            'name': 'Cali',
            'lat': '3.4516',
            'lng': '-76.5320',
            'department': 'Valle del Cauca'
        },
        'cartagena': {
            'name': 'Cartagena',
            'lat': '10.3910',
            'lng': '-75.4794',
            'department': 'Bolívar'
        },
        'barranquilla': {
            'name': 'Barranquilla',
            'lat': '10.9685',
            'lng': '-74.7813',
            'department': 'Atlántico'
        },
        'bucaramanga': {
            'name': 'Bucaramanga',
            'lat': '7.1193',
            'lng': '-73.1227',
            'department': 'Santander'
        },
        'pereira': {
            'name': 'Pereira',
            'lat': '4.8133',
            'lng': '-75.6961',
            'department': 'Risaralda'
        },
        'manizales': {
            'name': 'Manizales',
            'lat': '5.0689',
            'lng': '-75.5174',
            'department': 'Caldas'
        }
    }
    
    # Tipos de lugares turísticos
    TOURISM_TYPES = {
        'restaurants': {
            'google_type': 'restaurant',
            'keywords': ['restaurante', 'comida', 'cocina'],
            'ai_weight': 0.3
        },
        'hotels': {
            'google_type': 'lodging',
            'keywords': ['hotel', 'hospedaje', 'alojamiento'],
            'ai_weight': 0.4
        },
        'attractions': {
            'google_type': 'tourist_attraction',
            'keywords': ['turístico', 'atracción', 'lugar'],
            'ai_weight': 0.3
        },
        'museums': {
            'google_type': 'museum',
            'keywords': ['museo', 'cultura', 'arte'],
            'ai_weight': 0.2
        },
        'parks': {
            'google_type': 'park',
            'keywords': ['parque', 'naturaleza', 'verde'],
            'ai_weight': 0.2
        },
        'shopping': {
            'google_type': 'shopping_mall',
            'keywords': ['compras', 'centro comercial', 'tienda'],
            'ai_weight': 0.1
        },
        'nightlife': {
            'google_type': 'night_club',
            'keywords': ['noche', 'discoteca', 'bar'],
            'ai_weight': 0.1
        }
    }
    
    # Mapeo de estilos de viaje a preferencias
    TRAVEL_STYLE_PREFERENCES = {
        'cultural': {
            'preferred_types': ['museum', 'art_gallery', 'tourist_attraction'],
            'min_rating': 4.0,
            'max_price_level': 4
        },
        'aventura': {
            'preferred_types': ['park', 'tourist_attraction', 'natural_feature'],
            'min_rating': 3.5,
            'max_price_level': 3
        },
        'relajado': {
            'preferred_types': ['spa', 'park', 'restaurant'],
            'min_rating': 4.0,
            'max_price_level': 4
        },
        'familiar': {
            'preferred_types': ['park', 'tourist_attraction', 'restaurant'],
            'min_rating': 3.5,
            'max_price_level': 3
        },
        'negocios': {
            'preferred_types': ['restaurant', 'lodging', 'shopping_mall'],
            'min_rating': 4.0,
            'max_price_level': 5
        }
    }
    
    # Configuración de exportación
    EXPORT_CONFIG = {
        'default_filename_format': 'recommendations_{city}_{user_id}_{timestamp}.json',
        'include_photos': True,
        'include_reviews': True,
        'max_photos_per_place': 5,
        'max_reviews_per_place': 3
    }
    
    @classmethod
    def get_city_info(cls, city_key: str) -> Dict[str, Any]:
        """Obtiene información de una ciudad"""
        return cls.COLOMBIAN_CITIES.get(city_key, {})
    
    @classmethod
    def get_tourism_type_info(cls, type_key: str) -> Dict[str, Any]:
        """Obtiene información de un tipo de lugar turístico"""
        return cls.TOURISM_TYPES.get(type_key, {})
    
    @classmethod
    def get_travel_style_preferences(cls, style: str) -> Dict[str, Any]:
        """Obtiene preferencias para un estilo de viaje"""
        return cls.TRAVEL_STYLE_PREFERENCES.get(style, {})
    
    @classmethod
    def validate_api_key(cls) -> bool:
        """Valida que la API key esté configurada"""
        return bool(cls.GOOGLE_MAPS_API_KEY)
