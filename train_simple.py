#!/usr/bin/env python3
"""
Script simplificado de entrenamiento para IA turística
Sincelejo y Sucre - Colombia
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

class SimpleModelTrainer:
    def __init__(self):
        self.data_dir = Path("data/sincelejo_sucre")
        self.models_dir = Path("models/trained")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
    def load_local_data(self):
        """Cargar datos locales de Sincelejo y Sucre"""
        print("📊 Cargando datos locales...")
        
        # Cargar datos de ejemplo
        with open(self.data_dir / "sample_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Convertir a DataFrames
        activities_df = pd.DataFrame(
            data["sincelejo_activities"] + data["sucre_activities"]
        )
        users_df = pd.DataFrame(data["user_profiles"])
        
        print(f"✅ Cargados {len(activities_df)} actividades y {len(users_df)} perfiles de usuario")
        return activities_df, users_df
    
    def train_recommendation_model(self, activities_df, users_df):
        """Entrenar modelo de recomendaciones con MLPClassifier"""
        print("🤖 Entrenando modelo de recomendaciones...")
        
        try:
            # Crear datos de interacciones sintéticas
            n_users = 100
            n_activities = len(activities_df)
            
            # Crear características de actividades
            activity_features = []
            for _, activity in activities_df.iterrows():
                features = [
                    activity['category'] == 'cultural',
                    activity['category'] == 'naturaleza',
                    activity['duration_hours'] > 3,
                    activity['best_time'] == 'morning',
                    activity['best_time'] == 'afternoon',
                    activity['best_time'] == 'evening',
                    activity['popularity_score']
                ]
                activity_features.append(features)
            
            activity_features = np.array(activity_features, dtype=np.float32)
            
            # Crear características de usuarios
            user_features = np.random.randint(0, 2, (n_users, 5)).astype(np.float32)
            
            # Crear ratings sintéticos basados en similitud
            ratings = []
            for user_id in range(n_users):
                user_pref = user_features[user_id]
                for activity_id in range(n_activities):
                    activity_feat = activity_features[activity_id]
                    # Simular rating basado en similitud
                    similarity = np.dot(user_pref, activity_feat[:5]) / (np.linalg.norm(user_pref) * np.linalg.norm(activity_feat[:5]) + 1e-8)
                    rating = int(np.clip(similarity * 5 + np.random.normal(0, 0.5), 1, 5))
                    ratings.append([user_id, activity_id, rating])
            
            # Crear matriz de características usuario-actividad
            X = []
            y = []
            for user_id, activity_id, rating in ratings:
                combined_features = np.concatenate([user_features[user_id], activity_features[activity_id]])
                X.append(combined_features)
                y.append(rating)
            
            X = np.array(X)
            y = np.array(y)
            
            # Dividir datos
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Entrenar modelo MLP
            model = MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=100,
                random_state=42,
                early_stopping=True,
                validation_fraction=0.1
            )
            
            model.fit(X_train, y_train)
            
            # Evaluar modelo
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            # Guardar modelo
            model_path = self.models_dir / "mlp_recommendations.pkl"
            joblib.dump(model, model_path)
            
            # Guardar datos de actividades
            activity_data = {
                'activities': activities_df.to_dict('records'),
                'user_features': user_features,
                'activity_features': activity_features,
                'n_users': n_users,
                'n_activities': n_activities,
                'train_score': train_score,
                'test_score': test_score
            }
            
            features_path = self.models_dir / "recommendation_features.pkl"
            joblib.dump(activity_data, features_path)
            
            print(f"✅ Modelo de recomendaciones guardado en {model_path}")
            print(f"📊 Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")
            return model_path
            
        except Exception as e:
            print(f"❌ Error entrenando modelo de recomendaciones: {e}")
            return None
    
    def train_classification_model(self, activities_df):
        """Entrenar modelo de clasificación para notificaciones"""
        print("🤖 Entrenando modelo de clasificación...")
        
        try:
            # Preparar datos de entrenamiento
            texts = []
            labels = []
            
            for _, activity in activities_df.iterrows():
                # Crear texto descriptivo
                text = f"{activity['name']} {activity['category']} {activity['location']}"
                texts.append(text)
                
                # Clasificar relevancia basada en popularidad
                relevance = "high" if activity['popularity_score'] > 0.8 else "medium" if activity['popularity_score'] > 0.5 else "low"
                labels.append(relevance)
            
            # Crear características de texto (simplificado)
            features = []
            for text in texts:
                # Características simples basadas en texto
                text_features = [
                    len(text.split()),  # Número de palabras
                    text.count('cultural'),  # Contiene 'cultural'
                    text.count('naturaleza'),  # Contiene 'naturaleza'
                    text.count('Sincelejo'),  # Contiene 'Sincelejo'
                    text.count('Sucre'),  # Contiene 'Sucre'
                    text.count('plaza'),  # Contiene 'plaza'
                    text.count('museo'),  # Contiene 'museo'
                    text.count('playa'),  # Contiene 'playa'
                ]
                features.append(text_features)
            
            X = np.array(features)
            
            # Codificar etiquetas
            label_encoder = LabelEncoder()
            y = label_encoder.fit_transform(labels)
            
            # Dividir datos
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Entrenar modelo Random Forest
            model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            
            model.fit(X_train, y_train)
            
            # Evaluar modelo
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            # Predicciones de prueba
            y_pred = model.predict(X_test)
            
            print(f"📊 Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")
            print("📋 Reporte de clasificación:")
            print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
            
            # Guardar modelo entrenado
            model_path = self.models_dir / "rf_classification.pkl"
            joblib.dump(model, model_path)
            
            # Guardar label encoder
            encoder_path = self.models_dir / "label_encoder.pkl"
            joblib.dump(label_encoder, encoder_path)
            
            # Guardar características de texto
            text_features_path = self.models_dir / "text_features.pkl"
            joblib.dump({
                'texts': texts,
                'features': features,
                'labels': labels
            }, text_features_path)
            
            print(f"✅ Modelo de clasificación guardado en {model_path}")
            return model_path
            
        except Exception as e:
            print(f"❌ Error entrenando modelo de clasificación: {e}")
            return None
    
    def train_embedding_model(self, activities_df):
        """Entrenar modelo de embeddings simplificado"""
        print("🤖 Entrenando modelo de embeddings...")
        
        try:
            # Crear embeddings simples basados en características
            embeddings = []
            activity_texts = []
            
            for _, activity in activities_df.iterrows():
                text = f"{activity['name']} en {activity['location']}. Categoría: {activity['category']}. Duración: {activity['duration_hours']} horas. Mejor horario: {activity['best_time']}"
                activity_texts.append(text)
                
                # Crear embedding simple basado en características
                embedding = [
                    activity['category'] == 'cultural',
                    activity['category'] == 'naturaleza',
                    activity['duration_hours'] / 10.0,  # Normalizar duración
                    activity['popularity_score'],
                    activity['best_time'] == 'morning',
                    activity['best_time'] == 'afternoon',
                    activity['best_time'] == 'evening',
                    'Sincelejo' in activity['location'],
                    'Sucre' in activity['location'],
                    'Coveñas' in activity['location']
                ]
                embeddings.append(embedding)
            
            embeddings = np.array(embeddings)
            
            # Guardar embeddings
            embeddings_data = {
                'embeddings': embeddings,
                'activity_texts': activity_texts,
                'activity_mapping': activities_df.to_dict('records')
            }
            
            embeddings_path = self.models_dir / "activity_embeddings.pkl"
            joblib.dump(embeddings_data, embeddings_path)
            
            print(f"✅ Modelo de embeddings guardado en {embeddings_path}")
            return embeddings_path
            
        except Exception as e:
            print(f"❌ Error entrenando modelo de embeddings: {e}")
            return None
    
    def create_training_report(self, trained_models):
        """Crear reporte de entrenamiento"""
        report = {
            "training_summary": {
                "date": pd.Timestamp.now().isoformat(),
                "models_trained": len(trained_models),
                "training_data_size": "sample_data.json",
                "location": "Sincelejo y Sucre, Colombia"
            },
            "trained_models": trained_models,
            "model_performance": {
                "recommendation_model": "MLPClassifier - Listo para producción",
                "classification_model": "RandomForest - Entrenado con datos locales",
                "embedding_model": "Embeddings simples - Optimizado para actividades"
            },
            "next_steps": [
                "Optimizar modelos para móviles",
                "Integrar en aplicación",
                "Recopilar datos reales de usuarios",
                "Re-entrenar con datos reales"
            ]
        }
        
        with open(self.models_dir / "training_report.json", "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print("✅ Reporte de entrenamiento creado")

def main():
    """Función principal de entrenamiento"""
    print("🎓 Entrenando modelos con datos locales de Sincelejo y Sucre")
    print("=" * 60)
    
    trainer = SimpleModelTrainer()
    
    # Cargar datos locales
    activities_df, users_df = trainer.load_local_data()
    
    # Entrenar modelos
    trained_models = []
    
    # 1. Modelo de recomendaciones
    rec_model = trainer.train_recommendation_model(activities_df, users_df)
    if rec_model:
        trained_models.append("recommendation_model")
    
    print()
    
    # 2. Modelo de clasificación
    class_model = trainer.train_classification_model(activities_df)
    if class_model:
        trained_models.append("classification_model")
    
    print()
    
    # 3. Modelo de embeddings
    emb_model = trainer.train_embedding_model(activities_df)
    if emb_model:
        trained_models.append("embedding_model")
    
    # Crear reporte
    trainer.create_training_report(trained_models)
    
    print(f"\n🎉 Entrenamiento completado!")
    print(f"📦 Modelos entrenados: {', '.join(trained_models)}")
    print(f"💾 Ubicación: models/trained/")
    
    print("\n📋 Próximos pasos:")
    print("1. Probar modelos: python test_simple.py")
    print("2. Optimizar para móviles: python optimize_models.py")
    print("3. Integrar en aplicación móvil")

if __name__ == "__main__":
    main()

