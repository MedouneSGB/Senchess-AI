"""
Script pour downgrader PyTorch 2.9 → 2.8 (compatible IPEX)
"""

import subprocess
import sys

def downgrade_pytorch():
    """Downgrade PyTorch vers version 2.8 compatible avec IPEX"""
    
    print("=" * 70)
    print("🔄 DOWNGRADE PYTORCH 2.9 → 2.8")
    print("=" * 70)
    print()
    print("⚠️  Cela va désinstaller PyTorch 2.9.0 et installer PyTorch 2.8.0")
    print("    (Nécessaire pour tester IPEX avec Intel Iris Xe)")
    print()
    
    response = input("Continuer ? (oui/non) : ").strip().lower()
    if response not in ['oui', 'o', 'yes', 'y']:
        print("❌ Annulé par l'utilisateur")
        return
    
    print("\n📦 Désinstallation de PyTorch 2.9.0...")
    subprocess.run([
        sys.executable, "-m", "pip", "uninstall", "-y",
        "torch", "torchvision", "torchaudio"
    ])
    
    print("\n📦 Installation de PyTorch 2.8.0 + CPU...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "torch==2.8.0",
        "torchvision==0.19.0",
        "torchaudio==2.5.0",
        "--index-url", "https://download.pytorch.org/whl/cpu"
    ])
    
    print("\n📦 Réinstallation d'IPEX 2.8.10...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "intel-extension-for-pytorch==2.8.10+xpu",
        "-f", "https://pytorch-extension.intel.com/release-whl/stable/xpu/us/"
    ])
    
    print("\n✅ Downgrade terminé !")
    print()
    print("🔄 Vous pouvez maintenant relancer : python experiment_ipex.py")
    print()
    print("📝 Note : Pour revenir à PyTorch 2.9 après les tests :")
    print("    pip install torch torchvision torchaudio")

if __name__ == "__main__":
    downgrade_pytorch()
