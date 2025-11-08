"""
Modèle Ensemble : Combine Ultimate et Haki pour la meilleure détection
- Ultimate pour la détection globale (plus de pièces)
- Haki pour les pièces stratégiques (King, Queen, Rook, Bishop)
"""

from pathlib import Path
from ultralytics import YOLO
import cv2

class EnsembleChessDetector:
    """Combine les forces de Ultimate et Haki"""
    
    def __init__(self):
        """Charge les deux modèles"""
        print("🔄 Chargement des modèles...")
        
        # Pièces stratégiques pour Haki (meilleure précision)
        self.strategic_pieces = [
            'king', 'queen', 'rook', 'bishop',
            'black-king', 'black-queen', 'black-rook', 'black-bishop',
            'white-king', 'white-queen', 'white-rook', 'white-bishop'
        ]
        
        # Charger Ultimate (détection globale)
        ultimate_path = Path("models/senchess_ultimate_v1.0_quick/weights/best.pt")
        self.model_ultimate = YOLO(str(ultimate_path))
        print("✅ Ultimate chargé (détection globale)")
        
        # Charger Haki (pièces stratégiques)
        haki_path = Path("models/senchess_haki_v1.0/weights/best.pt")
        self.model_haki = YOLO(str(haki_path))
        print("✅ Haki chargé (pièces stratégiques)")
        
    def predict(self, image_path, conf=0.25, save=True, save_dir="predictions/ensemble"):
        """
        Prédiction intelligente combinant les deux modèles
        
        Args:
            image_path: Chemin vers l'image
            conf: Seuil de confiance
            save: Sauvegarder les résultats annotés
            save_dir: Dossier de sauvegarde
        
        Returns:
            dict avec les résultats combinés
        """
        image_path = Path(image_path)
        print(f"\n🎯 Analyse de {image_path.name}...")
        
        # 1. Détection Ultimate (toutes les pièces)
        results_ultimate = self.model_ultimate.predict(
            source=str(image_path),
            conf=conf,
            save=False,
            verbose=False
        )[0]
        
        # 2. Détection Haki (pièces stratégiques seulement)
        results_haki = self.model_haki.predict(
            source=str(image_path),
            conf=conf,
            save=False,
            verbose=False
        )[0]
        
        # 3. Combiner intelligemment
        final_boxes = []
        final_classes = []
        final_confs = []
        
        # Extraire les détections Haki (pièces stratégiques)
        haki_boxes = []
        if len(results_haki.boxes) > 0:
            for i, box in enumerate(results_haki.boxes):
                cls_id = int(box.cls[0])
                class_name = results_haki.names[cls_id]
                
                if any(piece in class_name.lower() for piece in ['king', 'queen', 'rook', 'bishop']):
                    haki_boxes.append({
                        'box': box.xyxy[0].cpu().numpy(),
                        'class': class_name,
                        'conf': float(box.conf[0]),
                        'cls_id': cls_id
                    })
        
        print(f"  🔴 Haki: {len(haki_boxes)} pièces stratégiques détectées")
        
        # Extraire les détections Ultimate
        ultimate_boxes = []
        if len(results_ultimate.boxes) > 0:
            for i, box in enumerate(results_ultimate.boxes):
                cls_id = int(box.cls[0])
                class_name = results_ultimate.names[cls_id]
                ultimate_boxes.append({
                    'box': box.xyxy[0].cpu().numpy(),
                    'class': class_name,
                    'conf': float(box.conf[0]),
                    'cls_id': cls_id
                })
        
        print(f"  🌟 Ultimate: {len(ultimate_boxes)} pièces détectées")
        
        # 4. Stratégie de fusion
        used_indices = set()
        
        # Priorité : Utiliser Haki pour les pièces stratégiques
        for haki_det in haki_boxes:
            final_boxes.append(haki_det['box'])
            final_classes.append(haki_det['class'])
            final_confs.append(haki_det['conf'])
            
            # Marquer les détections Ultimate qui se chevauchent
            for i, ultimate_det in enumerate(ultimate_boxes):
                if self._iou(haki_det['box'], ultimate_det['box']) > 0.5:
                    used_indices.add(i)
        
        # Ajouter les détections Ultimate non-stratégiques et non-chevauchantes
        for i, ultimate_det in enumerate(ultimate_boxes):
            if i not in used_indices:
                is_strategic = any(piece in ultimate_det['class'].lower() 
                                 for piece in ['king', 'queen', 'rook', 'bishop'])
                
                # Pour les pièces non-stratégiques, utiliser Ultimate
                if not is_strategic:
                    final_boxes.append(ultimate_det['box'])
                    final_classes.append(ultimate_det['class'])
                    final_confs.append(ultimate_det['conf'])
                # Pour les stratégiques, garder Ultimate si pas de Haki
                elif len([h for h in haki_boxes if self._iou(h['box'], ultimate_det['box']) > 0.3]) == 0:
                    final_boxes.append(ultimate_det['box'])
                    final_classes.append(ultimate_det['class'])
                    final_confs.append(ultimate_det['conf'])
        
        print(f"  🏆 Ensemble: {len(final_boxes)} pièces au total")
        
        # 5. Calculer les statistiques
        strategic_count = sum(1 for cls in final_classes 
                            if any(piece in cls.lower() for piece in ['king', 'queen', 'rook', 'bishop']))
        avg_conf = sum(final_confs) / len(final_confs) if final_confs else 0
        
        print(f"     → {strategic_count} pièces stratégiques (Haki)")
        print(f"     → {len(final_boxes) - strategic_count} autres pièces (Ultimate)")
        print(f"     → Confiance moyenne: {avg_conf:.1f}%")
        
        # 6. Sauvegarder l'image annotée
        if save and final_boxes:
            img = cv2.imread(str(image_path))
            
            for box, cls_name, conf in zip(final_boxes, final_classes, final_confs):
                x1, y1, x2, y2 = map(int, box)
                
                # Couleur selon le modèle source
                is_strategic = any(piece in cls_name.lower() 
                                 for piece in ['king', 'queen', 'rook', 'bishop'])
                color = (0, 0, 255) if is_strategic else (0, 255, 0)  # Rouge=Haki, Vert=Ultimate
                
                # Rectangle
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                
                # Label court (wKing, bQueen, etc.)
                short_name = self._get_short_name(cls_name)
                label = f"{short_name} {conf:.2f}"
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(img, (x1, y1 - 22), (x1 + w, y1), color, -1)
                cv2.putText(img, label, (x1, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Sauvegarder
            save_path = Path(save_dir) / image_path.name
            save_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(save_path), img)
            print(f"  💾 Sauvegardé: {save_path}")
        
        return {
            'total_detections': len(final_boxes),
            'strategic_pieces': strategic_count,
            'other_pieces': len(final_boxes) - strategic_count,
            'avg_confidence': avg_conf,
            'classes': final_classes,
            'confidences': final_confs
        }
    
    def _iou(self, box1, box2):
        """Calcule l'Intersection over Union entre deux boxes"""
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2
        
        # Intersection
        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)
        
        inter_area = max(0, inter_x_max - inter_x_min) * max(0, inter_y_max - inter_y_min)
        
        # Union
        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0
    
    def _get_short_name(self, class_name):
        """Convertit le nom de classe en notation courte (wK, bQ, etc.)"""
        # Mapping des noms longs vers notation ultra-courte
        mapping = {
            'white-king': 'wK',
            'white-queen': 'wQ',
            'white-rook': 'wR',
            'white-bishop': 'wB',
            'white-knight': 'wN',
            'white-pawn': 'wP',
            'black-king': 'bK',
            'black-queen': 'bQ',
            'black-rook': 'bR',
            'black-bishop': 'bB',
            'black-knight': 'bN',
            'black-pawn': 'bP',
            # Variantes
            'king': 'K',
            'queen': 'Q',
            'rook': 'R',
            'bishop': 'B',
            'knight': 'N',
            'pawn': 'P'
        }
        return mapping.get(class_name.lower(), class_name)


