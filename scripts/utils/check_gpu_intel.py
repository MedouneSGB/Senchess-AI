"""
Script pour vérifier la disponibilité du GPU Intel et les capacités
"""

import torch
import sys

def check_intel_gpu():
    """Vérifie et affiche les informations sur le GPU Intel"""
    
    print("\n" + "="*70)
    print("🔍 VÉRIFICATION DU GPU INTEL")
    print("="*70 + "\n")
    
    # Version de PyTorch
    print(f"📦 Version de PyTorch : {torch.__version__}")
    
    # Vérifier Intel Extension
    try:
        import intel_extension_for_pytorch as ipex
        print(f"📦 Intel Extension pour PyTorch : {ipex.__version__}")
        has_ipex = True
    except ImportError:
        print("⚠️  Intel Extension pour PyTorch non installé")
        print("   Exécutez : python install_gpu_intel.py")
        has_ipex = False
    
    print()
    
    # Vérifier les devices disponibles
    print("🖥️  Devices disponibles :")
    
    # CPU (toujours disponible)
    print("   ✅ CPU disponible")
    
    # XPU (Intel GPU)
    if has_ipex and hasattr(torch, 'xpu'):
        try:
            if torch.xpu.is_available():
                device_count = torch.xpu.device_count()
                print(f"   ✅ Intel XPU (GPU) disponible - {device_count} device(s)")
                
                for i in range(device_count):
                    device_name = torch.xpu.get_device_name(i)
                    print(f"      Device {i}: {device_name}")
                
                recommended_device = 'xpu'
            else:
                print("   ❌ Intel XPU non disponible")
                recommended_device = 'cpu'
        except Exception as e:
            print(f"   ❌ Erreur XPU : {e}")
            recommended_device = 'cpu'
    else:
        print("   ⚠️  Intel XPU non configuré")
        recommended_device = 'cpu'
    
    # CUDA (pour info)
    if torch.cuda.is_available():
        print(f"   ✅ CUDA disponible - {torch.cuda.device_count()} GPU(s)")
        recommended_device = 'cuda'
    else:
        print("   ❌ CUDA non disponible")
    
    print(f"\n🎯 Device recommandé : {recommended_device.upper()}")
    
    # Test simple
    if recommended_device != 'cpu':
        print(f"\n🧪 Test d'allocation sur {recommended_device.upper()}...")
        try:
            if recommended_device == 'xpu':
                x = torch.rand(1000, 1000).to('xpu')
                y = torch.rand(1000, 1000).to('xpu')
                z = x @ y
                print("   ✅ Test réussi ! Le GPU Intel fonctionne.")
            elif recommended_device == 'cuda':
                x = torch.rand(1000, 1000).cuda()
                y = torch.rand(1000, 1000).cuda()
                z = x @ y
                print("   ✅ Test réussi ! Le GPU CUDA fonctionne.")
            
            # Benchmark simple
            print("\n⚡ Benchmark simple (multiplication de matrices 2000x2000):")
            import time
            
            # CPU
            x_cpu = torch.rand(2000, 2000)
            y_cpu = torch.rand(2000, 2000)
            start = time.time()
            z_cpu = x_cpu @ y_cpu
            cpu_time = time.time() - start
            print(f"   CPU : {cpu_time:.4f} secondes")
            
            # GPU
            if recommended_device == 'xpu':
                x_gpu = torch.rand(2000, 2000).to('xpu')
                y_gpu = torch.rand(2000, 2000).to('xpu')
                torch.xpu.synchronize()
                start = time.time()
                z_gpu = x_gpu @ y_gpu
                torch.xpu.synchronize()
                gpu_time = time.time() - start
                print(f"   Intel XPU : {gpu_time:.4f} secondes")
            elif recommended_device == 'cuda':
                x_gpu = torch.rand(2000, 2000).cuda()
                y_gpu = torch.rand(2000, 2000).cuda()
                torch.cuda.synchronize()
                start = time.time()
                z_gpu = x_gpu @ y_gpu
                torch.cuda.synchronize()
                gpu_time = time.time()- start
                print(f"   CUDA : {gpu_time:.4f} secondes")
            
            speedup = cpu_time / gpu_time
            print(f"   🚀 Accélération : {speedup:.2f}x plus rapide")
            
        except Exception as e:
            print(f"   ❌ Erreur lors du test : {e}")
    
    # Recommandations
    print("\n" + "="*70)
    print("📋 RECOMMANDATIONS POUR L'ENTRAÎNEMENT")
    print("="*70 + "\n")
    
    if recommended_device == 'xpu':
        print("✅ GPU Intel Iris Xe détecté et fonctionnel")
        print("   Batch size recommandé : 8-16")
        print("   Le GPU Intel devrait accélérer l'entraînement de 2-4x")
        print("   Temps estimé : 3-5 heures pour 100 epochs")
    elif recommended_device == 'cuda':
        print("✅ GPU NVIDIA détecté et fonctionnel")
        print("   Batch size recommandé : 16-32")
        print("   Temps estimé : 45-90 minutes pour 100 epochs")
    else:
        print("⚠️  Aucun GPU détecté, utilisation du CPU")
        print("   Batch size recommandé : 4-8")
        print("   Temps estimé : 6-10 heures pour 100 epochs")
        
        if not has_ipex:
            print("\n💡 Pour utiliser votre GPU Intel Iris Xe :")
            print("   Exécutez : python install_gpu_intel.py")
    
    print("\n" + "="*70)
    
    return recommended_device


if __name__ == '__main__':
    device = check_intel_gpu()
    print(f"\nDevice sélectionné : {device}")
