#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Caché para Google Maps Places API
Optimiza el consumo de API almacenando resultados temporalmente
"""

import json
import time
import hashlib
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta

class APICache:
    """Sistema de caché para optimizar llamadas a Google Maps API"""
    
    def __init__(self, duration: int = 3600, cache_dir: str = "cache"):
        """
        Inicializa el sistema de caché
        
        Args:
            duration: Duración del caché en segundos (default: 1 hora)
            cache_dir: Directorio para almacenar archivos de caché
        """
        self.duration = duration
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Estadísticas
        self.hits = 0
        self.misses = 0
        self.total_requests = 0
    
    def _generate_cache_key(self, query: str, location: str = None, **kwargs) -> str:
        """
        Genera una clave única para el caché
        
        Args:
            query: Consulta de búsqueda
            location: Ubicación (opcional)
            **kwargs: Parámetros adicionales
            
        Returns:
            Clave de caché única
        """
        # Crear string único con todos los parámetros
        params = {
            'query': query,
            'location': location,
            **kwargs
        }
        
        # Ordenar parámetros para consistencia
        sorted_params = sorted(params.items())
        param_string = json.dumps(sorted_params, sort_keys=True)
        
        # Generar hash MD5
        return hashlib.md5(param_string.encode()).hexdigest()
    
    def _get_cache_file_path(self, cache_key: str, cache_type: str) -> Path:
        """
        Obtiene la ruta del archivo de caché
        
        Args:
            cache_key: Clave del caché
            cache_type: Tipo de caché (search, details)
            
        Returns:
            Ruta del archivo de caché
        """
        return self.cache_dir / f"{cache_type}_{cache_key}.json"
    
    def _is_cache_valid(self, cache_file: Path) -> bool:
        """
        Verifica si el caché es válido (no expirado)
        
        Args:
            cache_file: Archivo de caché
            
        Returns:
            True si el caché es válido
        """
        if not cache_file.exists():
            return False
        
        # Verificar tiempo de modificación
        file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
        expiry_time = file_time + timedelta(seconds=self.duration)
        
        return datetime.now() < expiry_time
    
    def get_search_results(self, query: str, location: str = None, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Obtiene resultados de búsqueda del caché
        
        Args:
            query: Consulta de búsqueda
            location: Ubicación
            **kwargs: Parámetros adicionales
            
        Returns:
            Resultados del caché o None si no existe
        """
        self.total_requests += 1
        
        cache_key = self._generate_cache_key(query, location, **kwargs)
        cache_file = self._get_cache_file_path(cache_key, "search")
        
        if self._is_cache_valid(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.hits += 1
                    print(f"💾 Caché HIT para: '{query}'")
                    return data.get('results', [])
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        self.misses += 1
        print(f"🔍 Caché MISS para: '{query}'")
        return None
    
    def set_search_results(self, query: str, results: List[Dict[str, Any]], 
                          location: str = None, **kwargs) -> None:
        """
        Almacena resultados de búsqueda en el caché
        
        Args:
            query: Consulta de búsqueda
            results: Resultados a almacenar
            location: Ubicación
            **kwargs: Parámetros adicionales
        """
        cache_key = self._generate_cache_key(query, location, **kwargs)
        cache_file = self._get_cache_file_path(cache_key, "search")
        
        cache_data = {
            'query': query,
            'location': location,
            'results': results,
            'cached_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=self.duration)).isoformat()
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Resultados almacenados en caché: {len(results)} lugares")
        except Exception as e:
            print(f"⚠️ Error guardando caché: {e}")
    
    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene detalles de un lugar del caché
        
        Args:
            place_id: ID del lugar
            
        Returns:
            Detalles del lugar o None si no existe
        """
        self.total_requests += 1
        
        cache_key = place_id
        cache_file = self._get_cache_file_path(cache_key, "details")
        
        if self._is_cache_valid(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.hits += 1
                    print(f"💾 Caché HIT para lugar: {place_id[:20]}...")
                    return data.get('details')
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        self.misses += 1
        print(f"🔍 Caché MISS para lugar: {place_id[:20]}...")
        return None
    
    def set_place_details(self, place_id: str, details: Any) -> None:
        """
        Almacena detalles de un lugar en el caché
        
        Args:
            place_id: ID del lugar
            details: Detalles del lugar (PlaceDetails object)
        """
        cache_key = place_id
        cache_file = self._get_cache_file_path(cache_key, "details")
        
        # Convertir PlaceDetails a diccionario serializable
        if hasattr(details, '__dict__'):
            details_dict = {
                'place_id': details.place_id,
                'name': details.name,
                'address': details.address,
                'rating': details.rating,
                'price_level': details.price_level,
                'types': details.types,
                'photos': details.photos,
                'phone_number': details.phone_number,
                'website': details.website,
                'opening_hours': details.opening_hours,
                'reviews': details.reviews,
                'geometry': details.geometry,
                'formatted_address': details.formatted_address,
                'business_status': details.business_status
            }
        else:
            details_dict = details
        
        cache_data = {
            'place_id': place_id,
            'details': details_dict,
            'cached_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=self.duration)).isoformat()
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Detalles almacenados en caché: {place_id[:20]}...")
        except Exception as e:
            print(f"⚠️ Error guardando caché: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del caché
        
        Returns:
            Estadísticas del caché
        """
        hit_rate = (self.hits / max(self.total_requests, 1)) * 100
        
        return {
            'total_requests': self.total_requests,
            'cache_hits': self.hits,
            'cache_misses': self.misses,
            'hit_rate_percentage': round(hit_rate, 2),
            'cache_duration_seconds': self.duration,
            'cache_directory': str(self.cache_dir)
        }
    
    def clear_expired_cache(self) -> int:
        """
        Limpia archivos de caché expirados
        
        Returns:
            Número de archivos eliminados
        """
        deleted_count = 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            if not self._is_cache_valid(cache_file):
                try:
                    cache_file.unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"⚠️ Error eliminando caché: {e}")
        
        if deleted_count > 0:
            print(f"🧹 Eliminados {deleted_count} archivos de caché expirados")
        
        return deleted_count
    
    def clear_all_cache(self) -> None:
        """Limpia todo el caché"""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            print("🧹 Todo el caché ha sido limpiado")
        except Exception as e:
            print(f"⚠️ Error limpiando caché: {e}")
    
    def get_cache_size(self) -> Dict[str, Any]:
        """
        Obtiene información del tamaño del caché
        
        Returns:
            Información del tamaño del caché
        """
        total_size = 0
        file_count = 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            total_size += cache_file.stat().st_size
            file_count += 1
        
        return {
            'total_files': file_count,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_directory': str(self.cache_dir)
        }

def main():
    """Función de demostración del sistema de caché"""
    print("💾 Sistema de Caché para Google Maps API")
    print("="*50)
    
    # Crear instancia del caché
    cache = APICache(duration=1800)  # 30 minutos
    
    # Simular algunas operaciones
    print("\n🔍 Simulando búsquedas...")
    
    # Primera búsqueda (MISS)
    results1 = cache.get_search_results("restaurantes Bogotá", "4.6097,-74.0817")
    if results1 is None:
        # Simular datos
        fake_results = [{"name": f"Restaurante {i}", "rating": 4.0 + i*0.1} for i in range(5)]
        cache.set_search_results("restaurantes Bogotá", fake_results, "4.6097,-74.0817")
    
    # Segunda búsqueda (HIT)
    results2 = cache.get_search_results("restaurantes Bogotá", "4.6097,-74.0817")
    
    # Mostrar estadísticas
    print("\n📊 Estadísticas del caché:")
    stats = cache.get_cache_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Mostrar tamaño del caché
    print("\n📁 Información del caché:")
    size_info = cache.get_cache_size()
    for key, value in size_info.items():
        print(f"   {key}: {value}")

if __name__ == "__main__":
    main()
