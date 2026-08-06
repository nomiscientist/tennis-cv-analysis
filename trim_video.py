"""
Trim a long match video to a short clip for analysis.
Adjust START_SEC and END_SEC to pick the rally you want to analyze.
"""
import cv2
import os

INPUT_VIDEO = "input_videos/australia_open.mp4"
OUTPUT_VIDEO = "input_videos/australia_open_clip.mp4"

# ========================================
# CHANGE THESE to pick your rally segment
# ========================================
START_SEC = 30    # Start at 30 seconds into the video
END_SEC = 45      # End at 45 seconds (15 second clip)

cap = cv2.VideoCapture(INPUT_VIDEO)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps

print(f"Source Video: {INPUT_VIDEO}")
print(f"Resolution: {width}x{height}, FPS: {fps}, Duration: {duration:.1f}s, Total Frames: {total_frames}")
print(f"Trimming: {START_SEC}s to {END_SEC}s ({END_SEC - START_SEC}s clip)")

start_frame = int(START_SEC * fps)
end_frame = int(END_SEC * fps)
clip_frames = end_frame - start_frame
memory_gb = clip_frames * width * height * 3 / (1024**3)
print(f"Clip Frames: {clip_frames}, Estimated RAM: {memory_gb:.2f} GB")

cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))

frame_count = 0
while cap.isOpened() and frame_count < clip_frames:
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)
    frame_count += 1

cap.release()
out.release()

file_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
print(f"\nSaved trimmed clip: {OUTPUT_VIDEO} ({file_size_mb:.1f} MB, {frame_count} frames)")
print(f"Now update main.py line 18 to: input_video_path = \"{OUTPUT_VIDEO}\"")
