#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETERNITY AI LSTM 7日間監視ダッシュボード
7日間のAI意思決定と学習プロセスを追跡・分析
"""

import json
import os
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

class ETERNITYLSTMMonitoringDashboard:
    """7日間LSTM監視ダッシュボード"""
    
    def __init__(self):
        self.db_path = "/home/seiya/.eternity_ai_learning"
        self.execution_history_file = os.path.join(self.db_path, "execution_history.json")
        self.monitoring_log_path = os.path.join(self.db_path, "lstm_monitoring_log.json")
        self.start_date = datetime.now().date()
        self.load_or_create_monitoring_log()
    
    def load_or_create_monitoring_log(self):
        """監視ログを読み込みまたは作成"""
        if os.path.exists(self.monitoring_log_path):
            with open(self.monitoring_log_path, 'r', encoding='utf-8') as f:
                self.monitoring_log = json.load(f)
        else:
            self.monitoring_log = {
                "monitoring_start": datetime.now().isoformat(),
                "target_days": 7,
                "daily_reports": [],
                "performance_metrics": {},
                "lstm_learning_progress": []
            }
            self.save_monitoring_log()
    
    def save_monitoring_log(self):
        """監視ログを保存"""
        with open(self.monitoring_log_path, 'w', encoding='utf-8') as f:
            json.dump(self.monitoring_log, f, indent=2, ensure_ascii=False)
    
    def generate_daily_report(self):
        """本日の日報を生成"""
        print("\n" + "=" * 80)
        print("ETERNITY AI LSTM 7日間監視ダッシュボード - 本日の日報")
        print("=" * 80)
        
        # 1. 実行統計
        executions = self.load_executions()
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_executions = [e for e in executions 
                          if datetime.fromisoformat(e['timestamp']) > today_start]
        
        print(f"\n【本日実行統計】{datetime.now().strftime('%Y-%m-%d')}")
        print(f"  本日実行数: {len(today_executions)}件")
        print(f"  累計実行数: {len(executions)}件")
        
        # 2. 直近実行の詳細
        if today_executions:
            latest = today_executions[-1]
            print(f"\n【最新実行詳細】")
            print(f"  実行時刻: {latest['timestamp']}")
            print(f"  圧力指数: {latest.get('pressure_index', 'N/A')}/100")
            print(f"  ステータス: {latest.get('status', 'UNKNOWN')}")
            print(f"  AI判定: {latest.get('ai_decision', 'UNKNOWN')}")
            print(f"  効果スコア: {latest.get('effectiveness', {}).get('effectiveness_score', 0):.2f}")
        
        # 3. 統計情報
        stats = self.load_statistics()
        print(f"\n【システム統計】")
        print(f"  総実行数: {stats.get('total_executions', 0)}件")
        print(f"  総最適化実行: {stats.get('total_optimizations', 0)}件")
        print(f"  解放メモリ合計: {stats.get('total_memory_freed_mb', 0):.1f}MB")
        print(f"  平均効果スコア: {stats.get('total_effectiveness_score', 0) / max(1, stats.get('total_executions', 1)):.2f}")
        
        # 4. 意思決定分布
        decisions = stats.get('decisions_count', {})
        print(f"\n【意思決定分布】")
        for decision, count in decisions.items():
            total = stats.get('total_executions', 1)
            ratio = (count / total * 100) if total > 0 else 0
            print(f"  {decision}: {count}回 ({ratio:.1f}%)")
        
        # 5. 学習サイクル進捗
        print(f"\n【学習サイクル進捗】")
        try:
            with open(os.path.join(self.db_path, "autonomous_learning.json"), 'r') as f:
                learning_data = json.load(f)
                cycles = learning_data.get('learning_cycles', [])
                print(f"  完了した学習サイクル: {len(cycles)}回")
                if len(cycles) > 0:
                    latest_cycle = cycles[-1]
                    print(f"  最新サイクル: {latest_cycle.get('timestamp', 'N/A')}")
        except:
            print(f"  完了した学習サイクル: 0回（学習開始待機中）")
        
        # 6. エラー検出
        print(f"\n【エラー・アラート】")
        errors = self.detect_anomalies(executions)
        if errors:
            for error in errors:
                print(f"  ⚠️  {error}")
        else:
            print(f"  ✅ エラーなし")
        
        # 7. 推奨アクション
        print(f"\n【推奨アクション】")
        recommendations = self.generate_recommendations(executions, stats)
        for rec in recommendations:
            print(f"  💡 {rec}")
        
        # ログに記録
        daily_record = {
            "date": datetime.now().isoformat(),
            "executions_today": len(today_executions),
            "total_executions": len(executions),
            "latest_decision": latest['ai_decision'] if today_executions else 'N/A',
            "learning_cycles": len(cycles) if 'cycles' in locals() else 0,
            "errors_detected": len(errors),
            "recommendations": recommendations
        }
        self.monitoring_log['daily_reports'].append(daily_record)
        self.save_monitoring_log()
        
        print("\n" + "=" * 80)
        print("✅ 本日の日報完成")
        print("=" * 80)
    
    def load_executions(self):
        """実行履歴を読み込み"""
        try:
            with open(self.execution_history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('executions', [])
        except:
            return []
    
    def load_statistics(self):
        """統計を読み込み"""
        try:
            with open(os.path.join(self.db_path, "statistics.json"), 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def detect_anomalies(self, executions):
        """異常を検出"""
        anomalies = []
        
        # 1. 圧力指数の急激な上昇
        if len(executions) >= 2:
            recent_pressures = [e.get('pressure_index', 50) for e in executions[-5:]]
            if recent_pressures[-1] > recent_pressures[0] + 20:
                anomalies.append(f"圧力指数が急上昇: {recent_pressures[0]:.1f} → {recent_pressures[-1]:.1f}")
        
        # 2. 低い効果スコア
        low_effectiveness = [e for e in executions[-5:] 
                            if e.get('effectiveness', {}).get('effectiveness_score', 0) < 1.0]
        if len(low_effectiveness) >= 3:
            anomalies.append(f"低い効果スコア: 直近5実行中{len(low_effectiveness)}件が低効率")
        
        # 3. 連続したNO_ACTION
        no_action_count = 0
        for e in reversed(executions[-10:]):
            if e.get('ai_decision') == 'NO_ACTION':
                no_action_count += 1
            else:
                break
        if no_action_count >= 8:
            anomalies.append(f"連続NO_ACTION: 直近{no_action_count}実行がすべてNO_ACTION")
        
        return anomalies
    
    def generate_recommendations(self, executions, stats):
        """推奨事項を生成"""
        recommendations = []
        
        # 学習データ充実度
        if len(executions) < 20:
            recommendations.append(f"実行データ蓄積: {len(executions)}/20件まで進捗（学習精度向上のため20件以上推奨）")
        else:
            recommendations.append(f"✅ 実行データ充分: {len(executions)}件、LSTM学習最適状態")
        
        # 学習サイクル実行
        try:
            with open(os.path.join(self.db_path, "autonomous_learning.json"), 'r') as f:
                cycles = json.load(f).get('learning_cycles', [])
                if len(cycles) == 0:
                    recommendations.append("学習サイクル待機: 5実行以上で自動開始")
                else:
                    recommendations.append(f"✅ 学習中: {len(cycles)}回の学習サイクル完了")
        except:
            recommendations.append("学習サイクル待機: 5実行以上で自動開始")
        
        # 意思決定品質
        decisions = stats.get('decisions_count', {})
        total = stats.get('total_executions', 1)
        if total > 0:
            light_opt_ratio = decisions.get('LIGHT_OPTIMIZE', 0) / total
            if light_opt_ratio > 0.7:
                recommendations.append(f"軽い最適化が頻繁: 閾値調整の自動最適化を監視中")
            elif light_opt_ratio < 0.2 and total > 10:
                recommendations.append(f"最適化が不足: Pressure Index上昇の可能性、監視強化推奨")
        
        # TensorFlow状態
        recommendations.append("TensorFlow: シミュレーションモード（pip install tensorflowで本番モード有効）")
        
        return recommendations
    
    def generate_week_summary(self):
        """週間サマリーを生成"""
        print("\n" + "=" * 80)
        print("ETERNITY AI LSTM 7日間監視 - 週間サマリー")
        print("=" * 80)
        
        reports = self.monitoring_log.get('daily_reports', [])
        
        if not reports:
            print("まだデータがありません")
            return
        
        total_executions = reports[-1].get('total_executions', 0) if reports else 0
        learning_cycles = reports[-1].get('learning_cycles', 0) if reports else 0
        total_errors = sum(r.get('errors_detected', 0) for r in reports)
        
        print(f"\n【監視期間】")
        print(f"  開始: {self.monitoring_log.get('monitoring_start')}")
        print(f"  期間: {len(reports)}日")
        
        print(f"\n【7日間統計】")
        print(f"  総実行数: {total_executions}件")
        平均実行数 = total_executions / max(1, len(reports))
        print(f"  平均実行数/日: {平均実行数:.1f}件")
        print(f"  学習サイクル: {learning_cycles}回")
        print(f"  検出エラー数: {total_errors}件")
        
        print(f"\n✅ 7日間監視完了")
        print("=" * 80)

def main():
    """メイン実行"""
    dashboard = ETERNITYLSTMMonitoringDashboard()
    dashboard.generate_daily_report()
    
    # 週間サマリーチェック
    reports = dashboard.monitoring_log.get('daily_reports', [])
    if len(reports) >= 7:
        dashboard.generate_week_summary()

if __name__ == "__main__":
    main()
