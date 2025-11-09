"""
Script de diagnostic OpenVINO pour comprendre les problèmes de performance
"""

import sys
import time
import numpy as np
from pathlib import Path

def check_openvino_installation():
    """Vérifie l'installation OpenVINO"""
    print("=" * 70)
    print("🔍 DIAGNOSTIC OpenVINO")
    print("=" * 70)
    print()
    
    # 1. Version OpenVINO
    print("📦 1. Version OpenVINO")
    print("-" * 70)
    try:
        import openvino as ov
        print(f"✅ OpenVINO installé : {ov.__version__}")
    except ImportError as e:
        print(f"❌ OpenVINO non installé : {e}")
        return False
    print()
    
    # 2. Devices disponibles
    print("💻 2. Devices disponibles")
    print("-" * 70)
    try:
        core = ov.Core()
        devices = core.available_devices()
        print(f"Devices détectés : {devices}")
        for device in devices:
            print(f"\n  📱 {device}:")
            try:
                properties = core.get_property(device, "FULL_DEVICE_NAME")
                print(f"     Nom: {properties}")
            except:
                pass
            
            # Afficher les capacités
            try:
                capabilities = core.get_property(device, "OPTIMIZATION_CAPABILITIES")
                print(f"     Capacités: {capabilities}")
            except:
                pass
    except Exception as e:
        print(f"❌ Erreur : {e}")
    print()
    
    # 3. PyTorch
    print("🔥 3. PyTorch")
    print("-" * 70)
    try:
        import torch
        print(f"✅ PyTorch : {torch.__version__}")
        print(f"   CPU disponible : {torch.cuda.is_available() == False or True}")
        print(f"   CUDA disponible : {torch.cuda.is_available()}")
        print(f"   Nombre de threads : {torch.get_num_threads()}")
    except ImportError as e:
        print(f"❌ PyTorch non installé : {e}")
    print()
    
    # 4. Ultralytics
    print("🎯 4. Ultralytics YOLO")
    print("-" * 70)
    try:
        from ultralytics import YOLO
        import ultralytics
        print(f"✅ Ultralytics : {ultralytics.__version__}")
    except ImportError as e:
        print(f"❌ Ultralytics non installé : {e}")
    print()
    
    return True