def test_ensemble():
    """Test le modèle ensemble sur les images de test"""
    print("\n" + "="*70)
    print("🏆 MODÈLE ENSEMBLE : ULTIMATE + HAKI")
    print("="*70)
    print("\nStratégie:")
    print("  🔴 Haki → King, Queen, Rook, Bishop (haute précision)")
    print("  🌟 Ultimate → Autres pièces (couverture maximale)")
    print("="*70 + "\n")
    
    # Créer le détecteur ensemble
    detector = EnsembleChessDetector()
    
    # Tester sur les images
    test_images = list(Path("examples/imgTest").glob("*.png"))
    
    if not test_images:
        print("❌ Aucune image trouvée dans examples/imgTest/")
        return
    
    results_summary = []
    for img_path in sorted(test_images):
        result = detector.predict(img_path, conf=0.25, save=True)
        results_summary.append(result)
    
    # Résumé final
    print("\n" + "="*70)
    print("📊 RÉSUMÉ ENSEMBLE")
    print("="*70)
    
    if not results_summary:
        print("\n❌ Aucun résultat à afficher")
        return
    
    total_det = sum(r['total_detections'] for r in results_summary)
    total_strategic = sum(r['strategic_pieces'] for r in results_summary)
    total_other = sum(r['other_pieces'] for r in results_summary)
    avg_conf = sum(r['avg_confidence'] for r in results_summary) / len(results_summary)
    
    print(f"\n🎯 Total détections: {total_det}")
    print(f"   🔴 Pièces stratégiques (Haki): {total_strategic}")
    print(f"   🌟 Autres pièces (Ultimate): {total_other}")
    print(f"   📈 Confiance moyenne: {avg_conf:.1f}%")
    print(f"\n💡 Ratio: {total_strategic}/{total_det} pièces stratégiques ({100*total_strategic/total_det:.1f}%)")
    print("\n✅ Images annotées sauvegardées dans: predictions/ensemble/")
    print("   Rouge = Haki (stratégique), Vert = Ultimate (autres)\n")


if __name__ == '__main__':
    test_ensemble()
