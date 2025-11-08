"""
Script d'évaluation et de comparaison des modèles Senchess AI
"""
import argparse
from pathlib import Path
from ultralytics import YOLO
import yaml
import json
from datetime import datetime

class SenchessEvaluator:
    """Évaluateur de modèles Senchess AI"""
    
    def __init__(self, config_path="models/MODEL_CONFIG.yaml"):
        self.base_dir = Path(__file__).parent.parent
        self.config_path = self.base_dir / config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Charge la configuration des modèles"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def evaluate_model(self, model_name, dataset_yaml=None, detailed=False):
        """
        Évalue un modèle sur un dataset de test
        
        Args:
            model_name: 'haki' ou 'gear'
            dataset_yaml: Chemin vers le fichier data.yaml (optionnel)
            detailed: Afficher les métriques détaillées par classe
        
        Returns:
            dict: Métriques d'évaluation
        """
        model_key = f"senchess_{model_name}_v1.0"
        
        if model_key not in self.config['models']:
            raise ValueError(f"Modèle '{model_name}' non trouvé. Utilisez 'haki' ou 'gear'")
        
        model_info = self.config['models'][model_key]
        model_path = self.base_dir / model_info['path']
        
        # Déterminer le dataset à utiliser
        if dataset_yaml is None:
            # Utiliser le dataset d'entraînement du modèle
            if model_name == 'haki':
                dataset_yaml = self.base_dir / "data/chess_decoder_1000/data.yaml"
            else:  # gear
                dataset_yaml = self.base_dir / "data/chess_dataset.yaml"
        
        print("\n" + "="*70)
        print(f"📊 ÉVALUATION : {model_info['full_name']}")
        print("="*70)
        print(f"Modèle    : {model_path}")
        print(f"Dataset   : {dataset_yaml}")
        print(f"Entraîné  : {model_info['training']['images']} images")
        print(f"mAP50 ref : {model_info['metrics']['mAP50']}%")
        print("="*70 + "\n")
        
        # Charger et évaluer le modèle
        model = YOLO(str(model_path))
        
        print("🔄 Évaluation en cours...\n")
        metrics = model.val(data=str(dataset_yaml), verbose=detailed)
        
        # Extraire les métriques principales
        results = {
            'model': model_info['full_name'],
            'mAP50': float(metrics.box.map50) * 100,
            'mAP50-95': float(metrics.box.map) * 100,
            'precision': float(metrics.box.mp) * 100,
            'recall': float(metrics.box.mr) * 100,
            'timestamp': datetime.now().isoformat(),
            'dataset': str(dataset_yaml)
        }
        
        # Afficher les résultats
        print("\n" + "="*70)
        print("✅ RÉSULTATS D'ÉVALUATION")
        print("="*70)
        print(f"mAP50     : {results['mAP50']:.2f}%")
        print(f"mAP50-95  : {results['mAP50-95']:.2f}%")
        print(f"Precision : {results['precision']:.2f}%")
        print(f"Recall    : {results['recall']:.2f}%")
        print("="*70 + "\n")
        
        # Métriques détaillées par classe
        if detailed and hasattr(metrics.box, 'ap_class_index'):
            print("\n📊 Métriques par classe :")
            print("-" * 70)
            class_names = metrics.names
            for i, class_idx in enumerate(metrics.box.ap_class_index):
                class_name = class_names[int(class_idx)]
                ap50 = metrics.box.ap50[i] * 100
                print(f"  {class_name:20s} : mAP50 = {ap50:.2f}%")
            print("-" * 70 + "\n")
        
        return results
    
    def compare_models(self, dataset_yaml=None, save_report=True):
        """
        Compare les performances de Haki et Gear
        
        Args:
            dataset_yaml: Dataset de test (si None, utilise les datasets respectifs)
            save_report: Sauvegarder le rapport en JSON
        
        Returns:
            dict: Comparaison des modèles
        """
        print("\n" + "="*70)
        print("⚖️  COMPARAISON : SENCHESS HAKI vs SENCHESS GEAR")
        print("="*70 + "\n")
        
        results = {}
        
        # Évaluer Haki
        print("🥇 Modèle 1/2 : Senchess Haki v1.0")
        results['haki'] = self.evaluate_model('haki', dataset_yaml)
        
        print("\n" + "-"*70 + "\n")
        
        # Évaluer Gear
        print("🥈 Modèle 2/2 : Senchess Gear v1.0")
        results['gear'] = self.evaluate_model('gear', dataset_yaml)
        
        # Tableau comparatif
        print("\n" + "="*70)
        print("📊 TABLEAU COMPARATIF")
        print("="*70)
        print(f"{'Métrique':<20} {'Haki v1.0':>15} {'Gear v1.0':>15} {'Gagnant':>15}")
        print("-"*70)
        
        metrics_to_compare = ['mAP50', 'mAP50-95', 'precision', 'recall']
        
        for metric in metrics_to_compare:
            haki_val = results['haki'][metric]
            gear_val = results['gear'][metric]
            winner = "🥇 Haki" if haki_val > gear_val else "🥈 Gear" if gear_val > haki_val else "Égalité"
            print(f"{metric:<20} {haki_val:>14.2f}% {gear_val:>14.2f}% {winner:>15}")
        
        print("="*70 + "\n")
        
        # Recommandations
        print("💡 RECOMMANDATIONS D'USAGE :")
        print("-"*70)
        print("  Senchess Haki v1.0 (99.5% mAP50)")
        print("    ✅ Diagrammes d'échecs 2D générés")
        print("    ✅ Images Chess Decoder")
        print("    ✅ Graphiques stylisés\n")
        print("  Senchess Gear v1.0 (98.5% mAP50)")
        print("    ✅ Photos d'échiquiers physiques")
        print("    ✅ Images smartphone")
        print("    ✅ Conditions d'éclairage variées")
        print("-"*70 + "\n")
        
        # Sauvegarder le rapport
        if save_report:
            report_path = self.base_dir / "evaluation_report.json"
            with open(report_path, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"📄 Rapport sauvegardé : {report_path}\n")
        
        return results
    
    def benchmark(self, image_path, conf=0.25):
        """
        Benchmark de vitesse et précision sur une image
        
        Args:
            image_path: Chemin vers l'image de test
            conf: Seuil de confiance
        
        Returns:
            dict: Résultats du benchmark
        """
        import time
        
        print("\n" + "="*70)
        print(f"🏁 BENCHMARK : {Path(image_path).name}")
        print("="*70 + "\n")
        
        results = {}
        
        for model_name in ['haki', 'gear']:
            model_key = f"senchess_{model_name}_v1.0"
            model_info = self.config['models'][model_key]
            model_path = self.base_dir / model_info['path']
            
            print(f"⏱️  Test : {model_info['full_name']}")
            
            # Charger le modèle
            start_load = time.time()
            model = YOLO(str(model_path))
            load_time = time.time() - start_load
            
            # Inférence (10 itérations pour moyenne)
            times = []
            for i in range(10):
                start = time.time()
                result = model.predict(source=image_path, conf=conf, verbose=False)
                times.append(time.time() - start)
            
            avg_inference_time = sum(times) / len(times)
            detections = len(result[0].boxes)
            avg_conf = result[0].boxes.conf.cpu().numpy().mean() if detections > 0 else 0
            
            results[model_name] = {
                'load_time': load_time,
                'inference_time': avg_inference_time,
                'detections': detections,
                'avg_confidence': float(avg_conf)
            }
            
            print(f"  Chargement    : {load_time:.3f}s")
            print(f"  Inférence     : {avg_inference_time:.3f}s (moyenne sur 10)")
            print(f"  Détections    : {detections}")
            print(f"  Confiance moy : {avg_conf:.2%}\n")
        
        # Comparaison
        print("="*70)
        print("🏆 RÉSULTATS")
        print("="*70)
        faster = 'haki' if results['haki']['inference_time'] < results['gear']['inference_time'] else 'gear'
        more_accurate = 'haki' if results['haki']['avg_confidence'] > results['gear']['avg_confidence'] else 'gear'
        
        print(f"  Plus rapide      : {faster.upper()}")
        print(f"  Plus confiant    : {more_accurate.upper()}")
        print("="*70 + "\n")
        
        return results


