"""
🧪 EXPÉRIMENTATION : Intel Extension for PyTorch (IPEX)
Test du support GPU Intel Iris Xe Graphics

Ce script teste progressivement les capacités IPEX :
1. Installation et détection
2. Tests basiques GPU
3. Benchmark CPU vs XPU
4. Training YOLO avec XPU
"""

import sys
import subprocess

def step_1_install_ipex():
    """Étape 1 : Installation d'IPEX"""
    print("\n" + "="*70)
    print("📦 ÉTAPE 1 : INSTALLATION D'IPEX")
    print("="*70 + "\n")
    
    print("Installation d'Intel Extension for PyTorch...")
    print("(Cela peut prendre 5-10 minutes...)\n")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 
            'intel-extension-for-pytorch',
            '--extra-index-url', 
            'https://pytorch-extension.intel.com/release-whl/stable/xpu/us/'
        ], check=True)
        
        print("\n✅ Installation réussie !")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur d'installation : {e}")
        print("\n💡 Alternative : Installation version CPU uniquement")
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                'intel-extension-for-pytorch'
            ], check=True)
            print("\n✅ IPEX CPU installé (pas de support XPU)")
            return False
        except:
            print("❌ Installation échouée complètement")
            return False


def step_2_test_detection():
    """Étape 2 : Test de détection GPU"""
    print("\n" + "="*70)
    print("🔍 ÉTAPE 2 : DÉTECTION DU GPU INTEL")
    print("="*70 + "\n")
    
    try:
        import torch
        import intel_extension_for_pytorch as ipex
        
        print(f"✅ PyTorch version : {torch.__version__}")
        print(f"✅ IPEX version : {ipex.__version__}")
        print()
        
        # Vérifier XPU
        if hasattr(torch, 'xpu') and torch.xpu.is_available():
            print("🎉 Intel XPU (GPU) DÉTECTÉ !")
            device_count = torch.xpu.device_count()
            print(f"   Nombre de devices : {device_count}")
            
            for i in range(device_count):
                device_name = torch.xpu.get_device_name(i)
                print(f"   Device {i} : {device_name}")
            
            return True, 'xpu'
        else:
            print("⚠️  XPU non disponible")
            print("   IPEX fonctionnera en mode CPU optimisé")
            return True, 'cpu'
            
    except ImportError:
        print("❌ IPEX non installé correctement")
        return False, None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False, None


def step_3_benchmark(device):
    """Étape 3 : Benchmark CPU vs XPU"""
    print("\n" + "="*70)
    print("⚡ ÉTAPE 3 : BENCHMARK DE PERFORMANCE")
    print("="*70 + "\n")
    
    import torch
    import intel_extension_for_pytorch as ipex
    import time
    
    print("Test : Multiplication de matrices 3000x3000\n")
    
    # Test CPU
    print("🖥️  Test CPU...")
    x_cpu = torch.rand(3000, 3000)
    y_cpu = torch.rand(3000, 3000)
    
    start = time.time()
    for _ in range(5):
        z = x_cpu @ y_cpu
    cpu_time = (time.time() - start) / 5
    print(f"   Temps moyen : {cpu_time:.4f} secondes")
    
    if device == 'xpu':
        # Test XPU
        print("\n🎮 Test XPU (GPU Intel)...")
        try:
            x_xpu = torch.rand(3000, 3000).to('xpu')
            y_xpu = torch.rand(3000, 3000).to('xpu')
            
            # Warmup
            for _ in range(2):
                z = x_xpu @ y_xpu
            torch.xpu.synchronize()
            
            start = time.time()
            for _ in range(5):
                z = x_xpu @ y_xpu
            torch.xpu.synchronize()
            xpu_time = (time.time() - start) / 5
            print(f"   Temps moyen : {xpu_time:.4f} secondes")
            
            speedup = cpu_time / xpu_time
            print(f"\n🚀 Accélération GPU : {speedup:.2f}x plus rapide !")
            
            if speedup > 1.5:
                print("   ✅ Le GPU apporte un gain significatif")
                return True
            else:
                print("   ⚠️  Gain limité, CPU peut être préférable")
                return False
                
        except Exception as e:
            print(f"   ❌ Erreur XPU : {e}")
            return False
    else:
        print("\n💡 XPU non disponible, pas de comparaison GPU")
        return False


