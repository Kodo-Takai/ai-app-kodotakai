# 📱 Guía de Integración Móvil - IA Turística Sincelejo y Sucre

## 🎯 Resumen del Proyecto

Este proyecto implementa un sistema de IA local para una aplicación turística de Sincelejo y Sucre, Colombia, que funciona completamente offline en dispositivos móviles.

## 🏗️ Arquitectura de Modelos

### Modelos por Requerimiento Funcional

| RF | Funcionalidad | Modelo | Tamaño | Plataforma |
|---|---|---|---|---|
| **RF-04** | Recomendaciones personalizadas | LightFM + AutoMLP | 50MB | Android/iOS |
| **RF-05** | Planificación temporal | Prophet + LSTM | 30MB | Cross-platform |
| **RF-10** | Notificaciones personalizadas | DistilBERT | 63MB | ONNX Runtime |
| **RF-18** | Optimización de rutas | GraphSAGE + A* | 20MB | Native |
| **RF-19** | Segmentación de usuario | K-Means + Autoencoder | 15MB | TensorFlow Lite |
| **RF-20** | Resúmenes automáticos | DistilBART | 300MB | ONNX Runtime |
| **RF-28** | Chat conversacional | Phi-3-mini (4B) | 625MB | ONNX Runtime |

## 🚀 Pipeline de Implementación

### 1. Configuración Inicial
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar entorno
python setup_environment.py
```

### 2. Descarga de Modelos
```bash
# Descargar modelos base
python download_models.py
```

### 3. Entrenamiento Local
```bash
# Entrenar con datos de Sincelejo y Sucre
python train_local.py
```

### 4. Optimización para Móviles
```bash
# Optimizar modelos para dispositivos móviles
python optimize_models.py
```

## 📊 Estrategias de Optimización

### Cuantización
- **DistilBERT**: 250MB → 63MB (75% reducción)
- **Phi-3-mini**: 2.5GB → 625MB (75% reducción)
- **Técnica**: INT8 quantization con TensorFlow Lite y ONNX Runtime

### Pruning
- Eliminación de conexiones menos importantes
- Reducción de parámetros sin pérdida significativa de precisión
- Aplicado a modelos de recomendación y clasificación

### Knowledge Distillation
- Modelos grandes (maestro) → Modelos pequeños (estudiante)
- Mantiene rendimiento con menor tamaño
- Especialmente útil para modelos de chat

## 📱 Integración Móvil

### Android (TensorFlow Lite)
```kotlin
// Ejemplo de integración en Android
class RecommendationEngine {
    private var interpreter: Interpreter? = null
    
    fun loadModel(context: Context) {
        val modelFile = loadModelFile(context, "recommendation_model.tflite")
        interpreter = Interpreter(modelFile)
    }
    
    fun getRecommendations(userFeatures: FloatArray): List<Activity> {
        val input = arrayOf(userFeatures)
        val output = Array(1) { FloatArray(10) }
        interpreter?.run(input, output)
        return processOutput(output[0])
    }
}
```

### iOS (ONNX Runtime)
```swift
// Ejemplo de integración en iOS
class ChatBot {
    private var session: ORTSession?
    
    func loadModel() {
        guard let modelPath = Bundle.main.path(forResource: "phi3_mini_mobile", ofType: "onnx") else { return }
        session = try? ORTSession(modelPath: modelPath)
    }
    
    func generateResponse(prompt: String) -> String {
        let input = prepareInput(prompt)
        let output = try? session?.run(withInputs: input, outputNames: ["logits"])
        return processOutput(output)
    }
}
```

## 🎯 Modelos Recomendados para Empezar

### 1. DistilBERT (250MB → 63MB)
- **Uso**: Clasificación de notificaciones, procesamiento de texto
- **Descarga**: `python download_models.py`
- **Optimización**: Cuantización INT8 automática

### 2. LightFM (50MB)
- **Uso**: Sistema de recomendaciones
- **Ventaja**: Ligero y eficiente
- **Entrenamiento**: Con datos locales de Sincelejo y Sucre

### 3. Sentence Transformer (80MB)
- **Uso**: Embeddings para similitud de actividades
- **Aplicación**: Búsqueda semántica de actividades turísticas

### 4. Phi-3-mini (2.5GB → 625MB)
- **Uso**: Chat conversacional
- **Optimización**: Cuantización + ONNX
- **Recomendación**: Usar solo si es esencial

## 📈 Métricas de Rendimiento

### Tiempo de Inferencia
- **DistilBERT**: ~50ms en smartphone promedio
- **LightFM**: ~10ms para recomendaciones
- **Phi-3-mini**: ~200ms para respuestas de chat

### Uso de Memoria
- **RAM**: 100-200MB total
- **Almacenamiento**: 1-2GB para todos los modelos
- **Batería**: Impacto mínimo con optimizaciones

## 🔧 Herramientas de Desarrollo

### Frameworks
- **TensorFlow Lite**: Para Android
- **ONNX Runtime Mobile**: Para iOS y cross-platform
- **Core ML**: Alternativa para iOS

### Librerías Python
- **Optimum**: Optimización de modelos Hugging Face
- **Neural Compressor**: Cuantización avanzada
- **LightFM**: Sistemas de recomendación

## 📋 Checklist de Implementación

### Fase 1: Preparación
- [ ] Instalar dependencias
- [ ] Configurar entorno
- [ ] Descargar modelos base

### Fase 2: Entrenamiento
- [ ] Recopilar datos locales
- [ ] Entrenar modelos
- [ ] Validar rendimiento

### Fase 3: Optimización
- [ ] Aplicar cuantización
- [ ] Optimizar para móviles
- [ ] Probar en dispositivos reales

### Fase 4: Integración
- [ ] Integrar en app Android
- [ ] Integrar en app iOS
- [ ] Pruebas de rendimiento

## 🎯 Próximos Pasos Recomendados

1. **Empezar con DistilBERT** (más pequeño, fácil de probar)
2. **Implementar LightFM** para recomendaciones básicas
3. **Probar en dispositivo móvil** antes de modelos más grandes
4. **Recopilar datos reales** de usuarios de Sincelejo y Sucre
5. **Iterar y mejorar** basado en feedback real

## 📞 Soporte y Recursos

- **Documentación TensorFlow Lite**: https://www.tensorflow.org/lite
- **ONNX Runtime Mobile**: https://onnxruntime.ai/docs/build/eps.html
- **Hugging Face Models**: https://huggingface.co/models
- **LightFM Documentation**: https://github.com/lyst/lightfm

---

*Desarrollado para el proyecto turístico de Sincelejo y Sucre, Colombia*

