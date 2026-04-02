"""
Router Prédictions
==================

Endpoint pour les prévisions de CA basées sur le modèle SARIMA.
"""

import pickle
from pathlib import Path
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Query

from statsmodels.tsa.statespace.sarimax import SARIMAX

# Création du router
router = APIRouter(
    prefix="/api/predict",
    tags=["Prédictions"]
)

# Chemin vers le modèle
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent  # api/app/routers -> OCR_Projet_9
print(f"Chemin projet : {PROJECT_ROOT}")
MODEL_PATH = PROJECT_ROOT / "data" / "models" / "saved" / "best_model_sarima.pkl"


@router.get("")
def get_predictions(
    horizon_days: int = Query(default=30, ge=1, le=90, description="Nombre de jours à prédire")
):
    """
    Génère des prévisions de CA pour les prochains jours.
    
    **Paramètres :**
    - horizon_days : Nombre de jours à prédire (1-90, défaut: 30)
    
    **Retourne :**
    - predictions : Liste des prévisions avec intervalle de confiance
    - model_info : Informations sur le modèle utilisé
    """
    
    # Vérifier que le modèle existe
    if not MODEL_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail=f"Modèle non disponible. Exécutez d'abord le notebook d'entraînement."
        )
    
    # Charger le modèle
    with open(MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    
    # Générer les prévisions avec intervalle de confiance
    forecast = model.get_forecast(steps=horizon_days)
    pred_mean = forecast.predicted_mean
    pred_ci = forecast.conf_int(alpha=0.05)  # IC 95%
    
    # Récupérer la dernière date d'entraînement
    last_date = model_data.get('last_date', datetime.now())
    
    # Construire la liste des prédictions
    predictions = []
    for i in range(horizon_days):
        pred_date = last_date + timedelta(days=i + 1)
        
        # Récupérer les valeurs (s'assurer qu'elles sont positives)
        ca_pred = max(0, float(pred_mean.iloc[i]))
        lower = max(0, float(pred_ci.iloc[i, 0]))
        upper = max(0, float(pred_ci.iloc[i, 1]))
        
        predictions.append({
            "date": pred_date.strftime('%Y-%m-%d'),
            "ca_predicted": round(ca_pred, 2),
            "lower": round(lower, 2),
            "upper": round(upper, 2)
        })
    
    # Récupérer les métriques
    metrics = model_data.get('metrics', {})
    
    return {
        "predictions": predictions,
        "model_info": {
            "type": "SARIMA",
            "order": str(model_data.get('order', '(1,0,1)')),
            "seasonal_order": str(model_data.get('seasonal_order', '(1,1,1,7)')),
            "last_training_date": str(last_date)[:10],
            "metrics": {
                "mae": metrics.get('MAE', metrics.get('mae', 'N/A')),
                "rmse": metrics.get('RMSE', metrics.get('rmse', 'N/A')),
                "mape": metrics.get('MAPE', metrics.get('mape', 'N/A'))
            }
        }
    }


@router.get("/info")
def get_model_info():
    """
    Retourne les informations du modèle sans générer de prédictions.
    
    Utile pour vérifier que le modèle est chargé et consulter ses métriques.
    """
    
    # Vérifier que le modèle existe
    if not MODEL_PATH.exists():
        return {
            "status": "error",
            "message": "Modèle non disponible",
            "file": str(MODEL_PATH)
        }
    
    # Charger le modèle
    with open(MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
    
    metrics = model_data.get('metrics', {})
    last_date = model_data.get('last_date', 'N/A')
    
    return {
        "status": "ok",
        "model": {
            "type": "SARIMA",
            "order": str(model_data.get('order', '(1,0,1)')),
            "seasonal_order": str(model_data.get('seasonal_order', '(1,1,1,7)')),
            "last_training_date": str(last_date)[:10] if last_date != 'N/A' else 'N/A'
        },
        "metrics": {
            "mae": metrics.get('MAE', metrics.get('mae', 'N/A')),
            "rmse": metrics.get('RMSE', metrics.get('rmse', 'N/A')),
            "mape": metrics.get('MAPE', metrics.get('mape', 'N/A'))
        },
        "file": str(MODEL_PATH)
    }