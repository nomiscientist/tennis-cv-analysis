# 🎾 Complete Guide: Processing a New Match Video (e.g., Australian Open Final)

This step-by-step guide explains how to adapt this project for a brand-new tennis match video (such as the **Australian Open Final**), including how to extract, annotate, or generate a custom **Court Keypoints Model / Data File**.

---

## 📌 Workflow Overview

```
1. Prepare Match Video ➔ 2. Test Existing Keypoint Model ➔ 3. (If Needed) Annotate 14 Keypoints ➔ 4. Train/Update Model ➔ 5. Reset Stubs & Run Inference
```

---

## 🎥 Step 1: Prepare Your Australian Open Video

1. **Obtain Video Footage**:
   - Download or trim your Australian Open match video clip (e.g., 30-60 seconds rally).
   - Ensure the camera angle is the **main high broadcast baseline view** (showing the full court and both players clearly).
2. **Save Video File**:
   - Save the file as `input_videos/australia_open_final.mp4`.
3. **Update `main.py` Video Path**:
   ```python
   # Inside main.py (Line 18)
   input_video_path = "input_videos/australia_open_final.mp4"
   ```

---

## 📐 Step 2: Test the Existing Court Keypoint Model

Australian Open hard courts have standard blue surfaces and standard court dimensions. The pre-trained ResNet-50 keypoint model (`models/keypoints_model.pth`) usually works out of the box!

1. Open `main.py` and temporarily disable stub loading so it re-runs detection on your new video:
   ```python
   # Line 25-31 in main.py:
   player_detections = player_tracker.detect_frames(video_frames, read_from_stub=False)
   ball_detections = ball_tracker.detect_frames(video_frames, read_from_stub=False)
   ```
2. Run `python main.py`.
3. Inspect the first frame keypoints saved in `output_videos/output_video.avi`.

---

## ✏️ Step 3: Creating a Custom Keypoint Dataset & File (If Re-Training Needed)

If the camera angle of your Australian Open clip is drastically different or zooming causes keypoint misalignments, follow these steps to build a **new custom keypoint dataset (`data.json`)**:

### The 14 Keypoints Landmark Map

You must annotate the 14 keypoint $(x, y)$ coordinates in exact sequence (indices 0 through 13):

```
       (0)------(4)--------------(6)------(1)  <-- Top Baseline
        |        |                |        |
        |       (8)-----(12)-----(9)       |  <-- Top Service Line
        |        |       |        |        |
    === | ====== | ===== | ====== | ====== | === (Net)
        |        |       |        |        |
        |       (10)----(13)----(11)       |  <-- Bottom Service Line
        |        |                |        |
       (2)------(5)--------------(7)------(3)  <-- Bottom Baseline
```

#### Keypoint Coordinate Mapping:
- **Keypoint 0**: Top-Left Outer Corner (Top Baseline, far left double line)
- **Keypoint 1**: Top-Right Outer Corner (Top Baseline, far right double line)
- **Keypoint 2**: Bottom-Left Outer Corner (Bottom Baseline, far left double line)
- **Keypoint 3**: Bottom-Right Outer Corner (Bottom Baseline, far right double line)
- **Keypoint 4**: Top-Left Singles Line Intersection
- **Keypoint 5**: Bottom-Left Singles Line Intersection
- **Keypoint 6**: Top-Right Singles Line Intersection
- **Keypoint 7**: Bottom-Right Singles Line Intersection
- **Keypoint 8**: Top Service Line (Left corner)
- **Keypoint 9**: Top Service Line (Right corner)
- **Keypoint 10**: Bottom Service Line (Left corner)
- **Keypoint 11**: Bottom Service Line (Right corner)
- **Keypoint 12**: Top Service Line Center T-Junction
- **Keypoint 13**: Bottom Service Line Center T-Junction

---

## 🛠️ Step 4: Annotation Tool Script (`annotate_court.py`)

Run this interactive tool to click and save 14 keypoints for your new video frame:

```python
# Create file: annotate_court.py
import cv2
import json

video_path = "input_videos/australia_open_final.mp4"
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
cap.release()

points = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(frame, str(len(points)-1), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Annotate 14 Keypoints", frame)
        print(f"Keypoint {len(points)-1}: ({x}, {y})")

cv2.imshow("Annotate 14 Keypoints", frame)
cv2.setMouseCallback("Annotate 14 Keypoints", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Format into JSON
dataset_entry = [{
    "id": "australia_open_frame1",
    "keypoints": [coord for pt in points for coord in pt] # flattened 28 values
}]

with open("training/custom_court_keypoints.json", "w") as f:
    json.dump(dataset_entry, f, indent=4)

print("Saved custom keypoints to training/custom_court_keypoints.json!")
```

---

## 🚀 Step 5: Training a New Model in Notebook

1. Open `training/tennis_court_keypoints_training.ipynb`.
2. Load your new dataset:
   ```python
   dataset = KeypointsDataset(img_dir="input_videos", data_file="training/custom_court_keypoints.json")
   ```
3. Run the training loop for 50-100 epochs using `MSELoss`.
4. Save the trained checkpoint:
   ```python
   torch.save(model.state_dict(), "models/australia_open_keypoints_model.pth")
   ```
5. Update `main.py`:
   ```python
   court_model_path = "models/australia_open_keypoints_model.pth"
   ```

---

## 🧹 Step 6: Reset Tracker Stubs & Run

Whenever you change your input video:
1. Delete old stub pickle files:
   ```bash
   rm tracker_stubs/*.pkl
   ```
2. In `main.py`, run with `read_from_stub=False` on first pass to generate new detection stubs.
3. Run the pipeline:
   ```bash
   python main.py
   ```
4. View your new Australian Open match analysis video in `output_videos/output_video.avi`!
