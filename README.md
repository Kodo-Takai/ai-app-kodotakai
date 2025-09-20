# 🇨🇴 IA Turística para Colombia - Sincelejo y Sucre

Sistema de Inteligencia Artificial para recomendaciones turísticas personalizadas en Colombia.

## 🚀 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd ia-turistica-colombia

# 2. Configuración automática
python quick_setup.py

# 3. ¡Listo!
```

## 🎯 Características

### 🏨 Sistema de Recomendaciones de Hoteles
- **IA Avanzada**: RandomForest Regressor para recomendaciones personalizadas
- **Datos Fake Realistas**: 20 hoteles, 10 usuarios, 50 reservas históricas
- **Filtros Inteligentes**: Presupuesto, rating, disponibilidad, estilo de viaje
- **Razones de Match**: Explica por qué cada hotel es recomendado
- **Salida JSON**: Formato estructurado para integración

### 🎯 Sistema de Actividades Turísticas
- **Recomendaciones Personalizadas**: Modelo MLPClassifier
- **Clasificación de Relevancia**: Modelo RandomForest
- **Procesamiento de Texto**: SentenceTransformer
- **Optimización Móvil**: ONNX/TensorFlow Lite
- **Funcionamiento Local**: Sin dependencia de internet

## 📱 Uso

### 🏨 Recomendaciones de Hoteles
```bash
# Generar datos fake de hoteles
python hotel_data_generator.py

# Obtener recomendaciones de hoteles
python hotel_recommendations.py
```

### 🎯 Recomendaciones de Actividades
```python
from examples.basic_usage import get_recommendations

# Obtener recomendaciones
recommendations = get_recommendations(user_id=0, limit=3)

for rec in recommendations:
    print(f"{rec['rank']}. {rec['name']} - {rec['category']}")
```

## 🤖 Modelos

### 🏨 Modelos de Hoteles
- `models/hotel_recommendations/` - Modelo RandomForest para recomendaciones de hoteles
- `data/fake_hotel_data.json` - Datos fake de hoteles, usuarios y reservas

### 🎯 Modelos de Actividades
- `models/final/` - Modelos entrenados
- `models/final/mobile/` - Modelos optimizados para móviles

## 📚 Documentación

- [Guía de Inicio](docs/quick_start_guide.md)
- [Integración Móvil](docs/mobile_integration_guide.md)
- [Resumen del Proyecto](docs/RESUMEN_FINAL.md)

## 🇨🇴 Datos Colombianos

### 🏨 Hoteles y Alojamiento
- **20 hoteles** en ciudades de Sucre (Sincelejo, Coveñas, Tolú, San Onofre, Galeras)
- **Categorías**: Económico, Medio, Lujo, Boutique, Ecológico
- **Amenities**: WiFi, Piscina, Restaurante, Spa, Estacionamiento, etc.
- **Datos realistas**: Precios, ratings, ubicaciones, contactos

### 🎯 Actividades Turísticas
- Actividades de Sincelejo y Sucre
- Procesamiento en español colombiano
- Categorías: cultural, naturaleza, gastronomía

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

**🇨🇴 ¡Listo para revolucionar el turismo en Colombia!**
