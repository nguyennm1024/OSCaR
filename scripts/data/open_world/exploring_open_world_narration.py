import json
import csv

# Load and parse the ego4d.json file
with open('ego4d.json', 'r') as f:
    ego4d_data = json.load(f)
clips = ego4d_data['clips']

# Convert clips list to a dictionary for faster access
clips_dict = {clip['video_uid']: clip for clip in clips}

# Load and parse the all_narrations_redacted.json file
with open('all_narrations_redacted.json', 'r') as f:
    narrations_data = json.load(f)
        
        
# Function to find the clip_uid by video_uid and clip_time_start
def find_clip_uid(video_uid, clip_time_start, clips_dict):
    clip = clips_dict.get(video_uid)
    if clip and clip['video_start_sec'] <= clip_time_start <= clip['video_end_sec']:
        return clip['clip_uid'], clip['video_start_sec']
    return None, None

# Open the CSV file for writing
with open('clips_mapping.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['clip_uid', 'action_time_start', 'narration'])
    count = 0
    # Iterate through videos in the narrations data
    for video_uid, video_data in narrations_data['videos'].items():
        count += 1
        # print(count)
        narrations = video_data['narrations']
        for i in range(len(narrations) - 1):
            clip_time_start = narrations[i]['_clip_time_start']
            
            clip_uid, video_start_sec = find_clip_uid(video_uid, clip_time_start, clips_dict)
            if narrations[i]['_clip_time_start'] != narrations[i]['_clip_time_end']:
                print(clip_uid)
            if clip_uid:
                # Write the result directly to the CSV file
                writer.writerow([
                    clip_uid,
                    clip_time_start-video_start_sec,
                    narrations[i]['text']
                ])
