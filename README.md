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

- **Recomendaciones Personalizadas**: Modelo MLPClassifier
- **Clasificación de Relevancia**: Modelo RandomForest
- **Procesamiento de Texto**: SentenceTransformer
- **Optimización Móvil**: ONNX/TensorFlow Lite
- **Funcionamiento Local**: Sin dependencia de internet

## 📱 Uso

```python
from examples.basic_usage import get_recommendations

# Obtener recomendaciones
recommendations = get_recommendations(user_id=0, limit=3)

for rec in recommendations:
    print(f"{rec['rank']}. {rec['name']} - {rec['category']}")
```

## 🤖 Modelos

- `models/final/` - Modelos entrenados
- `models/final/mobile/` - Modelos optimizados para móviles

## 📚 Documentación

- [Guía de Inicio](docs/quick_start_guide.md)
- [Integración Móvil](docs/mobile_integration_guide.md)
- [Resumen del Proyecto](docs/RESUMEN_FINAL.md)

## 🇨🇴 Datos Colombianos

- Actividades de Sincelejo y Sucre
- Procesamiento en español colombiano
- Categorías: cultural, naturaleza, gastronomía

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

**🇨🇴 ¡Listo para revolucionar el turismo en Colombia!**
