import os
import json
import sys
import shutil
import argparse

def rename_files(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file == 'frame_state_change.txt':
                # Construct full file path
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, 'state_change.txt')

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} -> {new_file_path}')


def convert_to_padded_string(number):
    return "{:010d}".format(number)

def process_folder(subdir, frame_files):
    contents = {}

    # Extract IDs and sort them
    frame_ids = [int(f.split('_')[1].split('.')[0]) for f in frame_files]
    frame_ids.sort()
    frame_ids = [convert_to_padded_string(id) for id in frame_ids]

    # Read files in sorted order
    for frame_id in frame_ids:
        file_name = f'frame_{frame_id}.txt'
        with open(os.path.join(subdir, file_name), 'r') as file:
            contents[f'Frame_{frame_ids.index(frame_id) + 1}'] = file.read().replace('.\n\n', '').replace('</s>', '').replace('.\n', '').strip()

    # Read state change file
    if os.path.isfile(os.path.join(subdir, 'state_change.txt')):
        state_change = os.path.join(subdir, 'state_change.txt')
    else:
        state_change = os.path.join(subdir, 'frame_state_change.txt')
    with open(state_change, 'r') as file:
        contents['State_change_caption'] = file.read().replace('.\n\n', '').replace('</s>', '').replace('.\n', '').strip()

    return contents

def clean_output_folders(root_folder):
    for subdir, dirs, files in os.walk(root_folder):
        if os.path.basename(subdir) == 'output':
            # subdir is an 'output' folder, clean it
            for filename in files:
                file_path = os.path.join(subdir, filename)
                os.remove(file_path)
                print(f'Removed file: {file_path}')

            for directory in dirs:
                dir_path = os.path.join(subdir, directory)
                shutil.rmtree(dir_path)
                print(f'Removed directory: {dir_path}')

            print(f'Cleaned output folder: {subdir}')


def main(root_folder):
    clean_output_folders(root_folder)
    # breakpoint()
    for subdir, dirs, files in os.walk(root_folder):
        if len(files) == 4:
            frame_files = [f for f in files if f.startswith('frame_') and f.endswith('.txt')]
            if ('state_change.txt' in files or 'frame_state_change.txt' in files) and len(frame_files) == 3:
                contents = process_folder(subdir, frame_files)
                folder_name = os.path.basename(subdir)

                if not folder_name.startswith('P'):
                    # parent_folder_name = os.path.basename(os.path.dirname(subdir))
                    folder_name = f"{folder_name}"
                if 'P' not in folder_name:
                    output_folder = os.path.join(subdir, '..', '..', 'output')
                else:
                    output_folder = os.path.join(subdir, '..', '..', 'output')
                os.makedirs(output_folder, exist_ok=True)
                output_file = os.path.join(output_folder, f'{folder_name}.json')

                with open(output_file, 'w') as json_file:
                    json.dump(contents, json_file, indent=4)
                print(f'JSON file saved to {output_file}')
                

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root-folder", required=True)
    args = parser.parse_args()
    rename_files(args.root_folder)
    main(args.root_folder)
