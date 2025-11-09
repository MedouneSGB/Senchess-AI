"""
Script d'installation automatique de PyTorch avec support CUDA
"""

import subprocess
import sys
import platform

def detect_cuda_version():
    """Détecte la version CUDA installée sur le système"""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            # Chercher la ligne avec CUDA Version
            for line in output.split('\n'):
                if 'CUDA Version' in line:
                    # Extraire la version
                    version = line.split('CUDA Version:')[1].strip().split()[0]
                    major = int(version.split('.')[0])
                    minor = int(version.split('.')[1])
                    return major, minor
    except Exception as e:
        print(f"Erreur lors de la détection CUDA : {e}")
    
    return None, None


def get_pytorch_install_command(cuda_major, cuda_minor):
    """Retourne la commande d'installation PyTorch appropriée"""
    
    # Mapper les versions CUDA aux URLs PyTorch
    if cuda_major == 11 and cuda_minor >= 8:
        return "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
    elif cuda_major == 12 and cuda_minor >= 1:
        return "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121"
    elif cuda_major == 11 and cuda_minor >= 7:
        return "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117"
    else:
        # Version générique pour CUDA 11.8
        return "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"


def install_pytorch_cuda():
    """Installe PyTorch avec support CUDA"""
    
    print("\n" + "="*70)
    print("🚀 INSTALLATION DE PYTORCH AVEC SUPPORT CUDA")
    print("="*70 + "\n")
    
    # Vérifier si nvidia-smi est disponible
    print("🔍 Détection du GPU NVIDIA...")
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Aucun GPU NVIDIA détecté ou drivers non installés")
            print("\n💡 Étapes à suivre :")
            print("   1. Vérifiez que vous avez un GPU NVIDIA")
            print("   2. Installez les drivers NVIDIA : https://www.nvidia.com/Download/index.aspx")
            print("   3. Redémarrez votre ordinateur")
            print("   4. Relancez ce script")
            return False
    except FileNotFoundError:
        print("❌ nvidia-smi non trouvé. Drivers NVIDIA non installés.")
        print("\n💡 Installez les drivers NVIDIA : https://www.nvidia.com/Download/index.aspx")
        return False
    
    # Détecter la version CUDA
    cuda_major, cuda_minor = detect_cuda_version()
    
    if cuda_major is None:
        print("⚠️  Impossible de détecter la version CUDA")
        print("   Installation de PyTorch avec CUDA 11.8 par défaut...")
        cuda_version = "11.8"
        install_cmd = "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
    else:
        cuda_version = f"{cuda_major}.{cuda_minor}"
        print(f"✅ CUDA Version détectée : {cuda_version}")
        install_cmd = get_pytorch_install_command(cuda_major, cuda_minor)
    
    print(f"\n📦 Commande d'installation :")
    print(f"   {install_cmd}")
    
    # Demander confirmation
    print()
    response = input("Voulez-vous installer PyTorch avec support CUDA ? (o/n): ")
    
    if response.lower() != 'o':
        print("❌ Installation annulée")
        return False
    
    # Désinstaller l'ancienne version
    print("\n🗑️  Désinstallation de l'ancienne version de PyTorch...")
    subprocess.run([sys.executable, '-m', 'pip', 'uninstall', '-y', 'torch', 'torchvision', 'torchaudio'])
    
    # Installer la nouvelle version
    print("\n📥 Installation de PyTorch avec CUDA...")
    print("   (Cela peut prendre quelques minutes...)\n")
    
    try:
        subprocess.run(install_cmd, shell=True, check=True)
        print("\n✅ Installation réussie !")
        
        # Vérifier l'installation
        print("\n🔍 Vérification de l'installation...")
        subprocess.run([sys.executable, 'check_gpu.py'])
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de l'installation : {e}")
        print("\n💡 Essayez d'installer manuellement :")
        print(f"   {install_cmd}")
        return False


def install_other_requirements():
    """Installe les autres dépendances depuis requirements.txt"""
    
    print("\n📦 Installation des autres dépendances...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation : {e}")
        return False


def main():
    """Fonction principale"""
    
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                SENCHESS AI - INSTALLATION GPU                  ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Vérifier le système d'exploitation
    os_name = platform.system()
    print(f"💻 Système d'exploitation : {os_name}")
    
    if os_name == "Windows":
        print("   ✅ Windows détecté")
    elif os_name == "Linux":
        print("   ✅ Linux détecté")
    else:
        print(f"   ⚠️  Système {os_name} - Ce script est optimisé pour Windows/Linux")
    
    # Installer PyTorch avec CUDA
    if install_pytorch_cuda():
        # Installer les autres dépendances
        install_other_requirements()
        
        print("\n" + "="*70)
        print("🎉 INSTALLATION TERMINÉE AVEC SUCCÈS !")
        print("="*70)
        print("\n🎯 Prochaines étapes :")
        print("   1. Vérifier le GPU : python check_gpu.py")
        print("   2. Lancer l'entraînement : python train_ultimate.py")
        print()
    else:
        print("\n❌ Installation échouée")
        print("\n💡 Installation manuelle :")
        print("   1. Vérifiez vos drivers NVIDIA : nvidia-smi")
        print("   2. Consultez : https://pytorch.org/get-started/locally/")
        print("   3. Installez PyTorch manuellement avec la commande appropriée")


if __name__ == '__main__':
    main()
