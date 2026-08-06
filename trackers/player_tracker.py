from ultralytics import YOLO 
import cv2
import pickle
import sys
sys.path.append('../')
from utils import measure_distance, get_center_of_bbox

class PlayerTracker:
    def __init__(self,model_path):
        self.model = YOLO(model_path)

    def choose_and_filter_players(self, court_keypoints, player_detections):
        top_y = (court_keypoints[1] + court_keypoints[3]) / 2
        bot_y = (court_keypoints[5] + court_keypoints[7]) / 2
        net_y = (top_y + bot_y) / 2

        filtered_player_detections = []
        for player_dict in player_detections:
            top_candidates = []
            bot_candidates = []
            for track_id, bbox in player_dict.items():
                cx, cy = get_center_of_bbox(bbox)
                h = bbox[3] - bbox[1]
                if h > 300:
                    continue  # Skip giant close-up boxes
                if cy < net_y:
                    top_candidates.append((track_id, cy, bbox))
                else:
                    bot_candidates.append((track_id, cy, bbox))
            
            top_candidates.sort(key=lambda x: abs(x[1] - top_y))
            bot_candidates.sort(key=lambda x: abs(x[1] - bot_y))

            frame_filtered = {}
            if top_candidates:
                frame_filtered[1] = top_candidates[0][2]
            if bot_candidates:
                frame_filtered[2] = bot_candidates[0][2]

            filtered_player_detections.append(frame_filtered)

        return filtered_player_detections


    def detect_frames(self,frames, read_from_stub=False, stub_path=None):
        player_detections = []

        if read_from_stub and stub_path is not None:
            with open(stub_path, 'rb') as f:
                player_detections = pickle.load(f)
            return player_detections

        for frame in frames:
            player_dict = self.detect_frame(frame)
            player_detections.append(player_dict)
        
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(player_detections, f)
        
        return player_detections

    def detect_frame(self,frame):
        results = self.model.track(frame, persist=True)[0]
        id_name_dict = results.names

        player_dict = {}
        for box in results.boxes:
            if box.id is None:
                continue  # Skip detections with no tracking ID assigned yet
            track_id = int(box.id.tolist()[0])
            result = box.xyxy.tolist()[0]
            object_cls_id = box.cls.tolist()[0]
            object_cls_name = id_name_dict[object_cls_id]
            if object_cls_name == "person":
                player_dict[track_id] = result
        
        return player_dict

    def draw_bboxes(self, video_frames, player_detections, valid_frames=None):
        output_video_frames = []
        for i, (frame, player_dict) in enumerate(zip(video_frames, player_detections)):
            if valid_frames is None or valid_frames[i]:
                # Draw Bounding Boxes
                for track_id, bbox in player_dict.items():
                    x1, y1, x2, y2 = bbox
                    cv2.putText(frame, f"Player ID: {track_id}", (int(bbox[0]), int(bbox[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
            output_video_frames.append(frame)
        
        return output_video_frames


    