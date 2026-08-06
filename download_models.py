import os
import sys

def download_models():
    # pyrefly: ignore [missing-import]
    import gdown

    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)

    ball_model_path = os.path.join(models_dir, "yolo5_last.pt")
    keypoint_model_path = os.path.join(models_dir, "keypoints_model.pth")

    BALL_MODEL_ID = "1UZwiG1jkWgce9lNhxJ2L0NVjX1vGM05U"
    KEYPOINT_MODEL_ID = "1QrTOF1ToQ4plsSZbkBs3zOLkVt3MBlta"

    # Remove invalid html error files if present
    for p in [ball_model_path, keypoint_model_path]:
        if os.path.exists(p) and os.path.getsize(p) < 1000000:
            print(f"Removing incomplete/invalid file {p} ({os.path.getsize(p)} bytes)")
            os.remove(p)

    if not os.path.exists(ball_model_path):
        print("Downloading Tennis Ball Model (yolo5_last.pt) via gdown...")
        url = f"https://drive.google.com/uc?id={BALL_MODEL_ID}"
        gdown.download(url, ball_model_path, quiet=False)

    if not os.path.exists(keypoint_model_path):
        print("Downloading Court Keypoint Model (keypoints_model.pth) via gdown...")
        url = f"https://drive.google.com/uc?id={KEYPOINT_MODEL_ID}"
        gdown.download(url, keypoint_model_path, quiet=False)

    print("--- Model Verification ---")
    print(f"yolo5_last.pt size: {os.path.getsize(ball_model_path) if os.path.exists(ball_model_path) else 'Missing'} bytes")
    print(f"keypoints_model.pth size: {os.path.getsize(keypoint_model_path) if os.path.exists(keypoint_model_path) else 'Missing'} bytes")

if __name__ == "__main__":
    download_models()
