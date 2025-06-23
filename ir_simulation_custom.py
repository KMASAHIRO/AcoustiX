import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tensorflow as tf
tf.get_logger().setLevel('ERROR')
tf.random.set_seed(1)

import json
import numpy as np
from simu_utils import ir_simulation, save_ir, load_cfg
from shutil import copyfile

if __name__ == '__main__':
    # シミュレーション設定ファイルとシーンファイルのパス
    config_file = "./simu_config/basic_config.yml"
    dataset_name = "real_env_Smooth_concrete_painted"
    scene_path = "./custom_scene/real_env_Smooth_concrete_painted/real_env_Smooth_concrete_painted.xml"

    # 受信機の位置と向き
    rx_pos = np.asarray([[0.0, 0.0, 1.5]])
    rx_ori = np.asarray([[1.0, 0.0, 0.0]])

    # 送信機の位置と向き
    tx_pos = np.asarray([4.0, 4.0, 1.5])
    tx_ori = np.asarray([1.0, 0.0, 0.0])

    rx_ori /= np.linalg.norm(rx_ori)
    tx_ori /= np.linalg.norm(tx_ori)

    # 出力先ディレクトリの作成と設定ファイルのコピー
    scene_folder = os.path.dirname(os.path.abspath(scene_path))
    output_path = os.path.join(scene_folder, dataset_name)
    os.makedirs(output_path, exist_ok=True)
    copyfile(config_file, os.path.join(output_path, "config.yml"))

    # 設定ファイルの読み込み
    simu_config = load_cfg(config_file=config_file)

    # 送信機の情報をJSONで保存
    data = {
        "speaker": {
            "positions": tx_pos.tolist(),
            "orientations": tx_ori.tolist()
        }
    }
    with open(os.path.join(output_path, 'speaker_data.json'), 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # IRのシミュレーション
    ir_time_all, rx_pos, rx_ori = ir_simulation(
        scene_path=scene_path,
        rx_pos=rx_pos,
        tx_pos=tx_pos,
        rx_ori=rx_ori,
        tx_ori=tx_ori,
        simu_config=simu_config
    )

    # IRデータの保存
    save_ir(
        ir_samples=ir_time_all,
        rx_pos=rx_pos,
        rx_ori=rx_ori,
        tx_pos=tx_pos,
        tx_ori=tx_ori,
        save_path=output_path,
        prefix=0
    )
