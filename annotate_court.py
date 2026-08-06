import cv2
import json
import os

def main():
    video_path = "input_videos/input_video.mp4"
    if not os.path.exists(video_path):
        print(f"Video file {video_path} not found. Please place your match video in input_videos/")
        return

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Could not read frame from video.")
        return

    points = []
    clone = frame.copy()

    print("=========================================================")
    print("🎾 Interactive Court Keypoint Annotator (14 Points)")
    print("Click on the 14 keypoints in sequence (0 to 13):")
    print(" 0: Top-Left Outer Corner       1: Top-Right Outer Corner")
    print(" 2: Bottom-Left Outer Corner    3: Bottom-Right Outer Corner")
    print(" 4: Top-Left Singles Line       5: Bottom-Left Singles Line")
    print(" 6: Top-Right Singles Line      7: Bottom-Right Singles Line")
    print(" 8: Top Service Left Corner     9: Top Service Right Corner")
    print("10: Bottom Service Left Corner 11: Bottom Service Right Corner")
    print("12: Top Service Center T-Joint 13: Bottom Service Center T-Joint")
    print("=========================================================")

    def click_event(event, x, y, flags, params):
        nonlocal frame
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 14:
            points.append((x, y))
            idx = len(points) - 1
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            cv2.putText(frame, str(idx), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.imshow("Click 14 Keypoints (Press 'r' to reset, 'q' to quit)", frame)
            print(f"Keypoint {idx}: ({x}, {y})")

    cv2.imshow("Click 14 Keypoints (Press 'r' to reset, 'q' to quit)", frame)
    cv2.setMouseCallback("Click 14 Keypoints (Press 'r' to reset, 'q' to quit)", click_event)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            points = []
            frame = clone.copy()
            cv2.imshow("Click 14 Keypoints (Press 'r' to reset, 'q' to quit)", frame)
            print("Reset all keypoints.")
        elif key == ord('q') or len(points) == 14:
            break

    cv2.destroyAllWindows()

    if len(points) == 14:
        flat_keypoints = []
        for p in points:
            flat_keypoints.extend([p[0], p[1]])
        
        output_data = [{
            "id": "custom_match_frame",
            "keypoints": flat_keypoints
        }]

        os.makedirs("training", exist_ok=True)
        out_json = "training/custom_match_keypoints.json"
        with open(out_json, "w") as f:
            json.dump(output_data, f, indent=4)
        print(f"Successfully saved 14 keypoints to {out_json}!")
    else:
        print(f"Annotation incomplete ({len(points)}/14 points collected).")

if __name__ == "__main__":
    main()
