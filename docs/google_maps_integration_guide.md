# Guía de Integración con Google Maps Places API

## 🗺️ Descripción General

Esta guía explica cómo integrar el sistema de recomendaciones turísticas con la API de Google Maps Places para obtener datos reales de lugares y mejorar las recomendaciones de IA.

## 🚀 Características Principales

- **Búsqueda de Lugares**: Integración con Google Places API para búsquedas en tiempo real
- **Datos Detallados**: Obtención de información completa de lugares (rating, fotos, reviews, etc.)
- **IA Mejorada**: Sistema de recomendaciones que combina IA con datos reales de Google Maps
- **Exportación JSON**: Generación de archivos JSON estructurados para frontend
- **Múltiples Ciudades**: Soporte para las principales ciudades de Colombia

## 📋 Requisitos Previos

### 1. API Key de Google Maps Platform

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita las siguientes APIs:
   - **Places API**
   - **Maps JavaScript API**
   - **Geocoding API**
4. Crea credenciales (API Key)
5. Configura restricciones de API key (recomendado)

### 2. Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configuración de Variables de Entorno

```bash
# Windows
set GOOGLE_MAPS_API_KEY=tu_api_key_aqui

# Linux/Mac
export GOOGLE_MAPS_API_KEY=tu_api_key_aqui
```

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Usuario       │    │  Sistema IA      │    │  Google Maps    │
│   (Frontend)    │◄──►│  Recomendaciones │◄──►│  Places API     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   JSON Export   │    │  Filtrado IA     │    │  Datos Reales   │
│   (Resultados)  │    │  + Ranking       │    │  de Lugares     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 Componentes Principales

### 1. GoogleMapsPlacesClient

Cliente principal para interactuar con Google Places API:

```python
from google_maps_client import GoogleMapsPlacesClient

# Inicializar cliente
client = GoogleMapsPlacesClient(api_key="tu_api_key")

# Buscar lugares
results = client.text_search(
    query="restaurantes colombianos",
    location="4.6097,-74.0817",  # Bogotá
    radius=10000
)

# Obtener detalles
details = client.get_place_details(place_id="ChIJ...")
```

### 2. EnhancedTourismRecommendationSystem

Sistema mejorado que combina IA con Google Maps:

```python
from enhanced_recommendations import EnhancedTourismRecommendationSystem

# Inicializar sistema
system = EnhancedTourismRecommendationSystem(api_key="tu_api_key")

# Generar recomendaciones
recommendations = system.get_user_recommendations(
    user_id=1,
    city='bogota'
)

# Exportar a JSON
system.export_recommendations_to_json(
    recommendations, 
    "recomendaciones.json"
)
```

## 📊 Tipos de Datos Soportados

### Lugares Turísticos
- **Restaurantes**: Comida local e internacional
- **Hoteles**: Alojamiento de diferentes categorías
- **Atracciones**: Lugares turísticos y culturales
- **Museos**: Centros culturales y artísticos
- **Parques**: Espacios naturales y recreativos
- **Compras**: Centros comerciales y tiendas
- **Vida Nocturna**: Bares, discotecas y entretenimiento

### Ciudades Soportadas
- Bogotá
- Medellín
- Cali
- Cartagena
- Barranquilla
- Bucaramanga
- Pereira
- Manizales

## 🎯 Ejemplos de Uso

### Búsqueda Básica

```python
# Buscar restaurantes en Bogotá
restaurants = system.search_tourism_places(
    city='bogota',
    place_type='restaurants',
    limit=10
)
```

### Recomendaciones Personalizadas

```python
# Preferencias del usuario
user_preferences = {
    'min_rating': 4.0,
    'max_price_level': 3,
    'travel_style': 'cultural',
    'preferred_types': ['museum', 'art_gallery']
}

# Generar recomendaciones
recommendations = system.generate_ai_recommendations(
    user_preferences=user_preferences,
    city='cartagena'
)
```

### Exportación JSON

```python
# Exportar recomendaciones
export_data = system.export_recommendations_to_json(
    recommendations,
    filename="recomendaciones_cartagena.json"
)
```

## 📁 Estructura de Archivos JSON

