/**
 * Service de reconnaissance d'échecs pour votre site web
 * Utilise l'API Senchess déployée sur Vercel
 */

// Types TypeScript
export interface ChessPositionAnalysis {
  fen: string;
  description: string;
  confidence: 'high' | 'medium' | 'low';
  detectedPieces: number;
  warnings: string[];
}

export interface ChessPiece {
  id: number;
  class: string;
  confidence: number;
  bbox: {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
    width: number;
    height: number;
  };
}

export interface ApiResponse {
  success: boolean;
  fen: string;
  pieces: ChessPiece[];
  confidence: number;
  detectedPieces: number;
  description: string;
  imageSize: {
    width: number;
    height: number;
  };
  warnings: string[];
}

/**
 * Configuration de l'API
 * Remplacez par votre URL Vercel après déploiement
 */
const API_CONFIG = {
  baseUrl: import.meta.env.VITE_SENCHESS_API_URL || 'http://localhost:5000',
  apiKey: import.meta.env.VITE_MODEL_API_KEY || '', // Optionnel
  timeout: 30000, // 30 secondes
};

/**
 * Analyse une image d'échiquier et retourne la position en FEN
 * 
 * @param imageUrl - URL de l'image ou Blob
 * @param confThreshold - Seuil de confiance (0-1)
 * @returns Position analysée avec le FEN et les détails
 */
export async function analyzeChessBoardImage(
  imageUrl: string | Blob,
  confThreshold: number = 0.25
): Promise<ChessPositionAnalysis> {
  try {
    // 1. Préparer l'image
    let imageBlob: Blob;
    
    if (typeof imageUrl === 'string') {
      // Si c'est une URL, télécharger l'image
      const response = await fetch(imageUrl);
      if (!response.ok) {
        throw new Error('Impossible de télécharger l\'image');
      }
      imageBlob = await response.blob();
    } else {
      // Si c'est déjà un Blob
      imageBlob = imageUrl;
    }
    
    // 2. Créer FormData
    const formData = new FormData();
    formData.append('image', imageBlob, 'chess.jpg');
    formData.append('conf', confThreshold.toString());
    
    // 3. Préparer les headers
    const headers: HeadersInit = {};
    
    if (API_CONFIG.apiKey) {
      headers['Authorization'] = `Bearer ${API_CONFIG.apiKey}`;
    }
    
    // 4. Appeler l'API
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);
    
    const response = await fetch(`${API_CONFIG.baseUrl}/predict`, {
      method: 'POST',
      body: formData,
      headers,
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({
        error: 'Erreur API',
        message: response.statusText
      }));
      throw new Error(error.message || 'Erreur lors de l\'analyse');
    }
    
    const result: ApiResponse = await response.json();
    
    // 5. Convertir la réponse au format attendu
    return {
      fen: result.fen,
      description: result.description,
      confidence: result.confidence > 0.9 ? 'high' : 
                  result.confidence > 0.7 ? 'medium' : 'low',
      detectedPieces: result.detectedPieces,
      warnings: result.warnings || []
    };
    
  } catch (error) {
    // Gestion des erreurs
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        throw new Error('Timeout : l\'analyse prend trop de temps');
      }
      throw new Error(`Échec de reconnaissance : ${error.message}`);
    }
    throw new Error('Échec de reconnaissance du modèle');
  }
}

/**
 * Vérifie que l'API est accessible et fonctionnelle
 * 
 * @returns Status de l'API
 */
export async function checkApiHealth(): Promise<{
  status: string;
  modelLoaded: boolean;
  message?: string;
}> {
  try {
    const response = await fetch(`${API_CONFIG.baseUrl}/health`, {
      method: 'GET',
    });
    
    if (!response.ok) {
      return {
        status: 'error',
        modelLoaded: false,
        message: 'API inaccessible'
      };
    }
    
    const data = await response.json();
    return {
      status: data.status,
      modelLoaded: data.model_loaded,
      message: data.status === 'healthy' ? 'API fonctionnelle' : 'Modèle non chargé'
    };
    
  } catch (error) {
    return {
      status: 'offline',
      modelLoaded: false,
      message: 'Impossible de contacter l\'API'
    };
  }
}

/**
 * Analyse une image depuis un fichier local (File input)
 * 
 * @param file - Fichier image depuis un input
 * @param confThreshold - Seuil de confiance
 * @returns Position analysée
 */
export async function analyzeChessBoardFile(
  file: File,
  confThreshold: number = 0.25
): Promise<ChessPositionAnalysis> {
  return analyzeChessBoardImage(file, confThreshold);
}

/**
 * Analyse une image depuis une image base64
 * 
 * @param base64Data - Données base64 de l'image
 * @param confThreshold - Seuil de confiance
 * @returns Position analysée
 */
export async function analyzeChessBoardBase64(
  base64Data: string,
  confThreshold: number = 0.25
): Promise<ChessPositionAnalysis> {
  try {
    // Créer FormData avec l'image base64
    const formData = new FormData();
    formData.append('image_base64', base64Data);
    formData.append('conf', confThreshold.toString());
    
    const headers: HeadersInit = {};
    if (API_CONFIG.apiKey) {
      headers['Authorization'] = `Bearer ${API_CONFIG.apiKey}`;
    }
    
    const response = await fetch(`${API_CONFIG.baseUrl}/predict`, {
      method: 'POST',
      body: formData,
      headers,
    });
    
    if (!response.ok) {
      throw new Error('Erreur lors de l\'analyse');
    }
    
    const result: ApiResponse = await response.json();
    
    return {
      fen: result.fen,
      description: result.description,
      confidence: result.confidence > 0.9 ? 'high' : 
                  result.confidence > 0.7 ? 'medium' : 'low',
      detectedPieces: result.detectedPieces,
      warnings: result.warnings || []
    };
    
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Échec de reconnaissance : ${error.message}`);
    }
    throw new Error('Échec de reconnaissance du modèle');
  }
}

/**
 * Exemple d'utilisation avec React
 */
export const ExampleReactComponent = `
import React, { useState } from 'react';
import { analyzeChessBoardFile, checkApiHealth } from './chessImageRecognition';

function ChessAnalyzer() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const analysis = await analyzeChessBoardFile(file, 0.25);
      setResult(analysis);
      console.log('Position FEN:', analysis.fen);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileUpload} />
      
      {loading && <p>Analyse en cours...</p>}
      {error && <p style={{color: 'red'}}>{error}</p>}
      
      {result && (
        <div>
          <p>FEN: {result.fen}</p>
          <p>Pièces détectées: {result.detectedPieces}</p>
          <p>Confiance: {result.confidence}</p>
        </div>
      )}
    </div>
  );
}
`;

export default {
  analyzeChessBoardImage,
  analyzeChessBoardFile,
  analyzeChessBoardBase64,
  checkApiHealth,
};