def step_4_yolo_test(device):
    """Étape 4 : Test YOLO avec XPU"""
    print("\n" + "="*70)
    print("🎯 ÉTAPE 4 : TEST YOLO AVEC XPU")
    print("="*70 + "\n")
    
    if device != 'xpu':
        print("⚠️  XPU non disponible, impossible de tester YOLO avec GPU")
        print("   Ultralytics ne supporte pas encore device='xpu' directement")
        return False
    
    print("⚠️  LIMITATION IMPORTANTE :")
    print("   Ultralytics YOLO ne supporte pas encore device='xpu' nativement")
    print("   Il faudrait modifier le code source d'Ultralytics")
    print()
    print("💡 SOLUTION ALTERNATIVE :")
    print("   1. Entraîner sur CPU (en cours)")
    print("   2. Convertir le modèle vers OpenVINO")
    print("   3. Utiliser OpenVINO pour l'inférence GPU")
    print()
    
    return False


def main():
    """Exécution complète de l'expérimentation"""
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║         🧪 EXPÉRIMENTATION IPEX - GPU INTEL IRIS XE             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

Objectif : Tester si le GPU Intel Iris Xe peut accélérer l'entraînement

⚠️  DISCLAIMER :
    - Support expérimental pour Iris Xe
    - Peut ne pas fonctionner sur tous les systèmes
    - Les drivers Intel doivent être à jour
    - Ultralytics YOLO ne supporte pas XPU nativement

📋 Plan d'expérimentation :
    1. Installation IPEX
    2. Détection du GPU Intel
    3. Benchmark CPU vs XPU
    4. Discussion sur YOLO + XPU

Prêt à commencer ? (Ctrl+C pour annuler)
""")
    
    input("Appuyez sur Entrée pour continuer...")
    
    # Étape 1 : Installation
    xpu_available = step_1_install_ipex()
    
    # Étape 2 : Détection
    success, device = step_2_test_detection()
    
    if not success:
        print("\n❌ Impossible de continuer sans IPEX fonctionnel")
        return
    
    # Étape 3 : Benchmark
    xpu_useful = step_3_benchmark(device)
    
    # Étape 4 : Test YOLO
    step_4_yolo_test(device)
    
    # Conclusion
    print("\n" + "="*70)
    print("📊 RÉSULTAT DE L'EXPÉRIMENTATION")
    print("="*70 + "\n")
    
    if device == 'xpu' and xpu_useful:
        print("✅ GPU Intel XPU fonctionnel et utile !")
        print()
        print("⚠️  MAIS : Ultralytics YOLO ne supporte pas XPU directement")
        print()
        print("💡 RECOMMANDATIONS :")
        print("   1. Continuer l'entraînement sur CPU (stable)")
        print("   2. Utiliser OpenVINO pour l'inférence GPU après training")
        print("   3. Gain de 3-5x sur les prédictions/inférence")
    elif device == 'xpu':
        print("⚠️  XPU détecté mais gain de performance limité")
        print()
        print("💡 RECOMMANDATION : Rester sur CPU")
    else:
        print("ℹ️  XPU non disponible sur ce système")
        print()
        print("💡 ALTERNATIVES :")
        print("   - CPU avec optimisations Intel (actuel)")
        print("   - OpenVINO pour l'inférence")
        print("   - GPU cloud (Colab, Kaggle)")
    
    print("\n" + "="*70)
    print("\n🎓 Apprentissages de cette expérimentation :")
    print("   1. IPEX existe mais support XPU limité pour Iris Xe")
    print("   2. Les GPUs intégrés Intel sont pour graphisme, pas ML")
    print("   3. OpenVINO est la meilleure solution Intel pour ML")
    print("   4. Pour training : CPU ou GPU NVIDIA dédié")
    print("   5. Pour inférence : OpenVINO sur GPU Intel")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Expérimentation interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
