#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de uso de la IA Turística para Colombia
Demuestra cómo usar los modelos entrenados
"""

import joblib
import numpy as np
from pathlib import Path

def load_models():
    """Carga los modelos entrenados"""
    models_dir = Path(__file__).parent.parent / "models" / "final"
    
    # Cargar modelo de recomendaciones
    rec_model = joblib.load(models_dir / "mlp_recommendations.pkl")
    rec_features = joblib.load(models_dir / "recommendation_features.pkl")
    
    return rec_model, rec_features

def get_recommendations(user_id=0, limit=3):
    """Obtiene recomendaciones para un usuario"""
    model, features = load_models()
    
    user_features = features['user_features'][user_id]
    activities = features['activities']
    activity_features = features['activity_features']
    
    # Generar recomendaciones
    predictions = []
    for activity_id in range(len(activities)):
        combined_features = np.concatenate([user_features, activity_features[activity_id]])
        pred = model.predict([combined_features])[0]
        predictions.append(pred)
    
    # Obtener top recomendaciones
    predictions = np.array(predictions)
    top_indices = np.argsort(predictions)[-limit:][::-1]
    
    recommendations = []
    for i, idx in enumerate(top_indices):
        activity = activities[idx]
        score = predictions[idx]
        recommendations.append({
            "rank": i + 1,
            "name": activity['name'],
            "category": activity['category'],
            "score": float(score)
        })
    
    return recommendations

if __name__ == "__main__":
    print("🇨🇴 IA Turística para Colombia - Ejemplo de Uso")
    print("=" * 50)
    
    recommendations = get_recommendations(user_id=0, limit=3)
    
    print("🎯 Recomendaciones personalizadas:")
    for rec in recommendations:
        print(f"   {rec['rank']}. {rec['name']} - {rec['category']} (Score: {rec['score']:.1f})")
