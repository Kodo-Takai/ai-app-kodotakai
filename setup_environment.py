#!/usr/bin/env python3
"""
Script de configuración inicial para el proyecto de IA turística local
Sincelejo y Sucre - Colombia
"""

import os
import subprocess
import sys
from pathlib import Path

def setup_directories():
    """Crear estructura de directorios del proyecto"""
    directories = [
        "models/pretrained",
        "models/trained", 
        "models/optimized",
        "data/raw",
        "data/processed",
        "data/sincelejo_sucre",
        "notebooks",
        "src/models",
        "src/utils",
        "mobile_models",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {directory}")

def download_initial_models():
    """Descargar modelos base para pruebas iniciales"""
    from transformers import AutoTokenizer, AutoModel
    import torch
    
    models_to_download = [
        {
            "name": "distilbert-base-uncased",
            "description": "Modelo NLP compacto para clasificación y procesamiento de texto",
            "size": "~250MB"
        },
        {
            "name": "microsoft/DialoGPT-small", 
            "description": "Modelo conversacional ligero para chat básico",
            "size": "~350MB"
        }
    ]
    
    print("\n🤖 Descargando modelos base...")
    
    for model_info in models_to_download:
        try:
            print(f"\n📥 Descargando {model_info['name']} ({model_info['size']})...")
            print(f"   Descripción: {model_info['description']}")
            
            tokenizer = AutoTokenizer.from_pretrained(model_info['name'])
            model = AutoModel.from_pretrained(model_info['name'])
            
            # Guardar en directorio local
            model_path = f"models/pretrained/{model_info['name'].replace('/', '_')}"
            model.save_pretrained(model_path)
            tokenizer.save_pretrained(model_path)
            
            print(f"✅ {model_info['name']} guardado en {model_path}")
            
        except Exception as e:
            print(f"❌ Error descargando {model_info['name']}: {e}")

def install_requirements():
    """Instalar dependencias del proyecto"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")

def create_sample_data():
    """Crear estructura de datos de ejemplo para Sincelejo y Sucre"""
    sample_data = {
        "sincelejo_activities": [
            {
                "id": 1,
                "name": "Feria de Sincelejo",
                "category": "cultural",
                "location": "Plaza Santander",
                "duration_hours": 4,
                "best_time": "evening",
                "popularity_score": 0.9
            },
            {
                "id": 2, 
                "name": "Museo de Arte",
                "category": "cultural",
                "location": "Centro Histórico",
                "duration_hours": 2,
                "best_time": "morning",
                "popularity_score": 0.7
            }
        ],
        "sucre_activities": [
            {
                "id": 3,
                "name": "Playa de Coveñas",
                "category": "naturaleza",
                "location": "Coveñas",
                "duration_hours": 6,
                "best_time": "afternoon",
                "popularity_score": 0.95
            }
        ],
        "user_profiles": [
            {
                "user_id": 1,
                "preferences": ["cultural", "gastronomía"],
                "budget_range": "medio",
                "travel_style": "relajado"
            }
        ]
    }
    
    import json
    
    # Guardar datos de ejemplo
    with open("data/sincelejo_sucre/sample_data.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Datos de ejemplo creados en data/sincelejo_sucre/sample_data.json")

def main():
    """Función principal de configuración"""
    print("🏗️  Configurando proyecto de IA turística - Sincelejo y Sucre")
    print("=" * 60)
    
    # Crear estructura de directorios
    setup_directories()
    
    # Instalar dependencias
    install_requirements()
    
    # Crear datos de ejemplo
    create_sample_data()
    
    # Descargar modelos base (opcional, comentado para evitar descargas automáticas)
    # download_initial_models()
    
    print("\n🎉 Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Ejecutar: python download_models.py")
    print("2. Revisar: data/sincelejo_sucre/sample_data.json")
    print("3. Comenzar con: notebooks/01_exploratory_analysis.ipynb")

if __name__ == "__main__":
    main()

