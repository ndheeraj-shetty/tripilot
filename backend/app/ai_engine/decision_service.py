import logging
from typing import Dict, Any, List
from uuid import UUID

from app.core.database import AsyncSessionLocal
from app.ai_engine.detection_service import DetectionService
from app.ai_engine.prediction_service import PredictionService
from app.ai_engine.recommendation_service import RecommendationService
from app.ai_engine.health_service import HealthScoreService
from app.ai_engine.trend_service import TrendAnalysisService
from app.domain.models.models import (
    AIDetection, AIPrediction, AIRecommendation, AIHealthScore, AIDecisionHistory, AITrend
)

logger = logging.getLogger(__name__)

class DecisionEngine:
    def __init__(self):
        self.detection_service = DetectionService()
        self.prediction_service = PredictionService()
        self.recommendation_service = RecommendationService()
        self.health_service = HealthScoreService()
        self.trend_service = TrendAnalysisService()

    async def evaluate_session_snapshot(
        self,
        session_id: UUID,
        current_epoch: int,
        current_step: int,
        total_steps: int,
        metrics_history: List[Dict[str, Any]],
        telemetry_history: List[Dict[str, Any]],
        logs_history: List[str]
    ) -> Dict[str, Any]:
        latest_telem = telemetry_history[-1] if telemetry_history else {}
        current_lr = metrics_history[-1].get("learning_rate", 0.001) if metrics_history else 0.001

        # 1. Detection Engine
        detections = self.detection_service.analyze(metrics_history, latest_telem, logs_history)

        # 2. Prediction Engine
        predictions = self.prediction_service.predict(
            current_step=current_step,
            total_steps=total_steps,
            metrics_history=metrics_history,
            telemetry_history=telemetry_history,
            detections=detections
        )

        # 3. Recommendation Engine
        recommendations = self.recommendation_service.generate(detections, latest_telem, current_lr)

        # 4. Health Score Engine
        health_score = self.health_service.calculate(detections, latest_telem, predictions.failure_probability)

        # 5. Trend Analysis
        trends = self.trend_service.analyze_trends(metrics_history)

        # 6. Save Decision Snapshot to PostgreSQL
        try:
            async with AsyncSessionLocal() as db:
                # Save Detections
                for d in detections:
                    db.add(AIDetection(
                        session_id=session_id,
                        detection_type=d.detection_type,
                        status=d.status,
                        severity=d.severity,
                        confidence=d.confidence,
                        reason=d.reason,
                        details=d.details
                    ))

                # Save Predictions
                db.add(AIPrediction(
                    session_id=session_id,
                    remaining_time_sec=predictions.remaining_time_sec,
                    failure_probability=predictions.failure_probability,
                    memory_growth_trend=predictions.memory_growth_trend,
                    speed_trend=predictions.speed_trend,
                    accuracy_trend=predictions.accuracy_trend,
                    loss_trend=predictions.loss_trend
                ))

                # Save Recommendations
                for r in recommendations:
                    db.add(AIRecommendation(
                        session_id=session_id,
                        title=r.title,
                        description=r.description,
                        priority=r.priority,
                        category=r.category,
                        reason=r.reason,
                        confidence=r.confidence,
                        expected_impact=r.expected_impact
                    ))

                # Save Health Score
                db.add(AIHealthScore(
                    session_id=session_id,
                    score=health_score.score,
                    category=health_score.category,
                    sub_scores=health_score.sub_scores
                ))

                # Save Decision History Timeline entry
                summary_text = f"Epoch {current_epoch} Step {current_step}: Health Score {health_score.score}/100 ({health_score.category}). {len(detections)} anomalies detected."
                db.add(AIDecisionHistory(
                    session_id=session_id,
                    epoch=current_epoch,
                    step=current_step,
                    health_score=health_score.score,
                    summary=summary_text,
                    detections_summary=[d.model_dump() for d in detections],
                    recommendations_summary=[r.model_dump() for r in recommendations]
                ))

                # Save Trends
                for t in trends:
                    db.add(AITrend(
                        session_id=session_id,
                        metric_type=t.metric_type,
                        moving_average_5=t.moving_average_5,
                        moving_average_20=t.moving_average_20,
                        slope=t.slope,
                        direction=t.direction
                    ))

                await db.commit()
        except Exception as e:
            logger.error(f"Error persisting AI decision snapshot for session {session_id}: {e}")

        return {
            "health_score": health_score.model_dump(),
            "detections": [d.model_dump() for d in detections],
            "predictions": predictions.model_dump(),
            "recommendations": [r.model_dump() for r in recommendations],
            "trends": [t.model_dump() for t in trends]
        }

decision_engine = DecisionEngine()
