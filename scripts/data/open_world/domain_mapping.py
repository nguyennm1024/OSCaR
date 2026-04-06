import pandas as pd
import json

# Load the init_open_world.csv file
df_init_open_world = pd.read_csv('init_open_world.csv')

# Load and parse the ego4d.json file
with open('ego4d.json', 'r') as f:
    ego4d_data = json.load(f)

# Extract clips and videos information
clips = ego4d_data['clips']
videos = ego4d_data['videos']

# Create a mapping from clip_uid to video_uid
clip_to_video_mapping = {clip['clip_uid']: clip['video_uid'] for clip in clips}

# Create a mapping from video_uid to scenarios
video_to_scenarios_mapping = {video['video_uid']: video['scenarios'] for video in videos}

# Map clip_uid to video_uid and add it as a new column to the DataFrame
df_init_open_world['video_uid'] = df_init_open_world['clip_uid'].map(clip_to_video_mapping)

# Map video_uid to scenarios and add it as a new column to the DataFrame
df_init_open_world['scenarios'] = df_init_open_world['video_uid'].map(video_to_scenarios_mapping)

# Add a column categorizing each row as 'In domain' or 'Open world'
df_init_open_world['domain'] = df_init_open_world['scenarios'].apply(
    lambda x: 'In domain' if isinstance(x, list) and 'Cooking' in x 
    else ('Open world' if isinstance(x, list) else 'Not sure')
)

# Save the updated DataFrame to final_open_world.csv
df_init_open_world.to_csv('final_open_world.csv', index=False)