#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente para Google Maps Places API
Integración con el sistema de recomendaciones turísticas
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import os
from dotenv import load_dotenv
from api_cache import APICache
from config import Config

# Cargar variables de entorno desde .env
load_dotenv()

@dataclass
class PlaceDetails:
    """Estructura para almacenar detalles de un lugar"""
    place_id: str
    name: str
    address: str
    rating: float
    price_level: int
    types: List[str]
    photos: List[str]
    phone_number: str
    website: str
    opening_hours: Dict[str, Any]
    reviews: List[Dict[str, Any]]
    geometry: Dict[str, Any]
    formatted_address: str
    business_status: str

class GoogleMapsPlacesClient:
    """Cliente para interactuar con Google Maps Places API"""
    
    def __init__(self, api_key: str):
        """
        Inicializa el cliente con la API key de Google Maps
        
        Args:
            api_key: Clave de API de Google Maps Platform
        """
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.session = requests.Session()
        
        # Headers por defecto
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'IA-Turistica-Colombia/1.0'
        })
        
        # Sistema de caché
        self.cache = APICache(
            duration=Config.SEARCH_CONFIG.get('cache_duration', 3600)
        )
        
        # Contadores para optimización
        self.api_calls_made = 0
        self.cache_hits = 0
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza una petición a la API de Google Maps
        
        Args:
            endpoint: Endpoint de la API
            params: Parámetros de la petición
            
        Returns:
            Respuesta de la API como diccionario
        """
        params['key'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'OK':
                print(f"⚠️ Error en API: {data.get('status')} - {data.get('error_message', 'Sin mensaje')}")
                return {}
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en petición: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error decodificando JSON: {e}")
            return {}
    
    def text_search(self, query: str, location: str = None, radius: int = 50000, 
                   type_filter: str = None, language: str = 'es') -> List[Dict[str, Any]]:
        """
        Busca lugares usando Text Search con caché optimizado
        
        Args:
            query: Término de búsqueda
            location: Ubicación para la búsqueda (lat,lng)
            radius: Radio de búsqueda en metros
            type_filter: Tipo de lugar (restaurant, lodging, tourist_attraction, etc.)
            language: Idioma de los resultados
            
        Returns:
            Lista de lugares encontrados (máximo 8)
        """
        # Verificar caché primero
        cache_key_params = {
            'radius': radius,
            'type_filter': type_filter,
            'language': language
        }
        
        cached_results = self.cache.get_search_results(
            query, location, **cache_key_params
        )
        
        if cached_results:
            self.cache_hits += 1
            return cached_results[:Config.SEARCH_CONFIG.get('max_results_per_category', 8)]
        
        # Si no está en caché, hacer petición a la API
        params = {
            'query': query,
            'language': language
        }
        
        if location:
            params['location'] = location
            params['radius'] = radius
        
        if type_filter:
            params['type'] = type_filter
        
        print(f"🔍 Buscando: '{query}' en {location or 'todo el mundo'}")
        
        data = self._make_request('textsearch/json', params)
        results = data.get('results', [])
        
        # Limitar resultados a 8 lugares máximo
        max_results = Config.SEARCH_CONFIG.get('max_results_per_category', 8)
        results = results[:max_results]
        
        # Almacenar en caché
        self.cache.set_search_results(
            query, results, location, **cache_key_params
        )
        
        print(f"✅ Encontrados {len(results)} lugares (limitado a {max_results})")
        return results
    
    def get_place_details(self, place_id: str, fields: List[str] = None) -> Optional[PlaceDetails]:
        """
        Obtiene detalles completos de un lugar con caché optimizado
        
        Args:
            place_id: ID del lugar en Google Maps
            fields: Campos específicos a obtener
            
        Returns:
            Detalles del lugar o None si hay error
        """
        # Verificar caché primero
        cached_details = self.cache.get_place_details(place_id)
        if cached_details:
            return cached_details
        
        if fields is None:
            fields = [
                'place_id', 'name', 'formatted_address', 'rating', 'price_level',
                'types', 'photos', 'formatted_phone_number', 'website',
                'opening_hours', 'reviews', 'geometry', 'business_status'
            ]
        
        params = {
            'place_id': place_id,
            'fields': ','.join(fields),
            'language': 'es'
        }
        
        print(f"📍 Obteniendo detalles del lugar: {place_id}")
        
        data = self._make_request('details/json', params)
        result = data.get('result', {})
        
        if not result:
            return None
        
        # Procesar fotos
        photos = []
        if 'photos' in result:
            for photo in result['photos'][:5]:  # Máximo 5 fotos
                photos.append(photo.get('photo_reference', ''))
        
        # Procesar reviews
        reviews = []
        if 'reviews' in result:
            for review in result['reviews'][:3]:  # Máximo 3 reviews
                reviews.append({
                    'author_name': review.get('author_name', ''),
                    'rating': review.get('rating', 0),
                    'text': review.get('text', ''),
                    'time': review.get('time', 0)
                })
        
        # Procesar horarios
        opening_hours = {}
        if 'opening_hours' in result:
            opening_hours = {
                'open_now': result['opening_hours'].get('open_now', False),
                'weekday_text': result['opening_hours'].get('weekday_text', [])
            }
        
        place_details = PlaceDetails(
            place_id=result.get('place_id', ''),
            name=result.get('name', ''),
            address=result.get('formatted_address', ''),
            rating=result.get('rating', 0.0),
            price_level=result.get('price_level', 0),
            types=result.get('types', []),
            photos=photos,
            phone_number=result.get('formatted_phone_number', ''),
            website=result.get('website', ''),
            opening_hours=opening_hours,
            reviews=reviews,
            geometry=result.get('geometry', {}),
            formatted_address=result.get('formatted_address', ''),
            business_status=result.get('business_status', 'OPERATIONAL')
        )
        
        # Almacenar en caché
        self.cache.set_place_details(place_id, place_details)
        
        return place_details
    
    def nearby_search(self, location: str, radius: int = 5000, 
                     type_filter: str = None, keyword: str = None) -> List[Dict[str, Any]]:
        """
        Busca lugares cercanos a una ubicación
        
        Args:
            location: Coordenadas (lat,lng)
            radius: Radio de búsqueda en metros
            type_filter: Tipo de lugar
            keyword: Palabra clave adicional
            
        Returns:
            Lista de lugares cercanos
        """
        params = {
            'location': location,
            'radius': radius,
            'language': 'es'
        }
        
        if type_filter:
            params['type'] = type_filter
        
        if keyword:
            params['keyword'] = keyword
        
        print(f"🗺️ Buscando lugares cercanos a {location}")
        
        data = self._make_request('nearbysearch/json', params)
        results = data.get('results', [])
        
        print(f"✅ Encontrados {len(results)} lugares cercanos")
        return results
    
    def get_photo_url(self, photo_reference: str, max_width: int = 400, 
                     max_height: int = 400) -> str:
        """
        Obtiene URL de una foto de Google Places
        
        Args:
            photo_reference: Referencia de la foto
            max_width: Ancho máximo
            max_height: Alto máximo
            
        Returns:
            URL de la foto
        """
        if not photo_reference:
            return ""
        
        params = {
            'photo_reference': photo_reference,
            'maxwidth': max_width,
            'maxheight': max_height,
            'key': self.api_key
        }
        
        return f"{self.base_url}/photo?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    def batch_place_details(self, place_ids: List[str], 
                           delay: float = None) -> List[PlaceDetails]:
        """
        Obtiene detalles de múltiples lugares con optimización de caché
        
        Args:
            place_ids: Lista de IDs de lugares (máximo 8)
            delay: Delay entre peticiones en segundos
            
        Returns:
            Lista de detalles de lugares
        """
        if delay is None:
            delay = Config.SEARCH_CONFIG.get('delay_between_requests', 0.1)
        
        # Limitar a 8 lugares máximo
        max_places = Config.SEARCH_CONFIG.get('max_results_per_category', 8)
        place_ids = place_ids[:max_places]
        
        details = []
        batch_size = Config.SEARCH_CONFIG.get('batch_size', 3)
        
        # Procesar en lotes pequeños
        for i in range(0, len(place_ids), batch_size):
            batch = place_ids[i:i + batch_size]
            
            for j, place_id in enumerate(batch):
                print(f"📊 Procesando lugar {i+j+1}/{len(place_ids)}: {place_id[:20]}...")
                
                place_details = self.get_place_details(place_id)
                if place_details:
                    details.append(place_details)
                
                # Delay optimizado entre peticiones
                if j < len(batch) - 1:
                    time.sleep(delay)
            
            # Delay entre lotes
            if i + batch_size < len(place_ids):
                time.sleep(delay * 2)
        
        return details
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de optimización de API"""
        cache_stats = self.cache.get_cache_stats()
        
        return {
            'api_calls_made': self.api_calls_made,
            'cache_hits': self.cache_hits,
            'cache_hit_ratio': (self.cache_hits / max(self.api_calls_made + self.cache_hits, 1)) * 100,
            'cache_stats': cache_stats,
            'optimization_level': 'high' if self.cache_hits > self.api_calls_made else 'medium'
        }
    
    def clear_cache(self):
        """Limpia el caché del cliente"""
        self.cache.clear_all_cache()
        self.api_calls_made = 0
        self.cache_hits = 0
        print("🧹 Caché del cliente limpiado")

