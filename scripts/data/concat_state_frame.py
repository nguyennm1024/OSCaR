import json
import os
import shutil
from PIL import Image
import csv
import argparse

def concat_images(image_paths):
    images = [Image.open(x) for x in image_paths]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im

def process_json_file(json_file, root_output_folder):
    with open(json_file, 'r') as file:
        data = json.load(file)

    csv_data = []
    
    for entry in data:
        result_id = entry['result_id']
        folder_name = result_id.split('-')[0]
        output_folder = os.path.join(root_output_folder, folder_name)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        frames = entry['frames']
        frame_paths = []
        for frame in frames:
            frame_id = frame.split('_')[-1].split('.')[0]
            new_frame_name = f"frame_{frame_id}.jpg"
            new_frame_path = os.path.join(output_folder, new_frame_name)
            shutil.copy(frame, new_frame_path)
            frame_paths.append(new_frame_path)

            # CSV data
            csv_data.append([new_frame_path, entry['raw']['object'].replace(':', ' '), f"Frame_{len(frame_paths)}"])

        combined_image = concat_images(frame_paths)
        combined_image_path = os.path.join(output_folder, 'state_change.jpg')
        combined_image.save(combined_image_path)

        # CSV data for combined image
        csv_data.append([combined_image_path, entry['raw']['object'].replace(':', ' '), "State_change_caption"])

    # Save CSV file
    csv_file_path = os.path.join(root_output_folder, "images_data.csv")
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['image_path', 'object', 'caption_key'])
        csvwriter.writerows(csv_data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-file", required=True)
    parser.add_argument("--output-folder", required=True)
    args = parser.parse_args()
    process_json_file(args.json_file, args.output_folder)


if __name__ == "__main__":
    main()
