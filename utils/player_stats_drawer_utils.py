import numpy as np
import cv2

def draw_player_stats(output_video_frames, player_stats, valid_frames=None):

    for index, row in player_stats.iterrows():
        if valid_frames is not None and not valid_frames[index]:
            continue
        player_1_shot_speed = row['player_1_last_shot_speed']
        player_2_shot_speed = row['player_2_last_shot_speed']
        player_1_speed = row['player_1_last_player_speed']
        player_2_speed = row['player_2_last_player_speed']

        avg_player_1_shot_speed = row['player_1_average_shot_speed']
        avg_player_2_shot_speed = row['player_2_average_shot_speed']
        avg_player_1_speed = row['player_1_average_player_speed']
        avg_player_2_speed = row['player_2_average_player_speed']

        frame = output_video_frames[index]

        width = 280
        height = 190

        # Position at bottom-right corner aligned with mini-court right margin
        end_x = frame.shape[1] - 20
        end_y = frame.shape[0] - 20
        start_x = end_x - width
        start_y = end_y - height

        overlay = frame.copy()
        cv2.rectangle(overlay, (start_x, start_y), (end_x, end_y), (0, 0, 0), -1)
        alpha = 0.5 
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        output_video_frames[index] = frame

        text = "     Player 1     Player 2"
        output_video_frames[index] = cv2.putText(output_video_frames[index], text, (start_x+60, start_y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        text = "Shot Speed"
        output_video_frames[index] = cv2.putText(output_video_frames[index], text, (start_x+10, start_y+62), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        text = f"{player_1_shot_speed:.1f} km/h    {player_2_shot_speed:.1f} km/h"
        output_video_frames[index] = cv2.putText(output_video_frames[index], text, (start_x+110, start_y+62), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)

        text = "Player Speed"
        output_video_frames[index] = cv2.putText(output_video_frames[index], text, (start_x+10, start_y+100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        text = f"{player_1_speed:.1f} km/h    {player_2_speed:.1f} km/h"
        output_video_frames[index] = cv2.putText(output_video_frames[index], text, (start_x+110, start_y+100), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
        
        text = "avg. S. Speed"
        output_video_frames[index] = cv2.putText(output_video_frames[index], text, (start_x+10, start_y+138), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        text = f"{avg_player_1_shot_speed:.1f} km/h    {avg_player_2_shot_speed:.1f} km/h"
        output_video_frames[index] = cv2.putText(output_video_frames[index], text, (start_x+110, start_y+138), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
        
        text = "avg. P. Speed"
        output_video_frames[index] = cv2.putText(output_video_frames[index], text, (start_x+10, start_y+175), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        text = f"{avg_player_1_speed:.1f} km/h    {avg_player_2_speed:.1f} km/h"
        output_video_frames[index] = cv2.putText(output_video_frames[index], text, (start_x+110, start_y+175), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
    
    return output_video_frames
