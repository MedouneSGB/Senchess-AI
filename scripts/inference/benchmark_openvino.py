"""
Script pour tester l'inférence avec un modèle OpenVINO
Compare les performances PyTorch vs OpenVINO
"""

import time
import argparse
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np

def benchmark_model(model_path: str, image_path: str, n_runs: int = 10, device: str = 'CPU'):
    """
    Benchmark d'un modèle sur plusieurs inférences
    
    Args:
        model_path: Chemin vers le modèle
        image_path: Chemin vers l'image de test
        n_runs: Nombre d'inférences pour le benchmark
        device: Device OpenVINO (CPU, GPU, AUTO)
    """
    print(f"📦 Modèle : {Path(model_path).name}")
    print(f"🖼️  Image : {image_path}")
    print(f"🔄 Runs : {n_runs}")
    print(f"💻 Device : {device}")
    print()
    
    # Charger le modèle
    print("🔄 Chargement du modèle...")
    model = YOLO(model_path)
    
    # Vérifier que l'image existe
    if not Path(image_path).exists():
        print(f"❌ Image introuvable : {image_path}")
        return None
    
    # Warm-up (première inférence est plus lente)
    print("🔥 Warm-up...")
    _ = model.predict(image_path, verbose=False, device=device)
    
    # Benchmark
    print(f"⏱️  Benchmark {n_runs} inférences...")
    times = []
    
    for i in range(n_runs):
        start = time.time()
        results = model.predict(image_path, verbose=False, device=device)
        end = time.time()
        elapsed = (end - start) * 1000  # en ms
        times.append(elapsed)
        print(f"   Run {i+1}/{n_runs}: {elapsed:.1f} ms")
    
    # Statistiques
    times = np.array(times)
    print()
    print("📊 STATISTIQUES :")
    print(f"   Moyenne : {times.mean():.1f} ms")
    print(f"   Médiane : {np.median(times):.1f} ms")
    print(f"   Min : {times.min():.1f} ms")
    print(f"   Max : {times.max():.1f} ms")
    print(f"   Std : {times.std():.1f} ms")
    print(f"   FPS : {1000 / times.mean():.1f}")
    
    # Afficher les détections
    result = results[0]
    print()
    print("🎯 DÉTECTIONS :")
    if len(result.boxes) > 0:
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = result.names[cls]
            print(f"   - {class_name}: {conf:.2%}")
    else:
        print("   Aucune détection")
    
    return {
        'mean': times.mean(),
        'median': np.median(times),
        'min': times.min(),
        'max': times.max(),
        'std': times.std(),
        'fps': 1000 / times.mean()
    }


