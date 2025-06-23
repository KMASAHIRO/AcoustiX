import numpy as np

# ファイルパス
npz_path = "/home/kato/AVR/AcoustiX/extract_scene/Pomaria_2_int/test/ir_000001.npz"

# npzファイルを読み込む
with np.load(npz_path) as data:
    print("📂 ファイル内の配列一覧:")
    for key in data.files:
        array = data[key]
        print(f" - {key}: shape={array.shape}, dtype={array.dtype}")
    
    print(data["position_rx"])
    print(data["position_tx"])
    print(data["orientation_rx"])
    print(data["orientation_tx"])
