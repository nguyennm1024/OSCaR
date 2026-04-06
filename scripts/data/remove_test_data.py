import json
import argparse
import pandas as pd

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", required=True)
    parser.add_argument("--test-split", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    test_paths = set(pd.read_csv(args.test_split)["image_path"].tolist())
    data = read_json(args.data_path)
    post_data = [conversation for conversation in data if conversation["image"] not in test_paths]
    write_json(post_data, args.output)


if __name__ == "__main__":
    main()
