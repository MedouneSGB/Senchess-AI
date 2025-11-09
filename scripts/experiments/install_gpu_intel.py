"""
Installation de PyTorch avec support pour GPU Intel Iris Xe
Utilise Intel Extension for PyTorch (IPEX)
"""

import subprocess
import sys

def install_intel_pytorch():
    """Installe PyTorch avec support Intel GPU"""
    
    print("\n" + "="*70)
    print("🚀 INSTALLATION DE PYTORCH POUR GPU INTEL IRIS XE")
    print("="*70 + "\n")
    
    print("📦 Installation de PyTorch et Intel Extension...")
    print("   (Cela peut prendre quelques minutes...)\n")
    
    packages = [
        "torch",
        "torchvision", 
        "torchaudio",
        "intel-extension-for-pytorch"
    ]
    
    try:
        for package in packages:
            print(f"📥 Installation de {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
        
        print("\n✅ Installation réussie !")
        
        # Tester l'installation
        print("\n🧪 Test de l'installation...")
        test_code = """
import torch
import intel_extension_for_pytorch as ipex

print(f"PyTorch version: {torch.__version__}")
print(f"IPEX version: {ipex.__version__}")

# Vérifier XPU (Intel GPU)
if hasattr(torch, 'xpu') and torch.xpu.is_available():
    print("✅ Intel GPU (XPU) disponible!")
    print(f"   Device: {torch.xpu.get_device_name(0)}")
else:
    print("⚠️  XPU non disponible, utilisation du CPU")
"""
        
        result = subprocess.run([sys.executable, '-c', test_code], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de l'installation : {e}")
        return False


if __name__ == '__main__':
    success = install_intel_pytorch()
    
    if success:
        print("\n" + "="*70)
        print("🎉 INSTALLATION TERMINÉE !")
        print("="*70)
        print("\n🎯 Prochaines étapes :")
        print("   1. Tester le GPU : python check_gpu_intel.py")
        print("   2. Entraîner le modèle : python train_new_model.py")
        print()
    else:
        print("\n❌ L'installation a échoué")
        print("💡 Note : Le GPU Intel Iris Xe peut nécessiter des drivers récents")
        print("   Mettez à jour vos drivers Intel : https://www.intel.com/content/www/us/en/download-center/home.html")
