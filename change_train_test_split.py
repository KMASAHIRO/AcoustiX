import pickle
from pathlib import Path

def change_split_base_dir(original_split_path: Path, old_base: Path, new_base: Path, output_path: Path):
    """
    既存の split.pkl を読み込んで、パスの親ディレクトリ（old_base）を new_base に変更して再保存
    """
    with open(original_split_path, 'rb') as f:
        split = pickle.load(f)

    updated_split = {}
    for key in ['train', 'test']:
        updated_split[key] = []
        for rel_path in split[key]:
            rel_path = Path(rel_path)  # すでに相対パスか確認（絶対なら relative_to を使う）
            new_path = new_base / rel_path
            updated_split[key].append(str(new_path))

    with open(output_path, 'wb') as f:
        pickle.dump(updated_split, f)

    print(f"Updated split saved to: {output_path}")

# 使用例
if __name__ == "__main__":
    original_split_path = Path("../Pyroomacoustics/outputs/real_env_avr_16kHz/train_test_split.pkl")
    old_base = Path("./outputs/real_env_avr_16kHz")
    new_base = Path("./custom_scene/real_env_Smooth_concrete_painted/real_env_Smooth_concrete_painted_16kHz")
    output_path = new_base / "train_test_split.pkl"

    change_split_base_dir(original_split_path, old_base, new_base, output_path)
