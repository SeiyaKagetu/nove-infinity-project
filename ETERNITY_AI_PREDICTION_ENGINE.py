#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETERNITY AI統合予測エンジン
LSTM予測と自律学習を統合した高度なAI意思決定システム
"""

import json
import os
from datetime import datetime
import numpy as np
from ETERNITY_AI_LSTM_PREDICTOR import ETERNITYAILSTMPredictor
from ETERNITY_AI_AUTONOMOUS_LEARNING import ETERNITYAIAutonomousLearning
from ETERNITY_AI_LEARNING_DATABASE import ETERNITYAILearningDB


class ETERNITYAIPredictionEngine:
    """統合予測エンジン - LSTM + 自律学習"""

    def __init__(self):
        self.predictor = ETERNITYAILSTMPredictor()
        self.learner = ETERNITYAIAutonomousLearning()
        self.learning_db = ETERNITYAILearningDB()
        self.db_path = "/home/seiya/.eternity_ai_learning"
        self.prediction_cache_path = os.path.join(self.db_path, "prediction_cache.json")

    def integrate_prediction_into_decision(self, pressure_index, historical_executions, current_thresholds):
        """予測を意思決定に統合

        Args:
            pressure_index: 現在の圧力指数
            historical_executions: 過去の実行データ
            current_thresholds: 現在の閾値

        Returns:
            {
                'base_decision': str,        # 従来のルールベース判定
                'predicted_decision': str,   # LSTM予測ベース判定
                'final_decision': str,       # 統合判定
                'confidence': float,
                'reasoning': str,
                'predicted_future_state': {...}
            }
        """

        # 1. 従来のルールベース判定
        base_decision = self._rule_based_decision(pressure_index, current_thresholds)

        # 2. LSTM予測を取得
        current_state = {
            'pressure_index': pressure_index,
            'memory_pct': 55,
            'cpu_pct': 40,
            'effectiveness_score': 5
        }

        prediction_result = self.learner.predict_optimal_action(current_state, historical_executions)
        predicted_decision = prediction_result['recommended_action']
        confidence = prediction_result['confidence']

        # 3. 予測精度を確認
        accuracy = self.learner.analyze_prediction_accuracy(historical_executions)
        prediction_reliability = accuracy.get('accuracy_percentage', 0) / 100.0

        # 4. 統合判定ロジック
        if prediction_reliability < 0.3:
            # 予測精度が低い場合はルールベースに従う
            final_decision = base_decision
            reasoning = f"予測精度が低いため ({prediction_reliability:.0%})、ルールベース判定を採用: {base_decision}"
            confidence = 0.7

        elif base_decision == predicted_decision:
            # 両方の判定が一致 → 確信度が高い
            final_decision = base_decision
            reasoning = f"ルールベース判定とLSTM予測が一致: {final_decision}"
            confidence = min(0.98, confidence + 0.1)

        elif self._is_more_aggressive_decision(predicted_decision, base_decision):
            # 予測がより積極的な場合 → 予測精度が高い場合のみ採用
            if confidence > 0.8 and prediction_reliability > 0.6:
                final_decision = predicted_decision
                reasoning = f"LSTM予測が信頼性高く、より積極的な最適化を推奨: {predicted_decision}"
            else:
                final_decision = base_decision
                reasoning = f"予測はより積極的だが、信頼性が不十分。ルールベースを採用: {base_decision}"

        else:
            # 予測がより保守的な場合 → 安全性を優先
            final_decision = base_decision
            reasoning = f"LSTM予測はより保守的。ルールベースの判定を採用: {base_decision}"

        result = {
            'base_decision': base_decision,
            'predicted_decision': predicted_decision,
            'final_decision': final_decision,
            'confidence': float(confidence),
            'reasoning': reasoning,
            'predicted_future_state': prediction_result['predicted_result_state'],
            'prediction_reliability': float(prediction_reliability),
            'detailed_predictions': prediction_result['detailed_predictions']
        }

        # キャッシュに保存
        self._cache_prediction(result)

        return result

    def continuous_learning_cycle(self):
        """継続的な学習サイクルを実行

        Returns:
            {
                'model_updated': bool,
                'thresholds_optimized': bool,
                'improvements': {...}
            }
        """

        executions = self.learning_db.get_recent_executions(count=100)

        if len(executions) < 5:
            return {
                'model_updated': False,
                'thresholds_optimized': False,
                'reason': 'insufficient_data',
                'executions_count': len(executions)
            }

        results = {
            'model_updated': False,
            'thresholds_optimized': False,
            'improvements': {}
        }

        # 1. LSTMモデルを再訓練
        print("🤖 LSTMモデルを再訓練中...")
        try:
            history = self.predictor.train(executions, epochs=50, batch_size=4)
            if history:
                results['model_updated'] = True
                results['improvements']['model_loss'] = float(history.history['loss'][-1])
                print(f"   ✅ モデル更新完了 (Loss: {history.history['loss'][-1]:.6f})")
        except Exception as e:
            print(f"   ⚠️ モデル更新失敗: {e}")

        # 2. 閾値を最適化
        print("🎯 閾値を最適化中...")
        current_thresholds = self.learning_db.get_ai_thresholds()

        optimization = self.learner.optimize_thresholds(executions, current_thresholds)

        if optimization['adjustments_made'] > 0:
            results['thresholds_optimized'] = True
            results['improvements']['threshold_adjustments'] = optimization['adjustments_made']
            results['improvements']['estimated_improvement'] = optimization['improvement_estimate']

            # 新しい閾値を保存
            self.learning_db.update_ai_thresholds(optimization['optimized_thresholds'])
            print(f"   ✅ 閾値最適化完了 ({optimization['adjustments_made']}個の調整)")

        # 3. 学習サイクルを記録
        learning_record = {
            'timestamp': datetime.now().isoformat(),
            'executions_analyzed': len(executions),
            'model_updated': results['model_updated'],
            'thresholds_optimized': results['thresholds_optimized'],
            'improvements': results['improvements']
        }

        self.learner.record_learning_cycle(learning_record)

        return results

    def _rule_based_decision(self, pressure_index, thresholds):
        """ルールベースの意思決定"""
        if pressure_index < thresholds.get('light_optimize_threshold', 30):
            return "NO_ACTION"
        elif pressure_index < thresholds.get('phase1_threshold', 50):
            return "LIGHT_OPTIMIZE"
        elif pressure_index < thresholds.get('phase1_2_threshold', 70):
            return "PHASE_1"
        elif pressure_index < thresholds.get('emergency_threshold', 90):
            return "PHASE_1_2"
        else:
            return "PHASE_1_4_EMERGENCY"

    def _is_more_aggressive_decision(self, decision1, decision2):
        """decision1がdecision2より積極的かどうか"""
        decision_order = {
            "NO_ACTION": 0,
            "LIGHT_OPTIMIZE": 1,
            "PHASE_1": 2,
            "PHASE_1_2": 3,
            "PHASE_1_4_EMERGENCY": 4
        }
        return decision_order.get(decision1, 0) > decision_order.get(decision2, 0)

    def _cache_prediction(self, result):
        """予測結果をキャッシュに保存"""
        try:
            # 既存キャッシュを読み込み
            if os.path.exists(self.prediction_cache_path):
                with open(self.prediction_cache_path, 'r') as f:
                    cache = json.load(f)
            else:
                cache = {'predictions': []}

            # 新しい予測を追加
            cache['predictions'].append(result)

            # 最新1000件に制限
            if len(cache['predictions']) > 1000:
                cache['predictions'] = cache['predictions'][-1000:]

            # キャッシュを保存
            with open(self.prediction_cache_path, 'w') as f:
                json.dump(cache, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"⚠️ 予測キャッシュ保存失敗: {e}")

    def generate_prediction_report(self):
        """予測レポートを生成"""
        executions = self.learning_db.get_recent_executions(count=50)

        if len(executions) == 0:
            return None

        accuracy = self.learner.analyze_prediction_accuracy(executions)

        report = {
            'timestamp': datetime.now().isoformat(),
            'prediction_metrics': {
                'mean_absolute_error': accuracy.get('mean_absolute_error', 0),
                'rmse': accuracy.get('rmse', 0),
                'accuracy_percentage': accuracy.get('accuracy_percentage', 0),
                'predictions_made': accuracy.get('prediction_count', 0)
            },
            'execution_statistics': {
                'total_executions': len(executions),
                'executions_analyzed': len(executions),
                'date_range': {
                    'earliest': executions[0].get('timestamp') if executions else None,
                    'latest': executions[-1].get('timestamp') if executions else None
                }
            },
            'decision_distribution': self.learner._analyze_decision_distribution(executions),
            'effectiveness_analysis': self.learner._analyze_optimization_effectiveness(executions),
            'failure_patterns': self.learner._detect_failure_patterns(executions)
        }

        return report


def main():
    """テスト実行"""
    print("=" * 80)
    print("ETERNITY AI統合予測エンジン - テスト実行")
    print("=" * 80)

    # 実行履歴を読み込み
    history_path = "/home/seiya/.eternity_ai_learning/execution_history.json"
    with open(history_path, 'r') as f:
        history_data = json.load(f)

    executions = history_data.get('executions', [])
    print(f"\n📊 読み込み実行数: {len(executions)}")

    # 統合予測エンジンを初期化
    engine = ETERNITYAIPredictionEngine()

    # 予測を統合した意思決定
    print("\n🤖 統合予測ベース意思決定:")
    current_pressure = 37.1
    current_thresholds = {
        'light_optimize_threshold': 30,
        'phase1_threshold': 50,
        'phase1_2_threshold': 70,
        'emergency_threshold': 90
    }

    integrated_decision = engine.integrate_prediction_into_decision(
        current_pressure,
        executions,
        current_thresholds
    )

    print(f"   現在の圧力指数: {current_pressure}/100")
    print(f"   基本判定: {integrated_decision['base_decision']}")
    print(f"   LSTM予測: {integrated_decision['predicted_decision']}")
    print(f"   最終判定: {integrated_decision['final_decision']}")
    print(f"   信頼度: {integrated_decision['confidence']:.0%}")
    print(f"   理由: {integrated_decision['reasoning']}")

    # 継続学習サイクル
    print("\n📚 継続学習サイクル:")
    learning_result = engine.continuous_learning_cycle()
    print(f"   モデル更新: {learning_result.get('model_updated', False)}")
    print(f"   閾値最適化: {learning_result.get('thresholds_optimized', False)}")

    # 予測レポート
    print("\n📈 予測レポート:")
    report = engine.generate_prediction_report()
    if report:
        print(f"   MAE: {report['prediction_metrics']['mean_absolute_error']:.2f}")
        print(f"   精度: {report['prediction_metrics']['accuracy_percentage']:.1f}%")
        print(f"   総実行数: {report['execution_statistics']['total_executions']}")

    print("\n" + "=" * 80)
    print("✅ 統合予測エンジンの初期化完了")
    print("=" * 80)


if __name__ == "__main__":
    main()