class PlacesDataExporter:
    """Exportador de datos de Google Places a JSON"""
    
    def __init__(self, client: GoogleMapsPlacesClient):
        self.client = client
    
    def export_places_to_json(self, places: List[PlaceDetails], 
                             filename: str = None) -> Dict[str, Any]:
        """
        Exporta lugares a formato JSON estructurado
        
        Args:
            places: Lista de detalles de lugares
            filename: Nombre del archivo (opcional)
            
        Returns:
            Diccionario con datos estructurados
        """
        export_data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "total_places": len(places),
                "source": "Google Maps Places API",
                "version": "1.0"
            },
            "places": []
        }
        
        for place in places:
            # Generar URLs de fotos
            photo_urls = []
            for photo_ref in place.photos:
                photo_url = self.client.get_photo_url(photo_ref)
                photo_urls.append(photo_url)
            
            place_data = {
                "id": place.place_id,
                "name": place.name,
                "address": place.address,
                "formatted_address": place.formatted_address,
                "rating": place.rating,
                "price_level": place.price_level,
                "types": place.types,
                "phone": place.phone_number,
                "website": place.website,
                "photos": photo_urls,
                "opening_hours": place.opening_hours,
                "reviews": place.reviews,
                "geometry": place.geometry,
                "business_status": place.business_status,
                "export_timestamp": datetime.now().isoformat()
            }
            
            export_data["places"].append(place_data)
        
        # Guardar archivo si se especifica
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Datos exportados a: {filename}")
        
        return export_data

