"""
Script pour vérifier la disponibilité du GPU et les capacités CUDA
"""

import torch
import sys

def check_gpu():
    """Vérifie et affiche les informations sur le GPU"""
    
    print("\n" + "="*70)
    print("🔍 VÉRIFICATION DU GPU ET CUDA")
    print("="*70 + "\n")
    
    # Version de PyTorch
    print(f"📦 Version de PyTorch : {torch.__version__}")
    
    # Disponibilité CUDA
    cuda_available = torch.cuda.is_available()
    print(f"\n🎮 CUDA disponible : {'✅ OUI' if cuda_available else '❌ NON'}")
    
    if cuda_available:
        # Version CUDA
        print(f"   Version CUDA : {torch.version.cuda}")
        print(f"   Version cuDNN : {torch.backends.cudnn.version()}")
        
        # Nombre de GPUs
        gpu_count = torch.cuda.device_count()
        print(f"\n🖥️  Nombre de GPUs : {gpu_count}")
        
        # Informations pour chaque GPU
        for i in range(gpu_count):
            print(f"\n   GPU {i}:")
            print(f"      Nom : {torch.cuda.get_device_name(i)}")
            
            # Capacité de mémoire
            total_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
            print(f"      Mémoire totale : {total_memory:.2f} GB")
            
            # Mémoire disponible
            if torch.cuda.is_available():
                torch.cuda.set_device(i)
                allocated = torch.cuda.memory_allocated(i) / (1024**3)
                reserved = torch.cuda.memory_reserved(i) / (1024**3)
                free = total_memory - reserved
                print(f"      Mémoire allouée : {allocated:.2f} GB")
                print(f"      Mémoire réservée : {reserved:.2f} GB")
                print(f"      Mémoire libre : {free:.2f} GB")
            
            # Capacité de calcul
            capability = torch.cuda.get_device_capability(i)
            print(f"      Compute Capability : {capability[0]}.{capability[1]}")
        
        # Test simple
        print("\n🧪 Test d'allocation GPU...")
        try:
            x = torch.rand(1000, 1000).cuda()
            y = torch.rand(1000, 1000).cuda()
            z = x @ y
            print("   ✅ Test réussi ! Le GPU fonctionne correctement.")
            
            # Benchmark simple
            import time
            print("\n⚡ Benchmark simple (multiplication de matrices):")
            
            # CPU
            x_cpu = torch.rand(2000, 2000)
            y_cpu = torch.rand(2000, 2000)
            start = time.time()
            z_cpu = x_cpu @ y_cpu
            cpu_time = time.time() - start
            print(f"   CPU : {cpu_time:.4f} secondes")
            
            # GPU
            x_gpu = torch.rand(2000, 2000).cuda()
            y_gpu = torch.rand(2000, 2000).cuda()
            torch.cuda.synchronize()
            start = time.time()
            z_gpu = x_gpu @ y_gpu
            torch.cuda.synchronize()
            gpu_time = time.time() - start
            print(f"   GPU : {gpu_time:.4f} secondes")
            
            speedup = cpu_time / gpu_time
            print(f"   🚀 Accélération : {speedup:.2f}x plus rapide")
            
        except Exception as e:
            print(f"   ❌ Erreur lors du test : {e}")
    
    else:
        print("\n⚠️  Aucun GPU détecté. Raisons possibles :")
        print("   1. Aucun GPU NVIDIA installé")
        print("   2. Drivers NVIDIA non installés ou obsolètes")
        print("   3. PyTorch installé sans support CUDA")
        print("\n💡 Pour installer PyTorch avec CUDA :")
        print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        print("   (Remplacez cu118 par votre version CUDA)")
    
    # Recommandations pour l'entraînement
    print("\n" + "="*70)
    print("📋 RECOMMANDATIONS POUR L'ENTRAÎNEMENT")
    print("="*70 + "\n")
    
    if cuda_available:
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        if gpu_memory >= 8:
            print("✅ Votre GPU a suffisamment de mémoire pour l'entraînement YOLOv8")
            print("   Batch size recommandé : 16-32")
        elif gpu_memory >= 4:
            print("⚠️  Mémoire GPU limitée")
            print("   Batch size recommandé : 8-16")
        else:
            print("⚠️  Mémoire GPU très limitée")
            print("   Batch size recommandé : 4-8")
        
        print(f"\n   Avec GPU, l'entraînement sera environ 10-20x plus rapide")
        print(f"   Temps estimé : 30-90 minutes pour 50 epochs")
    else:
        print("⚠️  Sans GPU, l'entraînement sera plus lent")
        print("   Temps estimé : 8-15 heures pour 50 epochs sur CPU")
    
    print("\n" + "="*70)
    
    return cuda_available


if __name__ == '__main__':
    gpu_available = check_gpu()
    sys.exit(0 if gpu_available else 1)