def compare_pytorch_openvino(pytorch_model: str, openvino_model: str, image_path: str, n_runs: int = 10):
    """
    Compare les performances PyTorch vs OpenVINO
    """
    print("=" * 70)
    print("⚡ COMPARAISON PYTORCH vs OPENVINO")
    print("=" * 70)
    print()
    
    # Benchmark PyTorch CPU
    print("🔷 PyTorch (CPU)")
    print("-" * 70)
    pytorch_stats = benchmark_model(pytorch_model, image_path, n_runs, device='cpu')
    
    print()
    print("=" * 70)
    print()
    
    # Benchmark OpenVINO CPU
    print("🔶 OpenVINO (CPU)")
    print("-" * 70)
    openvino_cpu_stats = benchmark_model(openvino_model, image_path, n_runs, device='CPU')
    
    print()
    print("=" * 70)
    print()
    
    # Benchmark OpenVINO GPU (si disponible)
    print("🔷 OpenVINO (GPU Intel)")
    print("-" * 70)
    try:
        openvino_gpu_stats = benchmark_model(openvino_model, image_path, n_runs, device='GPU')
    except Exception as e:
        print(f"⚠️  GPU Intel non disponible : {e}")
        openvino_gpu_stats = None
    
    print()
    print("=" * 70)
    print("📊 RÉSUMÉ COMPARATIF")
    print("=" * 70)
    print()
    
    # Tableau comparatif
    if pytorch_stats and openvino_cpu_stats:
        speedup_cpu = pytorch_stats['mean'] / openvino_cpu_stats['mean']
        print(f"{'Métrique':<20} {'PyTorch CPU':<15} {'OpenVINO CPU':<15} {'Gain':<10}")
        print("-" * 65)
        print(f"{'Temps moyen (ms)':<20} {pytorch_stats['mean']:>10.1f} ms  {openvino_cpu_stats['mean']:>10.1f} ms  {speedup_cpu:>6.2f}x")
        print(f"{'FPS':<20} {pytorch_stats['fps']:>10.1f}     {openvino_cpu_stats['fps']:>10.1f}     {speedup_cpu:>6.2f}x")
        
        if openvino_gpu_stats:
            speedup_gpu = pytorch_stats['mean'] / openvino_gpu_stats['mean']
            print()
            print(f"{'Métrique':<20} {'PyTorch CPU':<15} {'OpenVINO GPU':<15} {'Gain':<10}")
            print("-" * 65)
            print(f"{'Temps moyen (ms)':<20} {pytorch_stats['mean']:>10.1f} ms  {openvino_gpu_stats['mean']:>10.1f} ms  {speedup_gpu:>6.2f}x")
            print(f"{'FPS':<20} {pytorch_stats['fps']:>10.1f}     {openvino_gpu_stats['fps']:>10.1f}     {speedup_gpu:>6.2f}x")
        
        print()
        print("🎯 CONCLUSION :")
        if speedup_cpu >= 2.0:
            print(f"   ✅ OpenVINO CPU est {speedup_cpu:.1f}x plus rapide que PyTorch !")
        elif speedup_cpu >= 1.2:
            print(f"   ✅ OpenVINO CPU offre un gain de {speedup_cpu:.1f}x")
        else:
            print(f"   ⚠️  Gain modeste de {speedup_cpu:.1f}x (peut varier selon l'image)")
        
        if openvino_gpu_stats and openvino_gpu_stats['mean'] < openvino_cpu_stats['mean']:
            gpu_vs_cpu = openvino_cpu_stats['mean'] / openvino_gpu_stats['mean']
            print(f"   🚀 GPU Intel {gpu_vs_cpu:.1f}x plus rapide que CPU !")


def main():
    parser = argparse.ArgumentParser(description="Benchmark OpenVINO")
    parser.add_argument(
        '--pytorch',
        type=str,
        default='models/senchess_intel_v1.0_quick2/weights/best.pt',
        help='Modèle PyTorch (.pt)'
    )
    parser.add_argument(
        '--openvino',
        type=str,
        default=None,
        help='Modèle OpenVINO (détecté automatiquement si non spécifié)'
    )
    parser.add_argument(
        '--image',
        type=str,
        default='data/chess_dataset_1000/images/test',
        help='Chemin vers une image ou dossier de test'
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=10,
        help='Nombre d\'inférences pour le benchmark'
    )
    
    args = parser.parse_args()
    
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║              ⚡ BENCHMARK OpenVINO (Intel)                       ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    
    # Trouver une image de test
    image_path = args.image
    if Path(image_path).is_dir():
        # Prendre la première image du dossier
        images = list(Path(image_path).glob('*.jpg')) + list(Path(image_path).glob('*.png'))
        if images:
            image_path = str(images[0])
        else:
            print("❌ Aucune image trouvée dans le dossier")
            exit(1)
    
    # Détecter le modèle OpenVINO si non spécifié
    if args.openvino is None:
        pytorch_path = Path(args.pytorch)
        openvino_dir = pytorch_path.parent.parent / (pytorch_path.stem + "_openvino_model")
        if openvino_dir.exists():
            args.openvino = str(openvino_dir)
            print(f"✅ Modèle OpenVINO détecté : {args.openvino}")
        else:
            print(f"❌ Modèle OpenVINO introuvable : {openvino_dir}")
            print()
            print("💡 Exportez d'abord le modèle :")
            print(f"   python export_openvino.py --model {args.pytorch}")
            exit(1)
    
    print()
    
    # Lancer la comparaison
    compare_pytorch_openvino(args.pytorch, args.openvino, image_path, args.runs)


if __name__ == "__main__":
    main()
