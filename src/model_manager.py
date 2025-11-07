"""
Script utilitaire pour charger et utiliser les modèles Senchess AI
"""
import os
from pathlib import Path
from ultralytics import YOLO
import yaml

class SenchessModelManager:
    """Gestionnaire de modèles Senchess AI avec versioning"""
    
    def __init__(self, config_path="models/MODEL_CONFIG.yaml"):
        self.base_dir = Path(__file__).parent.parent
        self.config_path = self.base_dir / config_path
        self.config = self._load_config()
        self.models = {}
    
    def _load_config(self):
        """Charge la configuration des modèles"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def list_models(self):
        """Liste tous les modèles disponibles"""
        print("\n" + "="*60)
        print("🎯 MODÈLES SENCHESS AI DISPONIBLES")
        print("="*60)
        
        for name, info in self.config['models'].items():
            print(f"\n📦 {info['full_name']}")
            print(f"   mAP50: {info['metrics']['mAP50']}%")
            print(f"   Dataset: {info['training']['dataset']} ({info['training']['images']} images)")
            print(f"   Meilleur pour: {', '.join(info['best_for'][:2])}")
    
    def load_model(self, model_name):
        """
        Charge un modèle Senchess
        
        Args:
            model_name: 'haki' ou 'gear'
        
        Returns:
            YOLO model object
        """
        model_key = f"senchess_{model_name}"
        
        if model_key not in self.config['models']:
            raise ValueError(f"Modèle '{model_name}' non trouvé. Utilisez 'haki' ou 'gear'")
        
        model_info = self.config['models'][model_key]
        model_path = self.base_dir / model_info['path']
        
        if not model_path.exists():
            raise FileNotFoundError(f"Fichier modèle non trouvé : {model_path}")
        
        print(f"🔄 Chargement de {model_info['full_name']}...")
        print(f"   Performances: mAP50={model_info['metrics']['mAP50']}%")
        
        model = YOLO(str(model_path))
        self.models[model_name] = model
        
        return model
    
    def predict(self, model_name, image_path, conf=0.25, save=True):
        """
        Fait une prédiction avec un modèle Senchess
        
        Args:
            model_name: 'haki' ou 'gear'
            image_path: Chemin vers l'image
            conf: Seuil de confiance (0-1)
            save: Sauvegarder l'image annotée
        
        Returns:
            Results object
        """
        if model_name not in self.models:
            self.load_model(model_name)
        
        model = self.models[model_name]
        
        print(f"\n🎯 Prédiction avec {model_name.upper()}...")
        results = model.predict(
            source=image_path,
            conf=conf,
            save=save,
            project='predictions',
            name=f'senchess_{model_name}'
        )
        
        return results
    
    def compare_models(self, image_path, conf=0.25):
        """
        Compare les 2 modèles sur une même image
        
        Args:
            image_path: Chemin vers l'image
            conf: Seuil de confiance
        
        Returns:
            dict avec les résultats des 2 modèles
        """
        print("\n" + "="*60)
        print("⚖️  COMPARAISON HAKI vs GEAR")
        print("="*60)
        
        results = {}
        
        for model_name in ['haki', 'gear']:
            result = self.predict(model_name, image_path, conf, save=True)
            
            # Compter les détections
            detections = len(result[0].boxes)
            confidences = result[0].boxes.conf.cpu().numpy() if detections > 0 else []
            avg_conf = confidences.mean() if len(confidences) > 0 else 0
            
            results[model_name] = {
                'detections': detections,
                'avg_confidence': avg_conf,
                'result': result
            }
            
            print(f"\n{model_name.upper()}: {detections} détections (conf moy: {avg_conf:.2%})")
        
        return results
    
    def get_model_info(self, model_name):
        """Retourne les informations d'un modèle"""
        model_key = f"senchess_{model_name}"
        if model_key in self.config['models']:
            return self.config['models'][model_key]
        return None
    
    def recommend_model(self, use_case):
        """
        Recommande un modèle selon le cas d'usage
        
        Args:
            use_case: 'user_photos', 'generated_images', 'hybrid', 'universal'
        
        Returns:
            str: nom du modèle recommandé
        """
        strategies = self.config.get('usage_strategies', {})
        
        if use_case in strategies:
            strategy = strategies[use_case]
            model_path = strategy.get('recommended_model', '')
            
            # Extraire le nom du modèle
            if 'haki' in model_path:
                return 'haki'
            elif 'gear' in model_path:
                return 'gear'
        
        return 'haki'  # Par défaut


# Exemple d'utilisation
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestionnaire de modèles Senchess AI")
    parser.add_argument('--list', action='store_true', help="Liste les modèles disponibles")
    parser.add_argument('--model', type=str, choices=['haki', 'gear'], help="Nom du modèle")
    parser.add_argument('--image', type=str, help="Chemin vers l'image à analyser")
    parser.add_argument('--compare', action='store_true', help="Compare les 2 modèles")
    parser.add_argument('--conf', type=float, default=0.25, help="Seuil de confiance")
    
    args = parser.parse_args()
    
    manager = SenchessModelManager()
    
    if args.list:
        manager.list_models()
    
    elif args.image:
        if args.compare:
            manager.compare_models(args.image, args.conf)
        elif args.model:
            manager.predict(args.model, args.image, args.conf)
        else:
            print("❌ Spécifiez --model (haki/gear) ou --compare")
    
    else:
        print("Usage:")
        print("  python src/model_manager.py --list")
        print("  python src/model_manager.py --model haki --image imgTest/capture2.jpg")
        print("  python src/model_manager.py --compare --image imgTest/capture2.jpg")
