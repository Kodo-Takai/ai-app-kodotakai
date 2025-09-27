# 🇨🇴 Sistema de Recomendaciones Turísticas con IA

Sistema inteligente de recomendaciones turísticas para Colombia que combina Inteligencia Artificial con datos reales de Google Maps Places API.

## 🚀 Características Principales

- **🤖 IA Avanzada**: Sistema de recomendaciones personalizadas usando Machine Learning
- **🗺️ Google Maps Integration**: Datos reales de lugares, fotos, reviews y horarios
- **⚡ Optimizado**: Sistema de caché que reduce llamadas a API en 60%
- **📱 Multiplataforma**: Soporte para web y aplicaciones móviles
- **🏙️ Ciudades Colombianas**: Bogotá, Medellín, Cali, Cartagena, Barranquilla, Bucaramanga
- **🎯 Personalización**: Recomendaciones basadas en estilo de viaje y preferencias

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Sistema IA      │    │  Google Maps    │
│   (React/Vue)   │◄──►│  Recomendaciones │◄──►│  Places API     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   JSON Export   │    │  Filtrado IA     │    │  Datos Reales   │
│   (Resultados)  │    │  + Ranking       │    │  de Lugares     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📦 Instalación

### Prerrequisitos
- Python 3.8+
- API Key de Google Maps Platform
- pip (gestor de paquetes de Python)

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/ia-turistica-colombia.git
cd ia-turistica-colombia
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar API Key
```bash
# Crear archivo .env
cp env_example.txt .env

# Editar .env con tu API key
GOOGLE_MAPS_API_KEY=tu_api_key_aqui
```

### 5. Configurar Google Maps API
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto o selecciona uno existente
3. Habilita las siguientes APIs:
   - **Places API**
   - **Maps JavaScript API**
   - **Geocoding API**
4. Crea credenciales (API Key)
5. Configura restricciones de API key (recomendado)

## 🚀 Uso Rápido

### Demostración Básica
```bash
python examples/google_maps_demo.py
```

### Demostración Optimizada
```bash
python examples/optimized_demo.py
```

### Gestor de Caché
```bash
python cache_manager.py
```

## 📊 Ejemplo de Uso

```python
from enhanced_recommendations import EnhancedTourismRecommendationSystem

# Inicializar sistema
system = EnhancedTourismRecommendationSystem(api_key="tu_api_key")

# Generar recomendaciones para usuario 1 en Bogotá
recommendations = system.get_user_recommendations(user_id=1, city='bogota')

# Exportar a JSON para frontend
system.export_recommendations_to_json(recommendations, "recomendaciones.json")
```

## 🎯 Tipos de Recomendaciones

### 🍽️ Restaurantes
- Cocina colombiana e internacional
- Filtrado por rating y precio
- Información de horarios y contacto

### 🏨 Hoteles
- Alojamiento de diferentes categorías
- Amenidades y servicios
- Ubicación y accesibilidad

### 🏛️ Atracciones Turísticas
- Lugares históricos y culturales
- Parques y espacios naturales
- Museos y centros artísticos

## ⚡ Optimizaciones Implementadas

### 💾 Sistema de Caché
- **Duración**: 1 hora
- **Reducción**: 60% menos llamadas a API
- **Eficiencia**: 80-90% de aciertos en búsquedas repetidas

### 🎯 Límite Inteligente
- **8 lugares máximo** por categoría
- **Resultados más relevantes**
- **Procesamiento más rápido**

### 📊 Estadísticas en Tiempo Real
```python
# Obtener estadísticas de optimización
stats = client.get_optimization_stats()
print(f"Tasa de aciertos: {stats['cache_hit_ratio']:.1f}%")
```

## 🏙️ Ciudades Soportadas

| Ciudad | Departamento | Coordenadas |
|--------|-------------|-------------|
| Bogotá | Cundinamarca | 4.6097, -74.0817 |
| Medellín | Antioquia | 6.2442, -75.5812 |
| Cali | Valle del Cauca | 3.4516, -76.5320 |
| Cartagena | Bolívar | 10.3910, -75.4794 |
| Barranquilla | Atlántico | 10.9685, -74.7813 |
| Bucaramanga | Santander | 7.1193, -73.1227 |

## 📁 Estructura del Proyecto

```
ia-turistica-colombia/
├── 📁 docs/                          # Documentación
│   ├── google_maps_integration_guide.md
│   ├── IMPLEMENTACION_GOOGLE_MAPS.md
│   └── OPTIMIZACION_API.md
├── 📁 examples/                      # Ejemplos de uso
│   ├── google_maps_demo.py
│   └── optimized_demo.py
├── 📁 models/                        # Modelos de IA
│   └── final/
├── 🔧 api_cache.py                   # Sistema de caché
├── 🔧 cache_manager.py               # Gestor de caché
├── 🔧 config.py                      # Configuración
├── 🔧 enhanced_recommendations.py    # Sistema principal
├── 🔧 google_maps_client.py          # Cliente Google Maps
├── 🔧 hotel_recommendations.py       # Sistema de hoteles
├── 📄 requirements.txt               # Dependencias
└── 📄 README.md                      # Este archivo
```

## 🔧 Configuración Avanzada

### Personalizar Límites
```python
# En config.py
SEARCH_CONFIG = {
    'max_results_per_category': 5,  # Reducir a 5 lugares
    'cache_duration': 7200,  # 2 horas de caché
    'batch_size': 2,  # Lotes más pequeños
}
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

## 📊 Métricas de Rendimiento

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Lugares por categoría** | 20 | 8 | 60% menos |
| **Llamadas a API** | 60 | 24 | 60% menos |
| **Tiempo de respuesta** | 12-15s | 2-3s | 80% más rápido |
| **Caché efectivo** | 0% | 80-90% | Optimización total |

## 🛠️ Herramientas de Desarrollo

### Gestor de Caché
```bash
python cache_manager.py
```
- 📊 Ver estadísticas del caché
- 🧹 Limpiar caché expirado
- ⚡ Optimizar caché
- 📁 Gestionar archivos de caché

### Verificación de API
```bash
python setup_google_maps.py
```
- ✅ Verificar configuración
- 🔑 Validar API key
- 🌐 Probar conectividad
- 📦 Instalar dependencias

## 📈 Roadmap

### ✅ Completado
- [x] Sistema de recomendaciones con IA
- [x] Integración con Google Maps Places API
- [x] Sistema de caché optimizado
- [x] Límite de 8 lugares por categoría
- [x] Herramientas de gestión
- [x] Documentación completa

### 🚧 En Desarrollo
- [ ] Interfaz web con React/Vue.js
- [ ] Aplicación móvil nativa
- [ ] Sistema de reservas integrado
- [ ] Análisis de sentimientos en reviews

### 🔮 Futuro
- [ ] Machine Learning avanzado
- [ ] Predicción de tendencias turísticas
- [ ] Integración con redes sociales
- [ ] Sistema de recomendaciones colaborativas

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **David** - *Desarrollo inicial* - [tu-github](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- Google Maps Platform por la API de Places
- Comunidad de Python por las librerías
- Colombia por ser un país hermoso para visitar 🇨🇴

## 📞 Soporte

Si tienes preguntas o necesitas ayuda:

- 📧 Email: tu-email@ejemplo.com
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/ia-turistica-colombia/issues)
- 📖 Documentación: [docs/](docs/)

---

**¡Disfruta explorando Colombia con IA! 🇨🇴🤖✨**