```json
{
  "metadata": {
    "exported_at": "2024-01-15T10:30:00",
    "source": "IA Turística Colombia + Google Maps Places API",
    "version": "2.0",
    "total_categories": 3,
    "total_places": 15
  },
  "recommendations": {
    "city": "Cartagena",
    "user_info": {
      "user_id": 1,
      "name": "Juan Pérez",
      "travel_style": "cultural",
      "budget_range": "medio"
    },
    "categories": {
      "restaurants": {
        "total_found": 20,
        "ai_filtered": 5,
        "places": [
          {
            "name": "Restaurante El Santísimo",
            "address": "Calle del Santísimo, Cartagena",
            "rating": 4.5,
            "price_level": 3,
            "ai_score": 0.85,
            "match_reasons": [
              "Rating alto (4.5/5)",
              "Precio Moderado",
              "Bien valorado (15 reseñas)"
            ],
            "photos": ["https://maps.googleapis.com/..."],
            "reviews": [...],
            "opening_hours": {...}
          }
        ]
      }
    }
  }
}
```

## 🚀 Ejecución de Demostraciones

### Demo Básica

```bash
python examples/google_maps_demo.py
```

### Demo Personalizada

```python
from enhanced_recommendations import EnhancedTourismRecommendationSystem

# Configurar API key
import os
os.environ['GOOGLE_MAPS_API_KEY'] = 'tu_api_key'

# Ejecutar demo
system = EnhancedTourismRecommendationSystem(os.getenv('GOOGLE_MAPS_API_KEY'))

# Generar recomendaciones para diferentes usuarios
for user_id in range(1, 4):
    recommendations = system.get_user_recommendations(user_id, 'bogota')
    system.export_recommendations_to_json(
        recommendations, 
        f"recomendaciones_usuario_{user_id}.json"
    )
```

## ⚙️ Configuración Avanzada

### Personalizar Búsquedas

```python
# Configurar parámetros de búsqueda
system.google_maps_client.SEARCH_CONFIG.update({
    'default_radius': 15000,  # 15km
    'max_results_per_category': 15,
    'delay_between_requests': 0.3
})
```

### Agregar Nuevas Ciudades

```python
# En config.py
COLOMBIAN_CITIES['nueva_ciudad'] = {
    'name': 'Nueva Ciudad',
    'lat': 'lat_coord',
    'lng': 'lng_coord',
    'department': 'Departamento'
}
```

## 🔍 Troubleshooting

### Errores Comunes

1. **API Key no configurada**
   ```
   Error: GOOGLE_MAPS_API_KEY no configurada
   Solución: Configurar variable de entorno
   ```

2. **Límite de cuota excedido**
   ```
   Error: OVER_QUERY_LIMIT
   Solución: Verificar cuota en Google Cloud Console
   ```

3. **Lugar no encontrado**
   ```
   Error: NOT_FOUND
   Solución: Verificar que el lugar existe en Google Maps
   ```

### Optimización de Rendimiento

- Usar delays entre peticiones para evitar rate limiting
- Implementar caché para lugares ya consultados
- Filtrar resultados por relevancia antes de obtener detalles

## 📈 Métricas y Monitoreo

### Estadísticas de Uso

```python
# Obtener estadísticas de recomendaciones
stats = {
    'total_places_found': len(all_places),
    'ai_filtered_places': len(filtered_places),
    'export_success_rate': successful_exports / total_exports,
    'average_ai_score': sum(scores) / len(scores)
}
```

### Logs de API

```python
# Habilitar logging detallado
import logging
logging.basicConfig(level=logging.INFO)
```

## 🔐 Consideraciones de Seguridad

1. **API Key**: Nunca hardcodear en el código
2. **Restricciones**: Configurar restricciones de IP/dominio
3. **Cuotas**: Monitorear uso para evitar costos inesperados
4. **Datos**: Respetar políticas de privacidad de Google

## 📞 Soporte

Para problemas específicos con Google Maps API:
- [Documentación Oficial](https://developers.google.com/maps/documentation/places)
- [Google Cloud Support](https://cloud.google.com/support)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-maps)

## 🎉 Próximos Pasos

1. **Integración Frontend**: Conectar con React/Vue.js
2. **Caché Inteligente**: Implementar Redis para optimización
3. **Análisis Avanzado**: Agregar machine learning para patrones de usuario
4. **Geolocalización**: Integrar con GPS para recomendaciones basadas en ubicación
