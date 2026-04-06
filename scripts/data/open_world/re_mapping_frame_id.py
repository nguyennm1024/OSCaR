import pandas as pd
import json

def load_csv(file_path):
    return pd.read_csv(file_path)

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def normalize_frames(row, video_start_frames):
    clip_uid = row['clip_uid']
    if clip_uid in video_start_frames:
        video_start_frame = video_start_frames[clip_uid]
        row['start_frame'] -= video_start_frame
        row['middle_frame'] -= video_start_frame
        row['end_frame'] -= video_start_frame
    return row

def main():
    # Replace with your file paths
    csv_file_path = 'sampled_open_world_ego4d.csv'
    json_file_path = 'ego4d.json'

    df = load_csv(csv_file_path)
    json_data = load_json(json_file_path)

    # Extract video start frames
    video_start_frames = {clip['clip_uid']: clip['video_start_frame'] for clip in json_data['clips']}

    # Normalize the frame data
    df_normalized = df.apply(lambda row: normalize_frames(row, video_start_frames), axis=1)

    # Save to a new CSV file
    normalized_csv_file_path = 'normalized_sampled_open_world_ego4d.csv'
    df_normalized.to_csv(normalized_csv_file_path, index=False)

    print(f"Normalized data saved to {normalized_csv_file_path}")

if __name__ == "__main__":
    main()
