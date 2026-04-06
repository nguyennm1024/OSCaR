import pandas as pd

def sampling_ego4d():
    # Function to safely convert string to list
    def safe_eval(x):
        if isinstance(x, str):
            try:
                x = eval(x)
                return x
            except:
                return [x]  # Return a list with the original value in case of error
        return x  # If not a string, return as is

    # Load the CSV file
    df = pd.read_csv('open_world_Ego4D.csv')

    # Safely convert 'scenarios' column from string representation of list to actual list
    df['scenarios'] = df['scenarios'].apply(safe_eval)

    # Explode the 'scenarios' column
    df_exploded = df.explode('scenarios')

    # Initialize an empty DataFrame for the sampled data
    sampled_df = pd.DataFrame()

    # Sample 10 unique clips from each scenario
    for scenario, group in df_exploded.groupby('scenarios'):
        try:
            sampled_clips = group.drop_duplicates('clip_uid').sample(n=10, replace=False)
            sampled_df = sampled_df._append(sampled_clips, ignore_index=True)
        except ValueError:
            # Handle case where there are fewer than 10 clips for a scenario
            sampled_df = sampled_df._append(group.drop_duplicates('clip_uid'), ignore_index=True)

    # Save the sampled data to a new CSV file
    sampled_df[sampled_df['domain'] == 'Open world'].to_csv('sampled_open_world_ego4d.csv', index=False)

def sampling_ek():

    # Load the CSV file
    df = pd.read_csv('open_world_EK.csv')

    # Randomly sample 344 rows
    sampled_df = df.sample(n=344, random_state=1)  # random_state ensures reproducibility

    # Save the sampled data to a new CSV file
    sampled_df.to_csv('sampled_open_world_EK.csv', index=False)

sampling_ek()
