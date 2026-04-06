import json
import pandas as pd

with open('fho_main.json', 'r') as f:
    fho_data = json.load(f)

# count = 0
# fho_data = fho_data['videos']
# for i in range(len(fho_data)):
#     annotated_intervals = fho_data[i]['annotated_intervals']
#     breakpoint()
#     for j in range(len(annotated_intervals)):
#         narrated_actions = annotated_intervals[j]['narrated_actions']
#         if len(narrated_actions) > 0:
#             for k in range(len(narrated_actions)):
#                 narrated_text = narrated_actions[k]['narration_text']
#                 if len(narrated_text) > 0:
#                     narrated_text = narrated_text.replace('#C C', '').replace('#C', '').replace('#c c', '').replace('#O', '').strip()

data = []
fho_data = fho_data['videos']
for i in range(len(fho_data)):
    annotated_intervals = fho_data[i]['annotated_intervals']
    for j in range(len(annotated_intervals)):
        # # Clip id here
        # print(annotated_intervals[j]['clip_uid'])
        clip_uid = annotated_intervals[j]['clip_uid']
        narrated_actions = annotated_intervals[j]['narrated_actions']
        if len(narrated_actions) > 0:
            for k in range(len(narrated_actions)):
                object_name = ''
                # # Start and end frame here
                # print(narrated_actions[k])
                start_frame = narrated_actions[k]['start_frame']
                end_frame = narrated_actions[k]['end_frame']
                narrated_frames = narrated_actions[k]['frames']
                if narrated_frames:
                    for t in range(len(narrated_frames)):
                        for box in narrated_frames[t]['boxes']:
                            if box['object_type'] == 'object_of_change':
                                # print(box['structured_noun'])
                                object_name = box['structured_noun']
                                break
                    middle_frame = narrated_frames[len(narrated_frames)//2]['frame_number']
                    if middle_frame <= start_frame or middle_frame >= end_frame:
                        middle_frame = (start_frame+end_frame)//2
                    action = narrated_actions[k]['structured_verb']
                    action_narration = narrated_actions[k]['narration_text']
                    if clip_uid != None and action != None and object_name != None and start_frame != None and middle_frame != None and end_frame != None and action_narration != None:
                        data.append({'clip_uid': clip_uid, 'action': action, 'object': object_name, 
                 'start_frame': start_frame, 'middle_frame': middle_frame, 
                 'end_frame': end_frame, 'action_narration': action_narration.replace('\n', '')})

                        # print(clip_uid, action, object_name, start_frame, middle_frame, end_frame, action_narration)
                       
                    # print('==========================')
                    
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('init_open_world.csv', index=False)