def main():
    """Función de demostración"""
    print("🗺️ Cliente Google Maps Places API - IA Turística Colombia")
    print("="*60)
    
    # Obtener API key del entorno
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("❌ Error: No se encontró GOOGLE_MAPS_API_KEY en las variables de entorno")
        print("💡 Configura tu API key con: export GOOGLE_MAPS_API_KEY='tu_api_key'")
        return
    
    # Inicializar cliente
    client = GoogleMapsPlacesClient(api_key)
    
    # Ejemplo de búsqueda
    print("\n🔍 Ejemplo de búsqueda de restaurantes en Bogotá...")
    results = client.text_search(
        query="restaurantes colombianos",
        location="4.6097,-74.0817",  # Bogotá
        radius=10000,
        type_filter="restaurant"
    )
    
    if results:
        print(f"\n📋 Primeros 3 resultados:")
        for i, place in enumerate(results[:3]):
            print(f"{i+1}. {place.get('name', 'Sin nombre')} - {place.get('rating', 'N/A')}⭐")
        
        # Obtener detalles del primer lugar
        if results:
            first_place_id = results[0].get('place_id')
            if first_place_id:
                print(f"\n📍 Obteniendo detalles del primer lugar...")
                details = client.get_place_details(first_place_id)
                if details:
                    print(f"✅ Detalles obtenidos: {details.name}")
    
    print("\n✅ Demostración completada")

if __name__ == "__main__":
    main()
