#!/usr/bin/env python3
"""
Script para descargar modelos compactos específicos para el proyecto turístico
Sincelejo y Sucre - Colombia
"""

import os
import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from pathlib import Path
import json

class ModelDownloader:
    def __init__(self):
        self.models_dir = Path("models/pretrained")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
    def download_distilbert(self):
        """Descargar DistilBERT para NLP y clasificación"""
        print("📥 Descargando DistilBERT...")
        try:
            from transformers import DistilBertTokenizer, DistilBertModel
            
            model_name = "distilbert-base-uncased"
            tokenizer = DistilBertTokenizer.from_pretrained(model_name)
            model = DistilBertModel.from_pretrained(model_name)
            
            # Guardar modelo
            model_path = self.models_dir / "distilbert"
            model.save_pretrained(model_path)
            tokenizer.save_pretrained(model_path)
            
            # Información del modelo
            model_info = {
                "name": "DistilBERT",
                "size_mb": 250,
                "use_cases": ["clasificación", "procesamiento_texto", "notificaciones"],
                "mobile_optimized": True,
                "quantization_ready": True
            }
            
            with open(model_path / "model_info.json", "w") as f:
                json.dump(model_info, f, indent=2)
                
            print(f"✅ DistilBERT guardado en {model_path}")
            return model_path
            
        except Exception as e:
            print(f"❌ Error descargando DistilBERT: {e}")
            return None
    
    def download_phi3_mini(self):
        """Descargar Phi-3-mini para chat conversacional"""
        print("📥 Descargando Phi-3-mini...")
        try:
            model_name = "microsoft/Phi-3-mini-4k-instruct"
            
            # Verificar si hay GPU disponible
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"🖥️  Usando dispositivo: {device}")
            
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None
            )
            
            # Guardar modelo
            model_path = self.models_dir / "phi3_mini"
            model.save_pretrained(model_path)
            tokenizer.save_pretrained(model_path)
            
            # Información del modelo
            model_info = {
                "name": "Phi-3-mini",
                "size_mb": 2500,
                "use_cases": ["chat_conversacional", "generacion_texto"],
                "mobile_optimized": False,  # Requiere optimización
                "quantization_ready": True,
                "recommended_quantization": "int8"
            }
            
            with open(model_path / "model_info.json", "w") as f:
                json.dump(model_info, f, indent=2)
                
            print(f"✅ Phi-3-mini guardado en {model_path}")
            return model_path
            
        except Exception as e:
            print(f"❌ Error descargando Phi-3-mini: {e}")
            return None
    
    def download_sentence_transformer(self):
        """Descargar modelo de embeddings para recomendaciones"""
        print("📥 Descargando Sentence Transformer...")
        try:
            from sentence_transformers import SentenceTransformer
            
            model_name = "all-MiniLM-L6-v2"
            model = SentenceTransformer(model_name)
            
            # Guardar modelo
            model_path = self.models_dir / "sentence_transformer"
            model.save(str(model_path))
            
            # Información del modelo
            model_info = {
                "name": "all-MiniLM-L6-v2",
                "size_mb": 80,
                "use_cases": ["embeddings", "recomendaciones", "similitud"],
                "mobile_optimized": True,
                "quantization_ready": True
            }
            
            with open(model_path / "model_info.json", "w") as f:
                json.dump(model_info, f, indent=2)
                
            print(f"✅ Sentence Transformer guardado en {model_path}")
            return model_path
            
        except Exception as e:
            print(f"❌ Error descargando Sentence Transformer: {e}")
            return None
    
    def create_model_registry(self):
        """Crear registro de modelos disponibles"""
        registry = {
            "recommendation_models": {
                "lightfm": {
                    "type": "collaborative_filtering",
                    "size_mb": 50,
                    "mobile_ready": True
                },
                "sentence_transformer": {
                    "type": "content_based",
                    "size_mb": 80,
                    "mobile_ready": True
                }
            },
            "nlp_models": {
                "distilbert": {
                    "type": "classification",
                    "size_mb": 250,
                    "mobile_ready": True
                },
                "phi3_mini": {
                    "type": "generative",
                    "size_mb": 2500,
                    "mobile_ready": False,
                    "requires_optimization": True
                }
            },
            "time_series_models": {
                "prophet": {
                    "type": "forecasting",
                    "size_mb": 30,
                    "mobile_ready": True
                }
            },
            "optimization_status": {
                "quantization": "pending",
                "pruning": "pending", 
                "distillation": "pending"
            }
        }
        
        with open("models/model_registry.json", "w") as f:
            json.dump(registry, f, indent=2)
        
        print("✅ Registro de modelos creado en models/model_registry.json")

def main():
    """Función principal para descargar modelos"""
    print("🤖 Descargando modelos compactos para IA turística local")
    print("=" * 60)
    
    downloader = ModelDownloader()
    
    # Descargar modelos esenciales
    models_downloaded = []
    
    # 1. DistilBERT (NLP básico)
    distilbert_path = downloader.download_distilbert()
    if distilbert_path:
        models_downloaded.append("DistilBERT")
    
    # 2. Sentence Transformer (recomendaciones)
    st_path = downloader.download_sentence_transformer()
    if st_path:
        models_downloaded.append("Sentence Transformer")
    
    # 3. Phi-3-mini (chat - opcional, grande)
    print("\n⚠️  Phi-3-mini es grande (~2.5GB). ¿Descargar? (s/n): ", end="")
    response = input().lower()
    if response == 's':
        phi3_path = downloader.download_phi3_mini()
        if phi3_path:
            models_downloaded.append("Phi-3-mini")
    
    # Crear registro de modelos
    downloader.create_model_registry()
    
    print(f"\n🎉 Descarga completada!")
    print(f"📦 Modelos descargados: {', '.join(models_downloaded)}")
    print(f"💾 Ubicación: models/pretrained/")
    
    print("\n📋 Próximos pasos:")
    print("1. Ejecutar: python optimize_models.py")
    print("2. Probar modelos: python test_models.py")
    print("3. Entrenar con datos locales: python train_local.py")

if __name__ == "__main__":
    main()

