#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpieza Final - Eliminar Tests y Archivos Innecesarios
Deja el repositorio completamente limpio para GitHub
"""

import os
import shutil
from pathlib import Path

class FinalCleanup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        
        # Archivos y carpetas a eliminar
        self.files_to_remove = [
            # Archivos de test y reportes
            "test_complete_system.py",
            "system_test_report.json",
            "ESTADO_FINAL.md",
            "GITHUB_READY.md",
            "cleanup_final.py",  # Este mismo archivo
            
            # Carpetas de desarrollo
            "tests/",
            "notebooks/",
            "scripts/",
            "src/",
            
            # Archivos de configuración de desarrollo
            "model_registry.json",
            "optimization_report.json",
            
            # Carpetas de datos temporales
            "data/sample/",
        ]

    def remove_unnecessary_files(self):
        """Elimina archivos innecesarios"""
        print("🗑️ Eliminando archivos innecesarios...")
        
        removed_count = 0
        
        for item in self.files_to_remove:
            item_path = self.base_dir / item
            
            if item_path.exists():
                if item_path.is_dir():
                    shutil.rmtree(item_path)
                    print(f"🗑️ Eliminada carpeta: {item}")
                else:
                    item_path.unlink()
                    print(f"🗑️ Eliminado archivo: {item}")
                removed_count += 1
        
        print(f"✅ Total eliminado: {removed_count} archivos/carpetas")

    def clean_data_folder(self):
        """Limpia la carpeta de datos"""
        print("\n📁 Limpiando carpeta de datos...")
        
        data_dir = self.base_dir / "data"
        if data_dir.exists():
            # Mantener solo sincelejo_sucre
            for item in data_dir.iterdir():
                if item.name != "sincelejo_sucre":
                    if item.is_dir():
                        shutil.rmtree(item)
                        print(f"🗑️ Eliminada carpeta: data/{item.name}")
                    else:
                        item.unlink()
                        print(f"🗑️ Eliminado archivo: data/{item.name}")

    def clean_models_folder(self):
        """Limpia la carpeta de modelos"""
        print("\n🤖 Limpiando carpeta de modelos...")
        
        models_dir = self.base_dir / "models"
        if models_dir.exists():
            # Eliminar archivos de configuración
            config_files = [
                "model_registry.json",
                "optimization_report.json"
            ]
            
            for config_file in config_files:
                config_path = models_dir / config_file
                if config_path.exists():
                    config_path.unlink()
                    print(f"🗑️ Eliminado: models/{config_file}")

    def create_minimal_structure(self):
        """Crea estructura mínima necesaria"""
        print("\n🏗️ Creando estructura mínima...")
        
        # Crear carpetas necesarias
        folders = [
            "docs/",
            "examples/",
        ]
        
        for folder in folders:
            folder_path = self.base_dir / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Carpeta: {folder}")

    def update_gitignore_minimal(self):
        """Actualiza .gitignore para versión mínima"""
        print("\n📄 Actualizando .gitignore...")
        
        gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# Sistema operativo
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/
'''
        
        gitignore_path = self.base_dir / ".gitignore"
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("📄 Actualizado: .gitignore")

    def create_minimal_readme(self):
        """Crea README mínimo"""
        print("\n📖 Creando README mínimo...")
        
        readme_content = '''# 🇨🇴 IA Turística para Colombia - Sincelejo y Sucre

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
'''
        
        readme_path = self.base_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("📖 Creado: README.md")

    def run_final_cleanup(self):
        """Ejecuta la limpieza final"""
        print("🧹 LIMPIEZA FINAL - ELIMINANDO TESTS Y ARCHIVOS INNECESARIOS")
        print("=" * 70)
        print("Dejando el repositorio completamente limpio")
        print("=" * 70)
        
        # Ejecutar limpieza
        self.create_minimal_structure()
        self.remove_unnecessary_files()
        self.clean_data_folder()
        self.clean_models_folder()
        self.update_gitignore_minimal()
        self.create_minimal_readme()
        
        print("\n🎉 LIMPIEZA FINAL COMPLETADA")
        print("=" * 70)
        print("✅ Repositorio completamente limpio")
        print("🗑️ Tests y archivos innecesarios eliminados")
        print("📁 Estructura mínima creada")
        print("📖 README simplificado")
        
        print("\n📋 ESTRUCTURA FINAL:")
        print("├── README.md")
        print("├── LICENSE")
        print("├── requirements.txt")
        print("├── pyproject.toml")
        print("├── .gitignore")
        print("├── .gitattributes")
        print("├── CONTRIBUTING.md")
        print("├── CHANGELOG.md")
        print("├── docs/")
        print("├── examples/")
        print("├── models/final/")
        print("└── data/sincelejo_sucre/")
        
        print("\n🚀 COMANDOS PARA GITHUB:")
        print("1. git init")
        print("2. git add .")
        print("3. git commit -m 'feat: IA turística para Colombia'")
        print("4. git remote add origin <repository-url>")
        print("5. git push -u origin main")
        
        print("\n🎯 ¡REPOSITORIO LISTO PARA COMPARTIR!")

if __name__ == "__main__":
    cleanup = FinalCleanup()
    cleanup.run_final_cleanup()
