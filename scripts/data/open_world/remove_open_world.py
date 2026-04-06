import pandas as pd

ek_open = pd.read_csv('open_world_EK.csv')['object'].tolist()
# ego4d = pd.read_csv('open_world_Ego4D.csv')['object']

ego_training = pd.read_csv('../ego4d_train_prompts.csv')['object'].tolist()
ego_testing = pd.read_csv('../ego4d_test_prompts.csv')['object'].tolist()

ego4d = ego_testing + ego_training
ego4d = set(ego4d)
ek_open = list(set(ek_open))

count = 0
for obj in ek_open:
    if obj in ego4d:
        count += 1
        
print(count, len(ek_open))

ego4d_open = pd.read_csv('open_world_Ego4D.csv')['object'].tolist()
print(len(list(set(ego4d_open))))
