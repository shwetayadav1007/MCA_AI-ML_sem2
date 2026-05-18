from typing import Dict, List

RISK_THRESHOLDS = {
    'Safe': 0.0,
    'Moderate': 40.0,
    'Critical': 60.0,
}


def calculate_risk(groundwater_level: float) -> str:
    if groundwater_level >= RISK_THRESHOLDS['Critical']:
        return 'Critical'
    if groundwater_level >= RISK_THRESHOLDS['Moderate']:
        return 'Moderate'
    return 'Safe'


def recommendation_for_risk(risk: str) -> str:
    if risk == 'Critical':
        return 'Reduce water usage immediately, deploy drought mitigation plans, and conserve rainfall.'
    if risk == 'Moderate':
        return 'Monitor water usage closely, improve irrigation efficiency and conserve resources.'
    return 'Continue regular water conservation and maintain groundwater recharge systems.'


def create_prediction_response(prediction: float) -> Dict[str, str]:
    risk = calculate_risk(prediction)
    return {
        'groundwater_level': round(prediction, 2),
        'risk_category': risk,
        'recommendation': recommendation_for_risk(risk),
    }
