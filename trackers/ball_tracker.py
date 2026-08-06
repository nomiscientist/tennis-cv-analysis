from ultralytics import YOLO 
import cv2
import pickle
import pandas as pd

class BallTracker:
    def __init__(self,model_path):
        self.model = YOLO(model_path)

    def interpolate_ball_positions(self, ball_positions, court_keypoints=None):
        if court_keypoints is not None:
            import numpy as np
            court_poly = np.array([
                [court_keypoints[0], court_keypoints[1]],
                [court_keypoints[2], court_keypoints[3]],
                [court_keypoints[6], court_keypoints[7]],
                [court_keypoints[4], court_keypoints[5]]
            ], dtype=np.int32)

            cleaned_ball_positions = []
            for b_dict in ball_positions:
                valid_dict = {}
                if 1 in b_dict:
                    bbox = b_dict[1]
                    cx = (bbox[0] + bbox[2]) / 2
                    cy = (bbox[1] + bbox[3]) / 2
                    dist = cv2.pointPolygonTest(court_poly, (float(cx), float(cy)), True)
                    if dist >= -30:  # Keep detections inside or within 30px of court boundary
                        valid_dict[1] = bbox
                cleaned_ball_positions.append(valid_dict)
            ball_positions = cleaned_ball_positions

        ball_positions_list = [x.get(1,[]) for x in ball_positions]
        # convert the list into pandas dataframe
        df_ball_positions = pd.DataFrame(ball_positions_list,columns=['x1','y1','x2','y2'])

        # interpolate the missing values
        df_ball_positions = df_ball_positions.interpolate(method='linear')
        df_ball_positions = df_ball_positions.bfill().ffill()

        # Smooth trajectory with centered rolling window filter to remove pixel jitter
        df_ball_positions = df_ball_positions.rolling(window=5, min_periods=1, center=True).mean()

        ball_positions = [{1:x} for x in df_ball_positions.to_numpy().tolist()]

        return ball_positions

    def get_ball_shot_frames(self,ball_positions):
        ball_positions = [x.get(1,[]) for x in ball_positions]
        # convert the list into pandas dataframe
        df_ball_positions = pd.DataFrame(ball_positions,columns=['x1','y1','x2','y2'])

        df_ball_positions['ball_hit'] = 0

        df_ball_positions['mid_y'] = (df_ball_positions['y1'] + df_ball_positions['y2'])/2
        df_ball_positions['mid_y_rolling_mean'] = df_ball_positions['mid_y'].rolling(window=5, min_periods=1, center=False).mean()
        df_ball_positions['delta_y'] = df_ball_positions['mid_y_rolling_mean'].diff()
        minimum_change_frames_for_hit = 25
        for i in range(1,len(df_ball_positions)- int(minimum_change_frames_for_hit*1.2) ):
            negative_position_change = df_ball_positions['delta_y'].iloc[i] >0 and df_ball_positions['delta_y'].iloc[i+1] <0
            positive_position_change = df_ball_positions['delta_y'].iloc[i] <0 and df_ball_positions['delta_y'].iloc[i+1] >0

            if negative_position_change or positive_position_change:
                change_count = 0 
                for change_frame in range(i+1, i+int(minimum_change_frames_for_hit*1.2)+1):
                    negative_position_change_following_frame = df_ball_positions['delta_y'].iloc[i] >0 and df_ball_positions['delta_y'].iloc[change_frame] <0
                    positive_position_change_following_frame = df_ball_positions['delta_y'].iloc[i] <0 and df_ball_positions['delta_y'].iloc[change_frame] >0

                    if negative_position_change and negative_position_change_following_frame:
                        change_count+=1
                    elif positive_position_change and positive_position_change_following_frame:
                        change_count+=1
            
                if change_count>minimum_change_frames_for_hit-1:
                    df_ball_positions.loc[i, 'ball_hit'] = 1

        frame_nums_with_ball_hits = df_ball_positions[df_ball_positions['ball_hit']==1].index.tolist()

        return frame_nums_with_ball_hits

    def detect_frames(self,frames, read_from_stub=False, stub_path=None):
        ball_detections = []

        if read_from_stub and stub_path is not None:
            with open(stub_path, 'rb') as f:
                ball_detections = pickle.load(f)
            return ball_detections

        for frame in frames:
            player_dict = self.detect_frame(frame)
            ball_detections.append(player_dict)
        
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(ball_detections, f)
        
        return ball_detections

    def detect_frame(self, frame):
        results = self.model.predict(frame, conf=0.08)[0]

        best_ball = None
        max_conf = 0.0
        for box in results.boxes:
            result = box.xyxy.tolist()[0]
            conf = float(box.conf[0])
            if conf > max_conf:
                max_conf = conf
                best_ball = result

        ball_dict = {}
        if best_ball is not None:
            ball_dict[1] = best_ball
        
        return ball_dict

    def draw_bboxes(self, video_frames, player_detections, valid_frames=None):
        output_video_frames = []
        for i, (frame, ball_dict) in enumerate(zip(video_frames, player_detections)):
            if valid_frames is None or valid_frames[i]:
                # Draw Bounding Boxes
                for track_id, bbox in ball_dict.items():
                    x1, y1, x2, y2 = bbox
                    cv2.putText(frame, f"Ball ID: {track_id}", (int(bbox[0]), int(bbox[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
            output_video_frames.append(frame)
        
        return output_video_frames


    