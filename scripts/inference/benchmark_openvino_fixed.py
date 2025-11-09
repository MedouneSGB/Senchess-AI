"""
Benchmark optimisé OpenVINO avec support GPU Intel correct
"""

import time
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import argparse


def benchmark_openvino_native(model_path: str, image_path: str, device: str = 'CPU', n_runs: int = 20):
    """Benchmark avec OpenVINO natif (sans Ultralytics)"""
    import openvino as ov
    import cv2
    
    print(f"📦 Modèle OpenVINO natif")
    print(f"💻 Device: {device}")
    print()
    
    # Charger le modèle
    model_xml = Path(model_path) / "best.xml"
    if not model_xml.exists():
        print(f"❌ Modèle introuvable : {model_xml}")
        return None
    
    core = ov.Core()
    model = core.read_model(model_xml)
    
    # Compiler le modèle avec configuration optimisée
    config = {}
    if device == 'CPU':
        config['PERFORMANCE_HINT'] = 'LATENCY'
    elif device == 'GPU':
        config['PERFORMANCE_HINT'] = 'LATENCY'
        # GPU_THROUGHPUT_STREAMS n'existe pas pour GPU, on utilise juste LATENCY
    
    compiled_model = core.compile_model(model, device, config)
    
    # Charger l'image
    img = cv2.imread(str(image_path))
    img_resized = cv2.resize(img, (640, 640))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_normalized = img_rgb.astype(np.float32) / 255.0
    img_transposed = np.transpose(img_normalized, (2, 0, 1))
    img_batched = np.expand_dims(img_transposed, axis=0)
    
    # Warm-up
    print("🔥 Warm-up (5 runs)...")
    for _ in range(5):
        _ = compiled_model(img_batched)
    
    # Benchmark
    print(f"⏱️  Benchmark ({n_runs} runs)...")
    times = []
    for i in range(n_runs):
        start = time.time()
        _ = compiled_model(img_batched)
        end = time.time()
        elapsed = (end - start) * 1000
        times.append(elapsed)
        if (i + 1) % 5 == 0:
            print(f"   {i+1}/{n_runs}: {elapsed:.1f} ms")
    
    times = np.array(times)
    
    print()
    print("📊 RÉSULTATS :")
    print(f"   Moyenne : {times.mean():.1f} ms")
    print(f"   Médiane : {np.median(times):.1f} ms")
    print(f"   Min : {times.min():.1f} ms")
    print(f"   Max : {times.max():.1f} ms")
    print(f"   Std : {times.std():.1f} ms")
    print(f"   FPS : {1000 / times.mean():.1f}")
    
    return {
        'mean': times.mean(),
        'median': np.median(times),
        'min': times.min(),
        'max': times.max(),
        'std': times.std(),
        'fps': 1000 / times.mean()
    }


