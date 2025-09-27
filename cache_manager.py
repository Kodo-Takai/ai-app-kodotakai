#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Caché para Google Maps Places API
Herramientas para administrar el caché del sistema
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from api_cache import APICache
from config import Config

class CacheManager:
    """Gestor de caché para el sistema de recomendaciones"""
    
    def __init__(self):
        """Inicializa el gestor de caché"""
        self.cache = APICache(
            duration=Config.SEARCH_CONFIG.get('cache_duration', 3600)
        )
    
    def show_cache_stats(self):
        """Muestra estadísticas del caché"""
        print("📊 Estadísticas del Caché - Google Maps Places API")
        print("="*60)
        
        stats = self.cache.get_cache_stats()
        size_info = self.cache.get_cache_size()
        
        print(f"📁 Directorio de caché: {stats.get('cache_directory', 'N/A')}")
        print(f"⏰ Duración del caché: {stats.get('cache_duration_seconds', 0)} segundos")
        print(f"📊 Total de peticiones: {stats.get('total_requests', 0)}")
        print(f"✅ Aciertos de caché: {stats.get('cache_hits', 0)}")
        print(f"❌ Fallos de caché: {stats.get('cache_misses', 0)}")
        print(f"📈 Tasa de aciertos: {stats.get('hit_rate_percentage', 0):.1f}%")
        
        print(f"\n💾 Información de tamaño:")
        print(f"   📁 Total de archivos: {size_info.get('total_files', 0)}")
        print(f"   📊 Tamaño total: {size_info.get('total_size_mb', 0):.2f} MB")
        print(f"   📂 Tamaño en bytes: {size_info.get('total_size_bytes', 0):,}")
    
    def clean_expired_cache(self):
        """Limpia archivos de caché expirados"""
        print("🧹 Limpiando caché expirado...")
        
        deleted_count = self.cache.clear_expired_cache()
        
        if deleted_count > 0:
            print(f"✅ Eliminados {deleted_count} archivos de caché expirados")
        else:
            print("✅ No hay archivos de caché expirados")
    
    def clear_all_cache(self):
        """Limpia todo el caché"""
        print("🧹 Limpiando todo el caché...")
        
        self.cache.clear_all_cache()
        print("✅ Todo el caché ha sido limpiado")
    
    def show_cache_files(self):
        """Muestra información de archivos de caché"""
        print("📁 Archivos de Caché")
        print("="*40)
        
        cache_dir = Path(self.cache.cache_dir)
        
        if not cache_dir.exists():
            print("❌ Directorio de caché no existe")
            return
        
        files = list(cache_dir.glob("*.json"))
        
        if not files:
            print("📭 No hay archivos de caché")
            return
        
        print(f"📊 Total de archivos: {len(files)}")
        print("\n📋 Lista de archivos:")
        
        for i, file_path in enumerate(files, 1):
            file_size = file_path.stat().st_size
            file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            # Determinar tipo de archivo
            file_type = "🔍 Búsqueda" if "search_" in file_path.name else "📍 Detalles"
            
            print(f"   {i:2d}. {file_path.name}")
            print(f"       📊 Tipo: {file_type}")
            print(f"       📏 Tamaño: {file_size:,} bytes")
            print(f"       📅 Modificado: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
    
    def optimize_cache(self):
        """Optimiza el caché eliminando archivos expirados"""
        print("⚡ Optimizando caché...")
        
        # Limpiar archivos expirados
        deleted_count = self.cache.clear_expired_cache()
        
        # Mostrar estadísticas después de la optimización
        print(f"\n📊 Después de la optimización:")
        self.show_cache_stats()
        
        if deleted_count > 0:
            print(f"\n✅ Optimización completada: {deleted_count} archivos eliminados")
        else:
            print("\n✅ Caché ya está optimizado")

def main():
    """Función principal del gestor de caché"""
    print("💾 Gestor de Caché - Google Maps Places API")
    print("="*50)
    
    manager = CacheManager()
    
    while True:
        print("\n🔧 Opciones disponibles:")
        print("1. 📊 Mostrar estadísticas del caché")
        print("2. 🧹 Limpiar caché expirado")
        print("3. 🗑️ Limpiar todo el caché")
        print("4. 📁 Mostrar archivos de caché")
        print("5. ⚡ Optimizar caché")
        print("0. 🚪 Salir")
        
        try:
            choice = input("\n👉 Selecciona una opción (0-5): ").strip()
            
            if choice == "0":
                print("👋 ¡Hasta luego!")
                break
            elif choice == "1":
                manager.show_cache_stats()
            elif choice == "2":
                manager.clean_expired_cache()
            elif choice == "3":
                confirm = input("⚠️ ¿Estás seguro de limpiar todo el caché? (y/N): ").lower()
                if confirm in ['y', 'yes', 'sí', 's']:
                    manager.clear_all_cache()
                else:
                    print("❌ Operación cancelada")
            elif choice == "4":
                manager.show_cache_files()
            elif choice == "5":
                manager.optimize_cache()
            else:
                print("❌ Opción no válida")
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
