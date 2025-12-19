#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETERNITY AI LSTM統合学習エージェント
すべてのAIコンポーネントを統合して自律的に学習・最適化
"""

import json
import os
import sys
from datetime import datetime, timedelta
import subprocess

from ETERNITY_AI_CORE_ENGINE import ETERNITYAICore
from ETERNITY_AI_LEARNING_DATABASE import ETERNITYAILearningDB
from ETERNITY_AI_LSTM_PREDICTOR import ETERNITYAILSTMPredictor
from ETERNITY_AI_AUTONOMOUS_LEARNING import ETERNITYAIAutonomousLearning
from ETERNITY_AI_PREDICTION_ENGINE import ETERNITYAIPredictionEngine


class ETERNITYAILSTMLearningAgent:
    """LSTM統合学習エージェント"""

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.core_engine = ETERNITYAICore()
        self.learning_db = ETERNITYAILearningDB()
        self.lstm_predictor = ETERNITYAILSTMPredictor()
        self.autonomous_learner = ETERNITYAIAutonomousLearning()
        self.prediction_engine = ETERNITYAIPredictionEngine()

        self.db_path = "/home/seiya/.eternity_ai_learning"
        self.agent_log_path = os.path.join(self.db_path, "lstm_learning_agent.json")
        self.agent_log = self._load_agent_log()

    def _load_agent_log(self):
        """エージェントログを読み込み"""
        if os.path.exists(self.agent_log_path):
            with open(self.agent_log_path, 'r') as f:
                return json.load(f)
        return {
            'agent_version': '1.0.0',
            'initialized': datetime.now().isoformat(),
            'sessions': [],
            'total_decisions': 0,
            'learning_cycles': 0
        }

    def _save_agent_log(self):
        """エージェントログを保存"""
        with open(self.agent_log_path, 'w') as f:
            json.dump(self.agent_log, f, indent=2, ensure_ascii=False)

    def _log(self, message, level="INFO"):
        """ログ出力"""
        if self.verbose:
            timestamp = datetime.now().isoformat()
            print(f"[{timestamp}] [{level}] {message}")

    def analyze_system_with_prediction(self):
        """システムを分析して予測をベースにした最適化を実行

        Returns:
            {
                'pressure_index': float,
                'ai_decision': str,
                'predicted_decision': str,
                'final_decision': str,
                'confidence': float,
                'executed': bool
            }
        """
        self._log("=" * 80)
        self._log("システム分析 + 予測ベース最適化を開始")
        self._log("=" * 80)

        # 1. システム分析
        self._log("📊 システムメトリクスを採取中...")
        analysis = self.core_engine.analyze()

        if not analysis:
            self._log("❌ システム分析失敗", "ERROR")
            return None

        pressure_index = analysis['pressure_index']
        ai_decision = analysis['ai_decision']

        self._log(f"   Pressure Index: {pressure_index:.1f}/100 [{analysis['status']}]")
        self._log(f"   AI判定: {ai_decision}")

        # 2. 過去の実行を取得
        executions = self.learning_db.get_recent_executions(count=50)

        # 3. 予測ベースの判定を取得
        self._log("🤖 LSTM予測を実行中...")
        current_thresholds = self.learning_db.get_ai_thresholds()

        prediction_result = self.prediction_engine.integrate_prediction_into_decision(
            pressure_index,
            executions,
            current_thresholds
        )

        predicted_decision = prediction_result['predicted_decision']
        final_decision = prediction_result['final_decision']
        confidence = prediction_result['confidence']

        self._log(f"   LSTM予測: {predicted_decision}")
        self._log(f"   最終判定: {final_decision}")
        self._log(f"   信頼度: {confidence:.0%}")
        self._log(f"   理由: {prediction_result['reasoning']}")

        # 4. 判定に基づいて実行
        executed = False
        if final_decision != "NO_ACTION":
            self._log(f"🚀 {final_decision} を実行中...")

            # 最適化コマンドを実行
            if final_decision == "LIGHT_OPTIMIZE":
                try:
                    subprocess.run(['sudo', 'bash', '-c', 'echo 3 > /proc/sys/vm/drop_caches'],
                                 check=True, timeout=5)
                    subprocess.run(['sudo', 'bash', '-c', 'echo 1 > /proc/sys/vm/compact_memory'],
                                 check=True, timeout=5)
                    self._log("   ✅ キャッシュドロップとメモリコンパクション完了")
                    executed = True
                except Exception as e:
                    self._log(f"   ⚠️ 実行部分失敗: {e}", "WARN")

        else:
            self._log("   ✅ NO_ACTION - 最適化不要")
            executed = True

        # 5. 実行を記録
        if executed:
            # 現在のシステムメトリクスを採取
            current_analysis = self.core_engine.analyze()
            metrics_before = current_analysis.get('metrics', {}) if current_analysis else {}

            ai_report = {
                'timestamp': datetime.now().isoformat(),
                'pressure_index': pressure_index,
                'ai_decision': ai_decision,
                'status': current_analysis.get('status', 'UNKNOWN') if current_analysis else 'UNKNOWN'
            }

            optimization_executed = [final_decision] if final_decision != "NO_ACTION" else []

            metrics_after = {
                'cpu_pct': 0,  # ダミー値 (実際には最適化後のメトリクスが必要)
                'memory_used_gb': 0
            }

            self.learning_db.record_execution(ai_report, optimization_executed, metrics_before, metrics_after)
            self._log(f"✅ 実行を記録完了")

        return {
            'pressure_index': pressure_index,
            'ai_decision': ai_decision,
            'predicted_decision': predicted_decision,
            'final_decision': final_decision,
            'confidence': confidence,
            'executed': executed,
            'prediction_details': prediction_result
        }

    def continuous_learning_improvement(self, force_retrain=False):
        """継続的な学習と改善を実行

        Args:
            force_retrain: LSTMを強制的に再訓練するか
        """
        self._log("=" * 80)
        self._log("継続学習改善サイクルを開始")
        self._log("=" * 80)

        executions = self.learning_db.get_recent_executions(count=100)

        if len(executions) < 5:
            self._log(f"⚠️ 学習データが不足 ({len(executions)}/5)", "WARN")
            return None

        # 1. 予測精度を評価
        self._log("📈 予測精度を評価中...")
        accuracy = self.autonomous_learner.analyze_prediction_accuracy(executions)

        self._log(f"   MAE: {accuracy.get('mean_absolute_error', 0):.2f}")
        self._log(f"   RMSE: {accuracy.get('rmse', 0):.2f}")
        self._log(f"   精度: {accuracy.get('accuracy_percentage', 0):.1f}%")

        # 2. LSTM を再訓練（必要に応じて）
        if force_retrain or accuracy.get('accuracy_percentage', 0) < 50:
            self._log("🤖 LSTMモデルを再訓練中...")
            try:
                history = self.lstm_predictor.train(executions, epochs=100, batch_size=4)
                if history:
                    self._log(f"   ✅ 再訓練完了 (Loss: {history.history['loss'][-1]:.6f})")
            except Exception as e:
                self._log(f"   ⚠️ 再訓練失敗: {e}", "WARN")

        # 3. 閾値を最適化
        self._log("🎯 AI閾値を最適化中...")
        current_thresholds = self.learning_db.get_ai_thresholds()

        optimization = self.autonomous_learner.optimize_thresholds(executions, current_thresholds)

        if optimization['adjustments_made'] > 0:
            self._log(f"   ✅ {optimization['adjustments_made']}個の調整を実施")
            self._log(f"   見積もり改善: {optimization['improvement_estimate']:.2f}%")

            self.learning_db.update_ai_thresholds(optimization['optimized_thresholds'])

        # 4. 学習サイクルを記録
        self._log("📚 学習サイクルを記録中...")
        learning_cycle = {
            'timestamp': datetime.now().isoformat(),
            'cycle_number': self.agent_log['learning_cycles'] + 1,
            'executions_analyzed': len(executions),
            'prediction_accuracy': accuracy.get('accuracy_percentage', 0),
            'thresholds_optimized': optimization['adjustments_made'],
            'improvement_estimate': optimization['improvement_estimate']
        }

        self.autonomous_learner.record_learning_cycle(learning_cycle)
        self.agent_log['learning_cycles'] += 1
        self._save_agent_log()

        self._log(f"✅ 学習サイクル #{learning_cycle['cycle_number']} 完了")

        return learning_cycle

    def run_hourly_cycle(self):
        """毎時サイクルを実行（予測ベース最適化）"""
        session_start = datetime.now().isoformat()
        self._log("")
        self._log("╔" + "=" * 78 + "╗")
        self._log("║ ETERNITY AI LSTM学習エージェント - 毎時サイクル実行")
        self._log("╚" + "=" * 78 + "╝")

        result = self.analyze_system_with_prediction()

        self.agent_log['total_decisions'] += 1
        self.agent_log['sessions'].append({
            'timestamp': session_start,
            'cycle_type': 'hourly',
            'decision': result['final_decision'] if result else 'ERROR',
            'success': result is not None
        })

        self._save_agent_log()

        return result

    def run_weekly_learning_cycle(self):
        """週間学習サイクルを実行（深い学習と改善）"""
        session_start = datetime.now().isoformat()
        self._log("")
        self._log("╔" + "=" * 78 + "╗")
        self._log("║ ETERNITY AI LSTM学習エージェント - 週間学習サイクル実行")
        self._log("╚" + "=" * 78 + "╝")

        result = self.continuous_learning_improvement(force_retrain=True)

        self.agent_log['sessions'].append({
            'timestamp': session_start,
            'cycle_type': 'weekly_learning',
            'learning_cycles_completed': self.agent_log['learning_cycles'],
            'success': result is not None
        })

        self._save_agent_log()

        return result

    def generate_agent_report(self):
        """エージェントレポートを生成"""
        executions = self.learning_db.get_recent_executions(count=50)

        report = {
            'timestamp': datetime.now().isoformat(),
            'agent_status': {
                'total_decisions': self.agent_log['total_decisions'],
                'learning_cycles': self.agent_log['learning_cycles'],
                'sessions_completed': len(self.agent_log['sessions']),
                'uptime_hours': (datetime.fromisoformat(self.agent_log['initialized']) - datetime.now()).total_seconds() / 3600
            },
            'system_metrics': {
                'total_executions': len(executions),
                'prediction_accuracy': self.autonomous_learner.analyze_prediction_accuracy(executions),
                'decision_distribution': self.autonomous_learner._analyze_decision_distribution(executions)
            },
            'latest_decision': self.agent_log['sessions'][-1] if self.agent_log['sessions'] else None
        }

        return report


def main():
    """メイン実行"""
    print("=" * 80)
    print("ETERNITY AI LSTM統合学習エージェント - テスト実行")
    print("=" * 80)

    agent = ETERNITYAILSTMLearningAgent(verbose=True)

    # 毎時サイクルを実行
    print("\n【毎時サイクル実行】")
    result = agent.run_hourly_cycle()

    if result:
        print(f"\n✅ 毎時サイクル完了:")
        print(f"   圧力指数: {result['pressure_index']:.1f}")
        print(f"   最終判定: {result['final_decision']}")
        print(f"   信頼度: {result['confidence']:.0%}")

    # 週間学習サイクルを実行
    print("\n【週間学習サイクル実行】")
    learning_result = agent.run_weekly_learning_cycle()

    if learning_result:
        print(f"\n✅ 週間学習サイクル完了:")
        print(f"   分析実行数: {learning_result['executions_analyzed']}")
        print(f"   最適化調整数: {learning_result['thresholds_optimized']}")

    # レポートを生成
    print("\n【エージェントレポート】")
    report = agent.generate_agent_report()
    print(f"\n✅ エージェント状態:")
    print(f"   総決定数: {report['agent_status']['total_decisions']}")
    print(f"   学習サイクル: {report['agent_status']['learning_cycles']}")
    print(f"   セッション数: {report['agent_status']['sessions_completed']}")

    print("\n" + "=" * 80)
    print("✅ LSTM統合学習エージェントの初期化完了")
    print("=" * 80)


if __name__ == "__main__":
    main()
