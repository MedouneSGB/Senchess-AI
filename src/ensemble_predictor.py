#!/usr/bin/env python3
"""
Senchess AI - Ensemble Predictor
Combine les prédictions de tous les modèles disponibles pour un résultat optimal
"""

import yaml
from pathlib import Path
from ultralytics import YOLO
import numpy as np
import cv2
from typing import List, Dict, Tuple
import argparse


class SenchessEnsemble:
    """
    Système d'ensemble intelligent qui combine les prédictions de tous les modèles.
    Stratégies:
    - Voting: Utilise le modèle avec la meilleure confiance moyenne
    - Fusion: Combine toutes les détections avec NMS (Non-Maximum Suppression)
    - Auto: Choisit automatiquement le meilleur modèle selon le type d'image
    """
    
    def __init__(self, config_path='models/MODEL_CONFIG.yaml'):
        self.base_dir = Path(__file__).parent.parent
        self.config_path = self.base_dir / config_path
        self.models = self._load_models()
        
    def _load_models(self) -> Dict[str, YOLO]:
        """Charge tous les modèles disponibles"""
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        models = {}
        print("🔧 Chargement des modèles...")
        
        for model_name, model_info in config['models'].items():
            model_path = self.base_dir / model_info['path']
            if model_path.exists():
                models[model_name] = {
                    'model': YOLO(str(model_path)),
                    'info': model_info
                }
                print(f"  ✓ {model_name}: {model_info['full_name']}")
            else:
                print(f"  ⚠️  {model_name}: Modèle introuvable")
        
        # Ajouter Gear v1.1 s'il existe
        gear_v11_path = self.base_dir / 'models/senchess_gear_v1.1/weights/best.pt'
        if gear_v11_path.exists():
            models['senchess_gear_v1.1'] = {
                'model': YOLO(str(gear_v11_path)),
                'info': {
                    'full_name': 'Senchess Gear v1.1',
                    'version': '1.1',
                    'specialization': {
                        'type': '3D Physical Chess Pieces - Photos (Fine-tuned)',
                        'description': 'Version améliorée de Gear v1.0'
                    }
                }
            }
            print(f"  ✓ senchess_gear_v1.1: Senchess Gear v1.1 (Fine-tuned)")
        
        return models
    
    def predict_voting(self, image_path: str, conf_threshold: float = 0.25) -> Dict:
        """
        Stratégie VOTING: Utilise le modèle avec la meilleure confiance moyenne
        
        Args:
            image_path: Chemin vers l'image
            conf_threshold: Seuil de confiance minimal
            
        Returns:
            Dict avec les prédictions du meilleur modèle
        """
        print(f"\n🗳️  STRATÉGIE: Voting (Meilleur modèle)")
        print(f"📸 Image: {Path(image_path).name}")
        print("-" * 70)
        
        results_per_model = {}
        
        for model_name, model_data in self.models.items():
            model = model_data['model']
            results = model.predict(image_path, conf=conf_threshold, verbose=False)
            
            boxes = results[0].boxes
            if len(boxes) > 0:
                confidences = [box.conf.item() for box in boxes]
                avg_conf = np.mean(confidences)
                results_per_model[model_name] = {
                    'results': results,
                    'detections': len(boxes),
                    'avg_confidence': avg_conf,
                    'info': model_data['info']
                }
                print(f"  {model_data['info']['full_name']:25} | {len(boxes):2d} détections | Conf: {avg_conf*100:5.1f}%")
            else:
                print(f"  {model_data['info']['full_name']:25} | 0 détection")
        
        if not results_per_model:
            return {'best_model': None, 'detections': 0, 'strategy': 'voting'}
        
        # Sélectionner le meilleur modèle (confiance moyenne la plus élevée)
        best_model_name = max(results_per_model.keys(), 
                              key=lambda x: results_per_model[x]['avg_confidence'])
        best = results_per_model[best_model_name]
        
        print("\n" + "=" * 70)
        print(f"🏆 GAGNANT: {best['info']['full_name']}")
        print(f"   Détections: {best['detections']}")
        print(f"   Confiance moyenne: {best['avg_confidence']*100:.1f}%")
        print("=" * 70)
        
        return {
            'best_model': best_model_name,
            'model_info': best['info'],
            'results': best['results'],
            'detections': best['detections'],
            'avg_confidence': best['avg_confidence'],
            'all_results': results_per_model,
            'strategy': 'voting'
        }
    
    def predict_fusion(self, image_path: str, conf_threshold: float = 0.25, 
                       iou_threshold: float = 0.5) -> Dict:
        """
        Stratégie FUSION: Combine toutes les détections avec NMS
        
        Args:
            image_path: Chemin vers l'image
            conf_threshold: Seuil de confiance minimal
            iou_threshold: Seuil IoU pour NMS
            
        Returns:
            Dict avec les prédictions fusionnées
        """
        print(f"\n🔗 STRATÉGIE: Fusion (Combinaison NMS)")
        print(f"📸 Image: {Path(image_path).name}")
        print("-" * 70)
        
        all_boxes = []
        all_confidences = []
        all_class_ids = []
        
        for model_name, model_data in self.models.items():
            model = model_data['model']
            results = model.predict(image_path, conf=conf_threshold, verbose=False)
            
            boxes = results[0].boxes
            if len(boxes) > 0:
                for box in boxes:
                    xyxy = box.xyxy[0].cpu().numpy()
                    all_boxes.append(xyxy)
                    all_confidences.append(box.conf.item())
                    all_class_ids.append(int(box.cls.item()))
                
                print(f"  {model_data['info']['full_name']:25} | {len(boxes):2d} détections ajoutées")
        
        if not all_boxes:
            return {'detections': 0, 'strategy': 'fusion'}
        
        # Appliquer NMS pour fusionner les détections qui se chevauchent
        all_boxes = np.array(all_boxes)
        all_confidences = np.array(all_confidences)
        all_class_ids = np.array(all_class_ids)
        
        # Convertir au format NMS (x, y, w, h)
        boxes_xywh = all_boxes.copy()
        boxes_xywh[:, 2] = all_boxes[:, 2] - all_boxes[:, 0]  # width
        boxes_xywh[:, 3] = all_boxes[:, 3] - all_boxes[:, 1]  # height
        
        # Appliquer NMS par classe
        final_boxes = []
        final_confidences = []
        final_classes = []
        
        for class_id in np.unique(all_class_ids):
            mask = all_class_ids == class_id
            class_boxes = boxes_xywh[mask]
            class_confs = all_confidences[mask]
            
            # NMS avec OpenCV
            indices = cv2.dnn.NMSBoxes(
                class_boxes.tolist(),
                class_confs.tolist(),
                conf_threshold,
                iou_threshold
            )
            
            if len(indices) > 0:
                for idx in indices.flatten():
                    final_boxes.append(all_boxes[np.where(mask)[0][idx]])
                    final_confidences.append(class_confs[idx])
                    final_classes.append(class_id)
        
        print("\n" + "=" * 70)
        print(f"🔗 FUSION: {len(all_boxes)} détections → {len(final_boxes)} après NMS")
        print(f"   Confiance moyenne: {np.mean(final_confidences)*100:.1f}%")
        print("=" * 70)
        
        return {
            'boxes': final_boxes,
            'confidences': final_confidences,
            'classes': final_classes,
            'detections': len(final_boxes),
            'avg_confidence': np.mean(final_confidences) if final_confidences else 0,
            'strategy': 'fusion',
            'total_before_nms': len(all_boxes)
        }
    
    def predict_auto(self, image_path: str, conf_threshold: float = 0.25) -> Dict:
        """
        Stratégie AUTO: Choisit automatiquement le meilleur modèle
        Analyse l'image pour déterminer s'il s'agit d'un diagramme 2D ou d'une photo 3D
        
        Args:
            image_path: Chemin vers l'image
            conf_threshold: Seuil de confiance minimal
            
        Returns:
            Dict avec les prédictions du modèle optimal
        """
        print(f"\n🤖 STRATÉGIE: Auto (Sélection intelligente)")
        print(f"📸 Image: {Path(image_path).name}")
        print("-" * 70)
        
        # Analyser l'image
        img = cv2.imread(str(image_path))
        
        # Heuristique simple: images vectorielles/générées ont moins de bruit
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Analyser la saturation des couleurs
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        avg_saturation = np.mean(saturation)
        
        # Décision: diagramme 2D ou photo 3D
        is_2d_diagram = edge_density < 0.15 or avg_saturation > 100
        
        print(f"  📊 Analyse de l'image:")
        print(f"     Edge density: {edge_density:.4f}")
        print(f"     Saturation moy: {avg_saturation:.1f}")
        print(f"     Type détecté: {'📐 Diagramme 2D' if is_2d_diagram else '📷 Photo 3D'}")
        print()
        
        if is_2d_diagram:
            # Utiliser Haki pour diagrammes 2D
            preferred_models = ['senchess_haki_v1.0']
            print("  ✓ Sélection: Senchess Haki v1.0 (spécialisé diagrammes 2D)")
        else:
            # Utiliser Gear v1.1 ou v1.0 pour photos 3D
            if 'senchess_gear_v1.1' in self.models:
                preferred_models = ['senchess_gear_v1.1', 'senchess_gear_v1.0']
                print("  ✓ Sélection: Senchess Gear v1.1 (spécialisé photos 3D)")
            else:
                preferred_models = ['senchess_gear_v1.0']
                print("  ✓ Sélection: Senchess Gear v1.0 (spécialisé photos 3D)")
        
        # Tester les modèles préférés
        best_result = None
        best_conf = 0
        
        for model_name in preferred_models:
            if model_name in self.models:
                model_data = self.models[model_name]
                model = model_data['model']
                results = model.predict(image_path, conf=conf_threshold, verbose=False)
                
                boxes = results[0].boxes
                if len(boxes) > 0:
                    confidences = [box.conf.item() for box in boxes]
                    avg_conf = np.mean(confidences)
                    
                    print(f"     {model_data['info']['full_name']:25} | {len(boxes):2d} détections | Conf: {avg_conf*100:5.1f}%")
                    
                    if avg_conf > best_conf:
                        best_conf = avg_conf
                        best_result = {
                            'model_name': model_name,
                            'model_info': model_data['info'],
                            'results': results,
                            'detections': len(boxes),
                            'avg_confidence': avg_conf
                        }
        
        if not best_result:
            return {'best_model': None, 'detections': 0, 'strategy': 'auto'}
        
        print("\n" + "=" * 70)
        print(f"🤖 SÉLECTION AUTO: {best_result['model_info']['full_name']}")
        print(f"   Détections: {best_result['detections']}")
        print(f"   Confiance moyenne: {best_result['avg_confidence']*100:.1f}%")
        print("=" * 70)
        
        return {
            **best_result,
            'strategy': 'auto',
            'image_type': '2D Diagram' if is_2d_diagram else '3D Photo'
        }
    
    def predict(self, image_path: str, strategy: str = 'auto', 
                conf_threshold: float = 0.25, save: bool = False, 
                output_dir: str = None) -> Dict:
        """
        Prédiction avec la stratégie choisie
        
        Args:
            image_path: Chemin vers l'image
            strategy: 'auto', 'voting', ou 'fusion'
            conf_threshold: Seuil de confiance minimal
            save: Sauvegarder l'image avec les détections
            output_dir: Dossier de sortie
            
        Returns:
            Dict avec les résultats de la prédiction
        """
        if strategy == 'voting':
            result = self.predict_voting(image_path, conf_threshold)
        elif strategy == 'fusion':
            result = self.predict_fusion(image_path, conf_threshold)
        else:  # auto
            result = self.predict_auto(image_path, conf_threshold)
        
        # Sauvegarder l'image annotée si demandé
        if save and result.get('results'):
            if output_dir is None:
                output_dir = self.base_dir / f'runs/ensemble_{strategy}'
            else:
                output_dir = Path(output_dir)
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Sauvegarder avec les annotations
            annotated = result['results'][0].plot()
            output_path = output_dir / Path(image_path).name
            cv2.imwrite(str(output_path), annotated)
            print(f"\n💾 Image sauvegardée: {output_path}")
            result['output_path'] = str(output_path)
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description='Senchess AI Ensemble Predictor - Combine les prédictions de tous les modèles'
    )
    parser.add_argument('image', help='Chemin vers l\'image à analyser')
    parser.add_argument('--strategy', '-s', choices=['auto', 'voting', 'fusion'], 
                        default='auto', help='Stratégie de prédiction (défaut: auto)')
    parser.add_argument('--conf', '-c', type=float, default=0.25,
                        help='Seuil de confiance (défaut: 0.25)')
    parser.add_argument('--save', action='store_true',
                        help='Sauvegarder l\'image avec les détections')
    parser.add_argument('--output', '-o', help='Dossier de sortie')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("🎯 SENCHESS AI - ENSEMBLE PREDICTOR")
    print("=" * 70)
    
    # Créer l'ensemble
    ensemble = SenchessEnsemble()
    
    # Faire la prédiction
    result = ensemble.predict(
        args.image,
        strategy=args.strategy,
        conf_threshold=args.conf,
        save=args.save,
        output_dir=args.output
    )
    
    print("\n✅ Prédiction terminée!")


if __name__ == '__main__':
    main()
