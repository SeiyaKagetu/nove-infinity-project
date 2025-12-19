#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETERNITY AI LSTM予測エンジン
圧力指数と最適化効果を予測するニューラルネットワーク
"""

import json
import numpy as np
from datetime import datetime, timedelta
import os

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("警告: TensorFlowがインストールされていません。シミュレーションモードで実行します。")


class ETERNITYAILSTMPredictor:
    """LSTM予測エンジン"""

    def __init__(self, sequence_length=5, forecast_horizon=3):
        """
        Args:
            sequence_length: 入力シーケンス長（時系列ステップ数）
            forecast_horizon: 予測地平線（何ステップ先を予測するか）
        """
        self.sequence_length = sequence_length
        self.forecast_horizon = forecast_horizon
        self.model = None
        self.scaler_min = None
        self.scaler_max = None
        self.training_history = []
        self.db_path = "/home/seiya/.eternity_ai_learning"
        self.model_path = os.path.join(self.db_path, "lstm_model.h5")
        self.lstm_metadata_path = os.path.join(self.db_path, "lstm_metadata.json")

        if TENSORFLOW_AVAILABLE:
            self._load_or_create_model()

    def _load_or_create_model(self):
        """既存モデルを読み込むか新規作成"""
        if os.path.exists(self.model_path):
            try:
                self.model = keras.models.load_model(self.model_path)
                self._load_metadata()
                print(f"✅ LSTM モデルを読み込みました: {self.model_path}")
            except Exception as e:
                print(f"⚠️ モデル読み込み失敗: {e}。新規作成します。")
                self._create_model()
        else:
            self._create_model()

    def _create_model(self):
        """LSTM モデルを新規作成"""
        model = keras.Sequential([
            LSTM(64, activation='relu', input_shape=(self.sequence_length, 4), return_sequences=True),
            Dropout(0.2),
            LSTM(32, activation='relu', return_sequences=False),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(8, activation='relu'),
            Dense(self.forecast_horizon, activation='linear')
        ])

        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )

        self.model = model
        print("✅ 新規LSTMモデルを作成しました")

    def _normalize(self, data):
        """データを正規化 [0, 1]"""
        if len(data) == 0:
            return np.array([]), 0, 1

        data = np.array(data, dtype=np.float32)
        min_val = np.min(data)
        max_val = np.max(data)

        # スケール幅が0の場合の対処
        if max_val - min_val < 1e-6:
            return data, min_val, min_val + 1

        normalized = (data - min_val) / (max_val - min_val)
        return normalized, min_val, max_val

    def _denormalize(self, data, min_val, max_val):
        """正規化を逆変換"""
        return data * (max_val - min_val) + min_val

    def extract_features(self, execution_history):
        """実行履歴から特徴を抽出

        Returns:
            各実行の[Pressure Index, Memory %, CPU %, Effectiveness Score]
        """
        features = []

        for execution in execution_history:
            pressure = execution.get('pressure_index', 50)

            metrics_before = execution.get('metrics_before', {})
            memory_pct = (metrics_before.get('memory_used_gb', 5) / 15.3) * 100
            cpu_pct = metrics_before.get('cpu_pct', 30)

            effectiveness = execution.get('effectiveness', {}).get('effectiveness_score', 0)

            features.append([pressure, memory_pct, cpu_pct, effectiveness])

        return np.array(features, dtype=np.float32)

    def prepare_training_data(self, features):
        """訓練データを準備

        Args:
            features: [num_samples, 4] 形状の特徴配列

        Returns:
            X, y の訓練データペア
        """
        if len(features) < self.sequence_length + self.forecast_horizon:
            print(f"⚠️ データが不足: {len(features)} < {self.sequence_length + self.forecast_horizon}")
            return None, None

        X, y = [], []

        for i in range(len(features) - self.sequence_length - self.forecast_horizon + 1):
            # 入力: sequence_length個のステップ
            X.append(features[i:i + self.sequence_length])

            # 出力: 次のforecast_horizon個のステップの圧力指数
            y.append(features[i + self.sequence_length:i + self.sequence_length + self.forecast_horizon, 0])

        return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

    def train(self, execution_history, epochs=50, batch_size=2):
        """モデルを訓練

        Args:
            execution_history: 実行履歴のリスト
            epochs: エポック数
            batch_size: バッチサイズ
        """
        if not TENSORFLOW_AVAILABLE:
            print("⚠️ TensorFlowがインストールされていません。訓練をスキップします。")
            return None

        # 特徴抽出
        features = self.extract_features(execution_history)

        if len(features) < 10:
            print(f"⚠️ データが不十分（{len(features)}件）。合成データで補強します。")
            features = self._augment_with_synthetic_data(features)

        # 訓練データ準備
        X, y = self.prepare_training_data(features)

        if X is None:
            print("❌ 訓練データ作成失敗")
            return None

        # 正規化
        X_list = [X[:, :, i] for i in range(X.shape[2])]
        normalized_X_list = []
        for X_feat in X_list:
            X_norm, _, _ = self._normalize(X_feat.flatten())
            normalized_X_list.append(X_norm.reshape(X_feat.shape))

        X_normalized = np.stack(normalized_X_list, axis=2)
        y_normalized, y_min, y_max = self._normalize(y.flatten())
        y_normalized = y_normalized.reshape(y.shape)

        self.scaler_min = y_min
        self.scaler_max = y_max

        print(f"📊 訓練開始: X shape={X_normalized.shape}, y shape={y_normalized.shape}")

        # 訓練
        history = self.model.fit(
            X_normalized, y_normalized,
            epochs=epochs,
            batch_size=batch_size,
            verbose=0,
            validation_split=0.2
        )

        # メタデータ保存
        self._save_metadata()
        self._save_model()

        print(f"✅ 訓練完了 (Loss: {history.history['loss'][-1]:.6f})")
        self.training_history.append({
            'timestamp': datetime.now().isoformat(),
            'epochs': epochs,
            'final_loss': float(history.history['loss'][-1]),
            'samples_trained': len(X)
        })

        return history

    def predict_pressure(self, recent_features, steps_ahead=3):
        """将来の圧力指数を予測

        Args:
            recent_features: 最近の[Pressure, Memory%, CPU%, Effectiveness]
            steps_ahead: 何ステップ先まで予測するか

        Returns:
            予測された圧力指数のリスト
        """
        if not TENSORFLOW_AVAILABLE or self.model is None:
            return self._synthetic_prediction(recent_features, steps_ahead)

        # 最新のsequence_length個を入力
        if len(recent_features) < self.sequence_length:
            # パディング
            padding = np.tile(recent_features[-1], (self.sequence_length - len(recent_features), 1))
            sequence = np.vstack([padding, recent_features])
        else:
            sequence = recent_features[-self.sequence_length:]

        # 正規化
        sequence_norm = sequence.copy().astype(np.float32)
        for i in range(sequence_norm.shape[1]):
            col = sequence_norm[:, i]
            col_min = np.min(col)
            col_max = np.max(col)
            if col_max - col_min > 1e-6:
                sequence_norm[:, i] = (col - col_min) / (col_max - col_min)

        # 予測
        X_input = np.expand_dims(sequence_norm, axis=0)
        y_pred_norm = self.model.predict(X_input, verbose=0)[0]

        # 正規化を逆変換
        if self.scaler_max - self.scaler_min > 1e-6:
            y_pred = self._denormalize(y_pred_norm, self.scaler_min, self.scaler_max)
        else:
            y_pred = y_pred_norm * 50 + 30  # フォールバック

        # 予測値を[0, 100]に制限
        y_pred = np.clip(y_pred, 0, 100)

        return y_pred[:steps_ahead].tolist()

    def _synthetic_prediction(self, recent_features, steps_ahead):
        """合成予測（TensorFlow非使用時）"""
        if len(recent_features) == 0:
            return [50.0] * steps_ahead

        last_pressure = recent_features[-1, 0]
        predictions = []

        for i in range(steps_ahead):
            # 簡単な減衰予測
            trend = -2.0 * (i + 1) / steps_ahead  # 圧力は徐々に低下する傾向
            predicted = last_pressure + trend
            predicted = np.clip(predicted, 0, 100)
            predictions.append(float(predicted))

        return predictions

    def _augment_with_synthetic_data(self, features):
        """合成データで訓練データを補強"""
        print("🤖 合成データを生成して訓練セットを補強中...")

        synthetic = []
        base = features[0] if len(features) > 0 else np.array([50, 50, 30, 5])

        for i in range(30):
            noise = np.random.normal(0, 5, size=4)
            synthetic.append(base + noise)

        return np.vstack([features] + [np.array(s) for s in synthetic])

    def _save_model(self):
        """モデルを保存"""
        if self.model is not None:
            self.model.save(self.model_path)
            print(f"💾 モデルを保存: {self.model_path}")

    def _save_metadata(self):
        """メタデータを保存"""
        metadata = {
            'sequence_length': self.sequence_length,
            'forecast_horizon': self.forecast_horizon,
            'scaler_min': float(self.scaler_min) if self.scaler_min is not None else 0,
            'scaler_max': float(self.scaler_max) if self.scaler_max is not None else 100,
            'training_count': len(self.training_history),
            'last_trained': datetime.now().isoformat(),
            'training_history': self.training_history
        }

        with open(self.lstm_metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def _load_metadata(self):
        """メタデータを読み込み"""
        if os.path.exists(self.lstm_metadata_path):
            with open(self.lstm_metadata_path, 'r') as f:
                metadata = json.load(f)
                self.scaler_min = metadata.get('scaler_min', 0)
                self.scaler_max = metadata.get('scaler_max', 100)
                self.training_history = metadata.get('training_history', [])


def main():
    """テスト実行"""
    print("=" * 80)
    print("ETERNITY AI LSTM予測エンジン - テスト実行")
    print("=" * 80)

    # 実行履歴を読み込み
    history_path = "/home/seiya/.eternity_ai_learning/execution_history.json"
    with open(history_path, 'r') as f:
        history_data = json.load(f)

    executions = history_data.get('executions', [])
    print(f"\n📊 読み込み実行数: {len(executions)}")

    # LSTMプレディクターを初期化
    predictor = ETERNITYAILSTMPredictor(sequence_length=3, forecast_horizon=3)

    # 特徴を抽出
    features = predictor.extract_features(executions)
    print(f"✅ 特徴を抽出: {features.shape}")

    # 訓練
    if len(executions) >= 2 and TENSORFLOW_AVAILABLE:
        history = predictor.train(executions, epochs=100, batch_size=1)
        if history:
            print(f"📈 訓練履歴:")
            print(f"   最終Loss: {history.history['loss'][-1]:.6f}")

    # 予測
    print(f"\n🔮 将来の圧力指数を予測:")
    predictions = predictor.predict_pressure(features, steps_ahead=3)
    for i, pred in enumerate(predictions):
        print(f"   T+{i+1}: {pred:.1f}/100")

    print("\n" + "=" * 80)
    print("✅ LSTM予測エンジンの初期化完了")
    print("=" * 80)


if __name__ == "__main__":
    main()