def test_openvino_inference():
    """Test d'inférence OpenVINO avec différentes configurations"""
    print("=" * 70)
    print("⚡ TEST INFÉRENCE OpenVINO")
    print("=" * 70)
    print()
    
    try:
        import openvino as ov
        from ultralytics import YOLO
        
        # Modèles
        pytorch_model = "models/senchess_intel_v1.0_quick2/weights/best.pt"
        openvino_model = "models/senchess_intel_v1.0_quick2/weights/best_openvino_model"
        test_image = "data/chess_dataset_1000/images/test/chess_0016_purple_classic_italienne.png"
        
        if not Path(openvino_model).exists():
            print(f"❌ Modèle OpenVINO introuvable : {openvino_model}")
            return
        
        if not Path(test_image).exists():
            # Trouver une image de test
            test_images = list(Path("data/chess_dataset_1000/images/test").glob("*.png"))
            if test_images:
                test_image = str(test_images[0])
            else:
                print("❌ Aucune image de test trouvée")
                return
        
        # Test 1: OpenVINO natif (sans Ultralytics)
        print("🔷 Test 1: OpenVINO natif")
        print("-" * 70)
        try:
            core = ov.Core()
            
            # Charger le modèle
            model_xml = Path(openvino_model) / "best.xml"
            if not model_xml.exists():
                print(f"⚠️  Fichier XML introuvable : {model_xml}")
            else:
                print(f"📂 Chargement : {model_xml}")
                
                # Tester différents devices
                for device in ['CPU', 'GPU', 'AUTO']:
                    try:
                        print(f"\n  💻 Device: {device}")
                        model = core.read_model(model_xml)
                        compiled_model = core.compile_model(model, device)
                        
                        # Préparer l'input (dummy)
                        input_layer = compiled_model.input(0)
                        input_shape = input_layer.shape
                        print(f"     Input shape: {input_shape}")
                        
                        # Inférence de test
                        dummy_input = np.random.randn(*input_shape).astype(np.float32)
                        
                        # Warm-up
                        _ = compiled_model(dummy_input)
                        
                        # Benchmark
                        n_runs = 10
                        times = []
                        for i in range(n_runs):
                            start = time.time()
                            _ = compiled_model(dummy_input)
                            end = time.time()
                            times.append((end - start) * 1000)
                        
                        print(f"     Temps moyen: {np.mean(times):.1f} ms")
                        print(f"     FPS: {1000 / np.mean(times):.1f}")
                        
                    except Exception as e:
                        print(f"     ❌ Erreur {device}: {e}")
        
        except Exception as e:
            print(f"❌ Erreur OpenVINO natif : {e}")
            import traceback
            traceback.print_exc()
        
        print()
        
        # Test 2: Via Ultralytics avec différents devices
        print("🔶 Test 2: Ultralytics + OpenVINO")
        print("-" * 70)
        
        for device_name in ['CPU', 'AUTO']:
            try:
                print(f"\n  💻 Device: {device_name}")
                model = YOLO(openvino_model, task='detect')
                
                # Warm-up
                _ = model.predict(test_image, verbose=False, device=device_name)
                
                # Benchmark
                n_runs = 10
                times = []
                for i in range(n_runs):
                    start = time.time()
                    _ = model.predict(test_image, verbose=False, device=device_name)
                    end = time.time()
                    times.append((end - start) * 1000)
                
                print(f"     Temps moyen: {np.mean(times):.1f} ms")
                print(f"     Min/Max: {np.min(times):.1f} / {np.max(times):.1f} ms")
                print(f"     Std: {np.std(times):.1f} ms")
                print(f"     FPS: {1000 / np.mean(times):.1f}")
                
            except Exception as e:
                print(f"     ❌ Erreur {device_name}: {e}")
        
        print()
        
        # Test 3: Comparaison PyTorch
        print("🔷 Test 3: PyTorch CPU (référence)")
        print("-" * 70)
        try:
            model = YOLO(pytorch_model)
            
            # Warm-up
            _ = model.predict(test_image, verbose=False, device='cpu')
            
            # Benchmark
            n_runs = 10
            times = []
            for i in range(n_runs):
                start = time.time()
                _ = model.predict(test_image, verbose=False, device='cpu')
                end = time.time()
                times.append((end - start) * 1000)
            
            print(f"  Temps moyen: {np.mean(times):.1f} ms")
            print(f"  Min/Max: {np.min(times):.1f} / {np.max(times):.1f} ms")
            print(f"  Std: {np.std(times):.1f} ms")
            print(f"  FPS: {1000 / np.mean(times):.1f}")
            
        except Exception as e:
            print(f"❌ Erreur PyTorch : {e}")
        
    except Exception as e:
        print(f"❌ Erreur générale : {e}")
        import traceback
        traceback.print_exc()


def check_performance_hints():
    """Vérifie les hints de performance OpenVINO"""
    print()
    print("=" * 70)
    print("⚙️  CONFIGURATION DE PERFORMANCE")
    print("=" * 70)
    print()
    
    try:
        import openvino as ov
        core = ov.Core()
        
        print("💡 Hints de performance disponibles :")
        print("-" * 70)
        print("  • LATENCY - Optimisé pour latence minimale (batch=1)")
        print("  • THROUGHPUT - Optimisé pour débit maximum (batch>1)")
        print("  • CUMULATIVE_THROUGHPUT - Pour plusieurs requêtes simultanées")
        print()
        
        print("💻 Configuration actuelle CPU :")
        try:
            print(f"  Nombre de streams: {core.get_property('CPU', 'NUM_STREAMS')}")
        except:
            print("  Nombre de streams: AUTO")
        
        print()
        print("📝 Recommandations :")
        print("-" * 70)
        print("  1. Pour inférence temps réel (webcam) :")
        print("     → Utiliser LATENCY mode")
        print("     → Device AUTO pour auto-sélection CPU/GPU")
        print()
        print("  2. Pour traitement batch :")
        print("     → Utiliser THROUGHPUT mode")
        print("     → Augmenter batch_size")
        print()
        print("  3. Pour GPU Intel Iris Xe :")
        print("     → Installer drivers Intel Graphics récents")
        print("     → Utiliser device='GPU' ou 'AUTO'")
        print("     → Préférer FP16 pour meilleure performance")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║           🔍 DIAGNOSTIC COMPLET OpenVINO                         ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    
    # 1. Vérifier l'installation
    if not check_openvino_installation():
        print("❌ Installation OpenVINO incomplète")
        return
    
    # 2. Tester l'inférence
    test_openvino_inference()
    
    # 3. Afficher les recommandations
    check_performance_hints()
    
    print()
    print("=" * 70)
    print("✅ Diagnostic terminé")
    print("=" * 70)


if __name__ == "__main__":
    main()
