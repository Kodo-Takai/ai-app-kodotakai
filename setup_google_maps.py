#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Configuración para Google Maps Places API
Configura el entorno y verifica la integración
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("\n📦 Instalando dependencias...")
    
    try:
        # Instalar dependencias básicas
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "requests", "googlemaps", "python-dotenv"
        ])
        
        print("✅ Dependencias básicas instaladas")
        
        # Instalar dependencias completas si existe requirements.txt
        if Path("requirements.txt").exists():
            print("📋 Instalando dependencias completas...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("✅ Todas las dependencias instaladas")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def check_api_key():
    """Verifica la configuración de la API key"""
    print("\n🔑 Verificando API Key de Google Maps...")
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_MAPS_API_KEY no configurada")
        print("\n💡 Para configurar tu API key:")
        print("   Windows: set GOOGLE_MAPS_API_KEY=tu_api_key")
        print("   Linux/Mac: export GOOGLE_MAPS_API_KEY=tu_api_key")
        print("\n🔗 Obtén tu API key en: https://console.cloud.google.com/")
        return False
    
    if len(api_key) < 20:
        print("⚠️ API Key parece muy corta, verifica que sea correcta")
        return False
    
    print("✅ API Key configurada")
    return True

def test_google_maps_connection():
    """Prueba la conexión con Google Maps API"""
    print("\n🌐 Probando conexión con Google Maps API...")
    
    try:
        from google_maps_client import GoogleMapsPlacesClient
        
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        client = GoogleMapsPlacesClient(api_key)
        
        # Prueba simple de búsqueda
        results = client.text_search(
            query="Bogotá Colombia",
            location="4.6097,-74.0817",
            radius=1000
        )
        
        if results:
            print("✅ Conexión exitosa con Google Maps API")
            print(f"   📍 Encontrados {len(results)} lugares en la prueba")
            return True
        else:
            print("⚠️ Conexión exitosa pero sin resultados")
            return True
            
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error probando conexión: {e}")
        return False

def create_demo_files():
    """Crea archivos de demostración"""
    print("\n📁 Creando archivos de demostración...")
    
    # Crear directorio de ejemplos si no existe
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Crear archivo de configuración de ejemplo
    config_example = """# Configuración de ejemplo para Google Maps API
# Copia este archivo como .env y configura tus valores

GOOGLE_MAPS_API_KEY=tu_api_key_aqui
DEFAULT_CITY=bogota
DEFAULT_LANGUAGE=es
"""
    
    with open("env_example.txt", "w", encoding="utf-8") as f:
        f.write(config_example)
    
    print("✅ Archivos de demostración creados")
    return True

def run_basic_demo():
    """Ejecuta una demostración básica"""
    print("\n🚀 Ejecutando demostración básica...")
    
    try:
        # Importar y ejecutar demo
        from examples.google_maps_demo import demo_basic_search
        
        print("🔍 Ejecutando búsqueda básica...")
        demo_basic_search()
        
        print("✅ Demostración básica completada")
        return True
        
    except Exception as e:
        print(f"❌ Error en demostración: {e}")
        return False

def main():
    """Función principal de configuración"""
    print("🇨🇴 Configuración del Sistema de Recomendaciones Turísticas")
    print("🗺️ Integración con Google Maps Places API")
    print("="*60)
    
    # Verificaciones
    checks = [
        ("Versión de Python", check_python_version),
        ("Instalación de dependencias", install_dependencies),
        ("Configuración de API Key", check_api_key),
        ("Conexión con Google Maps", test_google_maps_connection),
        ("Archivos de demostración", create_demo_files)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
                print(f"❌ {check_name} falló")
            else:
                print(f"✅ {check_name} exitoso")
        except Exception as e:
            print(f"❌ Error en {check_name}: {e}")
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("🎉 ¡Configuración completada exitosamente!")
        print("\n📋 Próximos pasos:")
        print("1. Ejecuta: python examples/google_maps_demo.py")
        print("2. Revisa la documentación en docs/google_maps_integration_guide.md")
        print("3. Personaliza las configuraciones en config.py")
        
        # Preguntar si ejecutar demo
        try:
            response = input("\n¿Ejecutar demostración básica? (y/n): ").lower()
            if response in ['y', 'yes', 'sí', 's']:
                run_basic_demo()
        except KeyboardInterrupt:
            print("\n👋 Configuración completada")
    else:
        print("❌ Configuración incompleta")
        print("\n🔧 Revisa los errores anteriores y vuelve a ejecutar")
        print("💡 Para ayuda: python setup_google_maps.py --help")

if __name__ == "__main__":
    main()
