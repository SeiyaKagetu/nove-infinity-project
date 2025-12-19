#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETERNITY AI自律学習エンジン
LSTMを使用した予測ベースの閾値最適化と自動改善
"""

import json
import os
from datetime import datetime, timedelta
import numpy as np
from ETERNITY_AI_LSTM_PREDICTOR import ETERNITYAILSTMPredictor


class ETERNITYAIAutonomousLearning:
    """自律学習エンジン"""

    def __init__(self):
        self.db_path = "/home/seiya/.eternity_ai_learning"
        self.learning_log_path = os.path.join(self.db_path, "autonomous_learning.json")
        self.predictor = ETERNITYAILSTMPredictor()
        self.learning_data = self._load_learning_data()

    def _load_learning_data(self):
        """学習データを読み込み"""
        if os.path.exists(self.learning_log_path):
            with open(self.learning_log_path, 'r') as f:
                return json.load(f)
        return {
            "learning_cycles": [],
            "model_improvements": [],
            "threshold_adjustments": [],
            "prediction_accuracy": [],
            "total_learning_time_hours": 0,
            "model_version": 1
        }

    def _save_learning_data(self):
        """学習データを保存"""
        with open(self.learning_log_path, 'w') as f:
            json.dump(self.learning_data, f, indent=2, ensure_ascii=False)

    def analyze_prediction_accuracy(self, historical_executions):
        """予測精度を分析

        Args:
            historical_executions: 過去の実行データ

        Returns:
            {
                'mean_absolute_error': float,
                'rmse': float,
                'accuracy_percentage': float,
                'prediction_count': int
            }
        """
        if len(historical_executions) < 6:
            return {
                'mean_absolute_error': 0,
                'rmse': 0,
                'accuracy_percentage': 0,
                'prediction_count': 0,
                'status': 'insufficient_data'
            }

        # 特徴を抽出
        features = self.predictor.extract_features(historical_executions)

        # 複数ステップの予測精度を評価
        errors = []

        for i in range(3, len(features)):
            # 過去3ステップから現在を予測
            past_features = features[max(0, i-3):i]

            if len(past_features) >= 3:
                predicted = self.predictor.predict_pressure(past_features, steps_ahead=1)
                actual = features[i, 0]  # 実際の圧力

                if len(predicted) > 0:
                    error = abs(predicted[0] - actual)
                    errors.append(error)

        if len(errors) == 0:
            return {
                'mean_absolute_error': 0,
                'rmse': 0,
                'accuracy_percentage': 0,
                'prediction_count': 0,
                'status': 'no_predictions_made'
            }

        mae = np.mean(errors)
        rmse = np.sqrt(np.mean(np.array(errors) ** 2))

        # 精度を計算（誤差が小さいほど高精度）
        accuracy = max(0, 100 - mae)  # MAE < 100の場合のみ正の精度

        result = {
            'mean_absolute_error': float(mae),
            'rmse': float(rmse),
            'accuracy_percentage': float(accuracy),
            'prediction_count': len(errors),
            'status': 'success'
        }

        return result

    def optimize_thresholds(self, historical_executions, current_thresholds):
        """実行履歴に基づいて閾値を最適化

        Args:
            historical_executions: 過去の実行データ
            current_thresholds: 現在の閾値

        Returns:
            {
                'optimized_thresholds': {...},
                'adjustments_made': int,
                'improvement_estimate': float
            }
        """
        if len(historical_executions) < 2:
            return {
                'optimized_thresholds': current_thresholds,
                'adjustments_made': 0,
                'improvement_estimate': 0
            }
        optimized = current_thresholds.copy()
        adjustments_made = 0

        # 1. 決定分布を分析
        decision_dist = self._analyze_decision_distribution(historical_executions)

        # LIGHT_OPTIMIZE が多い場合 → 閾値を下げる（より早期に最適化）
        if decision_dist.get('light_optimize_ratio', 0) > 0.6:
            optimized['light_optimize_threshold'] = max(20, current_thresholds.get('light_optimize_threshold', 30) - 5)
            adjustments_made += 1
            print(f"   📊 LIGHT_OPTIMIZE が多いため、閾値を引き下げ: {current_thresholds.get('light_optimize_threshold', 30)} → {optimized['light_optimize_threshold']}")

        # 2. 効果分析
        effectiveness = self._analyze_optimization_effectiveness(historical_executions)

        if effectiveness.get('average_effectiveness', 0) > 6.0:
            # 効果的な最適化が多い場合 → より積極的に実行
            optimized['phase1_threshold'] = max(40, current_thresholds.get('phase1_threshold', 50) - 5)
            adjustments_made += 1
            print(f"   ✅ 最適化が効果的なため、Phase 1閾値を引き下げ: {current_thresholds.get('phase1_threshold', 50)} → {optimized['phase1_threshold']}")

        if effectiveness.get('average_effectiveness', 0) < 3.0:
            # 効果が薄い場合 → より保守的に実行
            optimized['phase1_threshold'] = min(70, current_thresholds.get('phase1_threshold', 50) + 5)
            adjustments_made += 1
            print(f"   ⚠️ 最適化の効果が低いため、Phase 1閾値を引き上げ: {current_thresholds.get('phase1_threshold', 50)} → {optimized['phase1_threshold']}")

        # 3. 失敗パターンの検出
        failures = self._detect_failure_patterns(historical_executions)
        if failures.get('cpu_increase_events', 0) > 2:
            # CPU が増加した場合 → CPU集約的な最適化を回避
            optimized['avoid_cpu_optimization'] = True
            adjustments_made += 1
            print(f"   🔴 CPU増加イベント検出: CPU最適化を回避")

        improvement_estimate = self._estimate_improvement(effectiveness, failures)

        return {
            'optimized_thresholds': optimized,
            'adjustments_made': adjustments_made,
            'improvement_estimate': improvement_estimate
        }

    def predict_optimal_action(self, current_state, historical_executions):
        """現在の状態から最適なアクションを予測

        Args:
            current_state: {pressure_index, memory_pct, cpu_pct, process_count}
            historical_executions: 過去の実行データ

        Returns:
            {
                'recommended_action': str,
                'confidence': float,
                'predicted_effectiveness': float,
                'predicted_result_state': {...}
            }
        """
        # 現在の状態から将来の圧力指数を予測
        features = self.predictor.extract_features(historical_executions)

        # 最新の状態を追加
        current_feature = np.array([[
            current_state.get('pressure_index', 50),
            current_state.get('memory_pct', 50),
            current_state.get('cpu_pct', 30),
            current_state.get('effectiveness_score', 0)
        ]])

        if len(features) > 0:
            features = np.vstack([features, current_feature])
        else:
            features = current_feature

        predicted_pressures = self.predictor.predict_pressure(features, steps_ahead=3)

        # 予測に基づいてアクションを決定
        avg_predicted_pressure = np.mean(predicted_pressures)

        if avg_predicted_pressure < 30:
            recommended_action = "NO_ACTION"
            confidence = 0.95
            predicted_effectiveness = 0
        elif avg_predicted_pressure < 50:
            recommended_action = "LIGHT_OPTIMIZE"
            confidence = 0.85
            predicted_effectiveness = 4.0
        elif avg_predicted_pressure < 70:
            recommended_action = "PHASE_1"
            confidence = 0.80
            predicted_effectiveness = 6.0
        elif avg_predicted_pressure < 90:
            recommended_action = "PHASE_1_2"
            confidence = 0.75
            predicted_effectiveness = 8.0
        else:
            recommended_action = "PHASE_1_4_EMERGENCY"
            confidence = 0.90
            predicted_effectiveness = 10.0

        predicted_result_state = {
            'predicted_pressure_index': float(avg_predicted_pressure),
            'predicted_memory_reduction_mb': float(predicted_effectiveness * 100),
            'predicted_cpu_improvement_pct': float(predicted_effectiveness / 2),
            'steps_ahead': 3
        }

        return {
            'recommended_action': recommended_action,
            'confidence': confidence,
            'predicted_effectiveness': predicted_effectiveness,
            'predicted_result_state': predicted_result_state,
            'detailed_predictions': predicted_pressures
        }

    def _analyze_decision_distribution(self, executions):
        """決定分布を分析"""
        if len(executions) == 0:
            return {}

        decisions = [e.get('ai_decision', 'UNKNOWN') for e in executions]
        total = len(decisions)

        return {
            'no_action_ratio': decisions.count('NO_ACTION') / total if total > 0 else 0,
            'light_optimize_ratio': decisions.count('LIGHT_OPTIMIZE') / total if total > 0 else 0,
            'phase1_ratio': decisions.count('PHASE_1') / total if total > 0 else 0,
            'phase1_2_ratio': decisions.count('PHASE_1_2') / total if total > 0 else 0,
            'emergency_ratio': decisions.count('PHASE_1_4_EMERGENCY') / total if total > 0 else 0,
            'total_count': total
        }

    def _analyze_optimization_effectiveness(self, executions):
        """最適化の効果を分析"""
        if len(executions) == 0:
            return {'average_effectiveness': 0, 'total_memory_freed': 0}

        effectiveness_scores = []
        memory_freed_list = []

        for exec_item in executions:
            eff = exec_item.get('effectiveness', {}).get('effectiveness_score', 0)
            mem = exec_item.get('effectiveness', {}).get('memory_improvement_mb', 0)

            if eff > 0:
                effectiveness_scores.append(eff)
            if mem > 0:
                memory_freed_list.append(mem)

        return {
            'average_effectiveness': np.mean(effectiveness_scores) if len(effectiveness_scores) > 0 else 0,
            'max_effectiveness': max(effectiveness_scores) if len(effectiveness_scores) > 0 else 0,
            'total_memory_freed': sum(memory_freed_list),
            'sample_count': len(effectiveness_scores)
        }

    def _detect_failure_patterns(self, executions):
        """失敗パターンを検出"""
        failures = {
            'cpu_increase_events': 0,
            'memory_increase_events': 0,
            'effectiveness_zero_events': 0,
            'total_events': 0
        }

        for i in range(1, len(executions)):
            curr = executions[i]
            prev = executions[i - 1]

            curr_cpu = curr.get('metrics_after', {}).get('cpu_pct', 0)
            prev_cpu = prev.get('metrics_after', {}).get('cpu_pct', 0)

            curr_mem = curr.get('metrics_after', {}).get('memory_used_gb', 0)
            prev_mem = prev.get('metrics_after', {}).get('memory_used_gb', 0)

            if curr_cpu > prev_cpu:
                failures['cpu_increase_events'] += 1
                failures['total_events'] += 1

            if curr_mem > prev_mem:
                failures['memory_increase_events'] += 1
                failures['total_events'] += 1

            eff = curr.get('effectiveness', {}).get('effectiveness_score', 0)
            if eff == 0:
                failures['effectiveness_zero_events'] += 1
                failures['total_events'] += 1

        return failures

    def _estimate_improvement(self, effectiveness, failures):
        """改善の見積もり"""
        if effectiveness['sample_count'] == 0:
            return 0

        avg_eff = effectiveness['average_effectiveness']
        failure_ratio = failures['total_events'] / max(1, len(failures))

        improvement = (avg_eff * 10) - (failure_ratio * 20)
        return max(0, float(improvement))

    def record_learning_cycle(self, cycle_data):
        """学習サイクルを記録"""
        cycle_record = {
            'timestamp': datetime.now().isoformat(),
            'cycle_number': len(self.learning_data['learning_cycles']) + 1,
            'data': cycle_data
        }

        self.learning_data['learning_cycles'].append(cycle_record)
        self._save_learning_data()

        print(f"✅ 学習サイクル #{cycle_record['cycle_number']} を記録")


def main():
    """テスト実行"""
    print("=" * 80)
    print("ETERNITY AI自律学習エンジン - テスト実行")
    print("=" * 80)

    # 実行履歴を読み込み
    history_path = "/home/seiya/.eternity_ai_learning/execution_history.json"
    with open(history_path, 'r') as f:
        history_data = json.load(f)

    executions = history_data.get('executions', [])
    print(f"\n📊 読み込み実行数: {len(executions)}")

    # 自律学習エンジンを初期化
    learner = ETERNITYAIAutonomousLearning()

    # 予測精度を分析
    print("\n📈 予測精度を分析中...")
    accuracy = learner.analyze_prediction_accuracy(executions)
    print(f"   平均誤差 (MAE): {accuracy.get('mean_absolute_error', 0):.2f}")
    print(f"   二乗平均平方根誤差 (RMSE): {accuracy.get('rmse', 0):.2f}")
    print(f"   精度: {accuracy.get('accuracy_percentage', 0):.1f}%")

    # 閾値を最適化
    print("\n🎯 閾値を最適化中...")
    current_thresholds = {
        'light_optimize_threshold': 30,
        'phase1_threshold': 50,
        'phase1_2_threshold': 70,
        'emergency_threshold': 90
    }

    optimization = learner.optimize_thresholds(executions, current_thresholds)
    print(f"   実施した調整数: {optimization['adjustments_made']}")
    print(f"   見積もられた改善: {optimization['improvement_estimate']:.2f}%")

    # 最適なアクションを予測
    print("\n🔮 最適なアクションを予測中...")
    current_state = {
        'pressure_index': 37,
        'memory_pct': 55,
        'cpu_pct': 41,
        'effectiveness_score': 5
    }

    prediction = learner.predict_optimal_action(current_state, executions)
    print(f"   推奨アクション: {prediction['recommended_action']}")
    print(f"   信頼度: {prediction['confidence']:.0%}")
    print(f"   予測効果: {prediction['predicted_effectiveness']:.1f}")
    print(f"   予測される圧力指数の推移: {[f'{p:.1f}' for p in prediction['detailed_predictions']]}")

    print("\n" + "=" * 80)
    print("✅ 自律学習エンジンの初期化完了")
    print("=" * 80)


if __name__ == "__main__":
    main()
