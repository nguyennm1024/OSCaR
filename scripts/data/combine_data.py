import json
import argparse

# Function to read a JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to write data to a JSON file
def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-a", required=True)
    parser.add_argument("--input-b", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data_1 = read_json(args.input_a)
    data_2 = read_json(args.input_b)
    combined_data = data_1 + data_2
    write_json(combined_data, args.output)


if __name__ == "__main__":
    main()
