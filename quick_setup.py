#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración Rápida del Sistema de IA Turística para Colombia
Script automatizado para configurar el sistema desde cero
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class QuickSetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.setup_log = []
        
    def log(self, message):
        """Registra mensajes del setup"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        self.setup_log.append(log_message)
    
    def check_python_version(self):
        """Verifica la versión de Python"""
        self.log("🐍 Verificando versión de Python...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.log("❌ Python 3.8+ requerido")
            self.log(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
            return False
        
        self.log(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    
    def check_disk_space(self):
        """Verifica espacio en disco"""
        self.log("💾 Verificando espacio en disco...")
        
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.base_dir)
            free_gb = free // (1024**3)
            
            if free_gb < 5:
                self.log(f"⚠️ Espacio insuficiente: {free_gb}GB disponibles (5GB requeridos)")
                return False
            
            self.log(f"✅ Espacio disponible: {free_gb}GB - OK")
            return True
            
        except Exception as e:
            self.log(f"⚠️ No se pudo verificar espacio: {e}")
            return True  # Continuar de todas formas
    
    def install_dependencies(self):
        """Instala las dependencias"""
        self.log("📦 Instalando dependencias...")
        
        try:
            # Actualizar pip
            self.log("   Actualizando pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            
            # Instalar dependencias
            self.log("   Instalando dependencias principales...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            
            self.log("✅ Dependencias instaladas correctamente")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Error instalando dependencias: {e}")
            return False
    
    def setup_environment(self):
        """Configura el entorno"""
        self.log("⚙️ Configurando entorno...")
        
        try:
            result = subprocess.run([sys.executable, "setup_environment.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Entorno configurado correctamente")
                return True
            else:
                self.log(f"❌ Error configurando entorno: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error ejecutando setup_environment.py: {e}")
            return False
    
    def train_models(self):
        """Entrena los modelos"""
        self.log("🤖 Entrenando modelos...")
        
        try:
            result = subprocess.run([sys.executable, "train_simple.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Modelos entrenados correctamente")
                return True
            else:
                self.log(f"❌ Error entrenando modelos: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error ejecutando train_simple.py: {e}")
            return False
    
    def optimize_models(self):
        """Optimiza los modelos para móviles"""
        self.log("📱 Optimizando modelos para móviles...")
        
        try:
            result = subprocess.run([sys.executable, "optimize_simple.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Modelos optimizados correctamente")
                return True
            else:
                self.log(f"❌ Error optimizando modelos: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error ejecutando optimize_simple.py: {e}")
            return False
    
    def test_system(self):
        """Prueba el sistema completo"""
        self.log("🧪 Probando sistema completo...")
        
        try:
            result = subprocess.run([sys.executable, "test_complete_system.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Sistema probado correctamente")
                return True
            else:
                self.log(f"❌ Error probando sistema: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"❌ Error ejecutando test_complete_system.py: {e}")
            return False
    
    def save_setup_log(self):
        """Guarda el log del setup"""
        log_path = self.base_dir / "setup_log.txt"
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("🇨🇴 LOG DE CONFIGURACIÓN RÁPIDA\n")
            f.write("=" * 50 + "\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            for log_entry in self.setup_log:
                f.write(log_entry + "\n")
        
        self.log(f"📄 Log guardado en: {log_path}")
    
    def run_quick_setup(self):
        """Ejecuta la configuración rápida completa"""
        print("🇨🇴 CONFIGURACIÓN RÁPIDA - IA TURÍSTICA PARA COLOMBIA")
        print("=" * 60)
        print("Configurando el sistema desde cero...")
        print("=" * 60)
        
        steps = [
            ("Verificar Python", self.check_python_version),
            ("Verificar espacio", self.check_disk_space),
            ("Instalar dependencias", self.install_dependencies),
            ("Configurar entorno", self.setup_environment),
            ("Entrenar modelos", self.train_models),
            ("Optimizar modelos", self.optimize_models),
            ("Probar sistema", self.test_system)
        ]
        
        successful_steps = 0
        total_steps = len(steps)
        
        for step_name, step_func in steps:
            self.log(f"\n🔄 {step_name}...")
            
            if step_func():
                successful_steps += 1
                self.log(f"✅ {step_name} - COMPLETADO")
            else:
                self.log(f"❌ {step_name} - FALLÓ")
                self.log("⚠️ Continuando con los siguientes pasos...")
        
        # Guardar log
        self.save_setup_log()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("🎯 RESUMEN DE CONFIGURACIÓN")
        print("=" * 60)
        print(f"✅ Pasos completados: {successful_steps}/{total_steps}")
        print(f"📊 Tasa de éxito: {(successful_steps/total_steps)*100:.1f}%")
        
        if successful_steps >= 5:  # Al menos 5 de 7 pasos
            print("\n🎉 ¡CONFIGURACIÓN EXITOSA!")
            print("🇨🇴 El sistema de IA Turística está listo para usar")
            print("\n📋 PRÓXIMOS PASOS:")
            print("1. Ejecutar: python test_complete_system.py")
            print("2. Probar: python examples/basic_usage.py")
            print("3. Ver documentación en docs/")
            return True
        else:
            print("\n⚠️ CONFIGURACIÓN PARCIAL")
            print("🔧 Algunos pasos fallaron, revisar setup_log.txt")
            print("\n📋 PASOS MANUALES:")
            print("1. Revisar errores en setup_log.txt")
            print("2. Ejecutar pasos fallidos manualmente")
            print("3. Contactar soporte si persisten los problemas")
            return False

if __name__ == "__main__":
    setup = QuickSetup()
    success = setup.run_quick_setup()
    
    if success:
        print(f"\n🎯 RESULTADO: SISTEMA LISTO")
        sys.exit(0)
    else:
        print(f"\n⚠️ RESULTADO: REVISAR CONFIGURACIÓN")
        sys.exit(1)