def main():
    parser = argparse.ArgumentParser(description="Évaluation des modèles Senchess AI")
    parser.add_argument('--model', type=str, choices=['haki', 'gear'], 
                       help="Modèle à évaluer (haki ou gear)")
    parser.add_argument('--compare', action='store_true', 
                       help="Comparer les 2 modèles")
    parser.add_argument('--benchmark', type=str, 
                       help="Benchmarker sur une image spécifique")
    parser.add_argument('--dataset', type=str, 
                       help="Chemin vers data.yaml pour l'évaluation")
    parser.add_argument('--detailed', action='store_true', 
                       help="Afficher les métriques détaillées par classe")
    parser.add_argument('--conf', type=float, default=0.25, 
                       help="Seuil de confiance pour le benchmark")
    
    args = parser.parse_args()
    
    evaluator = SenchessEvaluator()
    
    if args.benchmark:
        evaluator.benchmark(args.benchmark, args.conf)
    
    elif args.compare:
        evaluator.compare_models(args.dataset)
    
    elif args.model:
        evaluator.evaluate_model(args.model, args.dataset, args.detailed)
    
    else:
        print("Usage:")
        print("  python src/evaluate.py --model haki")
        print("  python src/evaluate.py --compare")
        print("  python src/evaluate.py --benchmark imgTest/capture2.jpg")
        print("  python src/evaluate.py --model gear --detailed")


if __name__ == '__main__':
    main()
