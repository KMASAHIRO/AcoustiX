import os
import numpy as np
from pathlib import Path

# 中心基準 → 隅基準 へのオフセット差分
center_based_origin = np.array([
    -6.110 / 2 + 1.0,  # x_offset（旧基準）
    -8.807 / 2 + 1.5,  # y_offset
    -2.7 / 2 + 1.5     # z_pos
])
corner_based_origin = np.array([1.0, 1.5, 1.5])  # 新しい原点（部屋隅）

# シフト量を計算
delta = corner_based_origin - center_based_origin

def transform_and_save_ir(input_root: Path, output_root: Path):
    for tx_dir in sorted(input_root.glob("tx_*")):
        for rx_dir in sorted(tx_dir.glob("rx_*")):
            ir_files = sorted(rx_dir.glob("ir_*.npz"))
            if len(ir_files) == 0:
                continue

            # 保存先ディレクトリ作成
            rel_path = rx_dir.relative_to(input_root)
            save_dir = output_root / rel_path
            os.makedirs(save_dir, exist_ok=True)

            for ir_file in ir_files:
                data = np.load(ir_file)
                ir = data["ir"]
                rx_pos = data["position_rx"] + delta
                tx_pos = data["position_tx"] + delta
                ori_rx = data["orientation_rx"]
                ori_tx = data["orientation_tx"]

                # 保存内容構成（ch_idx は存在する場合のみ保存）
                save_args = {
                    "ir": ir,
                    "position_rx": rx_pos,
                    "position_tx": tx_pos,
                    "orientation_rx": ori_rx,
                    "orientation_tx": ori_tx,
                }
                if "ch_idx" in data:
                    save_args["ch_idx"] = data["ch_idx"]

                save_path = save_dir / ir_file.name
                np.savez(save_path, **save_args)

# 実行パス設定
input_root = Path("./custom_scene/real_env_Smooth_concrete_painted/real_env_Smooth_concrete_painted_16kHz")
output_root = Path("./custom_scene/real_env_Smooth_concrete_painted/real_env_Smooth_concrete_painted_16kHz_standard")

transform_and_save_ir(input_root, output_root)