def benchmark_pytorch(model_path: str, image_path: str, n_runs: int = 20):
    """Benchmark PyTorch CPU"""
    print(f"📦 Modèle PyTorch")
    print(f"💻 Device: CPU")
    print()
    
    model = YOLO(model_path)
    
    # Warm-up
    print("🔥 Warm-up (5 runs)...")
    for _ in range(5):
        _ = model.predict(image_path, verbose=False, device='cpu')
    
    # Benchmark
    print(f"⏱️  Benchmark ({n_runs} runs)...")
    times = []
    for i in range(n_runs):
        start = time.time()
        _ = model.predict(image_path, verbose=False, device='cpu')
        end = time.time()
        elapsed = (end - start) * 1000
        times.append(elapsed)
        if (i + 1) % 5 == 0:
            print(f"   {i+1}/{n_runs}: {elapsed:.1f} ms")
    
    times = np.array(times)
    
    print()
    print("📊 RÉSULTATS :")
    print(f"   Moyenne : {times.mean():.1f} ms")
    print(f"   Médiane : {np.median(times):.1f} ms")
    print(f"   Min : {times.min():.1f} ms")
    print(f"   Max : {times.max():.1f} ms")
    print(f"   Std : {times.std():.1f} ms")
    print(f"   FPS : {1000 / times.mean():.1f}")
    
    return {
        'mean': times.mean(),
        'median': np.median(times),
        'min': times.min(),
        'max': times.max(),
        'std': times.std(),
        'fps': 1000 / times.mean()
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pytorch', default='models/senchess_intel_v1.0_quick2/weights/best.pt')
    parser.add_argument('--openvino', default='models/senchess_intel_v1.0_quick2/weights/best_openvino_model')
    parser.add_argument('--image', default='data/chess_dataset_1000/images/test')
    parser.add_argument('--runs', type=int, default=20)
    args = parser.parse_args()
    
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║         ⚡ BENCHMARK OPTIMISÉ PyTorch vs OpenVINO                ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    
    # Trouver une image
    image_path = args.image
    if Path(image_path).is_dir():
        images = list(Path(image_path).glob('*.png')) + list(Path(image_path).glob('*.jpg'))
        if images:
            image_path = str(images[0])
    
    print(f"🖼️  Image de test : {Path(image_path).name}")
    print()
    
    results = {}
    
    # 1. PyTorch CPU
    print("=" * 70)
    print("🔷 PYTORCH CPU (baseline)")
    print("=" * 70)
    print()
    results['pytorch_cpu'] = benchmark_pytorch(args.pytorch, image_path, args.runs)
    
    print()
    print("=" * 70)
    print()
    
    # 2. OpenVINO CPU
    print("=" * 70)
    print("🔶 OPENVINO CPU")
    print("=" * 70)
    print()
    results['openvino_cpu'] = benchmark_openvino_native(args.openvino, image_path, 'CPU', args.runs)
    
    print()
    print("=" * 70)
    print()
    
    # 3. OpenVINO GPU
    print("=" * 70)
    print("🚀 OPENVINO GPU (Intel Iris Xe)")
    print("=" * 70)
    print()
    try:
        results['openvino_gpu'] = benchmark_openvino_native(args.openvino, image_path, 'GPU', args.runs)
    except Exception as e:
        print(f"❌ Erreur GPU : {e}")
        results['openvino_gpu'] = None
    
    # Résumé comparatif
    print()
    print("=" * 70)
    print("📊 RÉSUMÉ COMPARATIF")
    print("=" * 70)
    print()
    
    print(f"{'Configuration':<25} {'Temps (ms)':<15} {'FPS':<10} {'Speedup':<10}")
    print("-" * 70)
    
    baseline = results['pytorch_cpu']['mean']
    
    for name, label in [
        ('pytorch_cpu', 'PyTorch CPU'),
        ('openvino_cpu', 'OpenVINO CPU'),
        ('openvino_gpu', 'OpenVINO GPU (Iris Xe)')
    ]:
        if results.get(name):
            stats = results[name]
            speedup = baseline / stats['mean']
            print(f"{label:<25} {stats['mean']:>10.1f} ms  {stats['fps']:>8.1f}  {speedup:>8.2f}x")
    
    print()
    print("=" * 70)
    print("🎯 CONCLUSION")
    print("=" * 70)
    print()
    
    if results.get('openvino_gpu'):
        gpu_speedup = baseline / results['openvino_gpu']['mean']
        cpu_speedup = baseline / results['openvino_cpu']['mean']
        
        if gpu_speedup > 1.5:
            print(f"✅ OpenVINO GPU est {gpu_speedup:.1f}x plus rapide que PyTorch !")
            print(f"   Recommandation : Utiliser OpenVINO GPU pour production")
        elif cpu_speedup > 1.2:
            print(f"✅ OpenVINO CPU offre un gain de {cpu_speedup:.1f}x")
            print(f"   OpenVINO GPU : {gpu_speedup:.1f}x")
        else:
            print(f"⚠️  Gains modestes : CPU {cpu_speedup:.1f}x, GPU {gpu_speedup:.1f}x")
            print(f"   PyTorch CPU reste compétitif pour ce modèle")
    else:
        print("⚠️  GPU Intel Iris Xe non disponible pour ce test")


if __name__ == "__main__":
    main()
