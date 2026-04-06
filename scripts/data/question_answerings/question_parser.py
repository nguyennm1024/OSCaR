import json
import glob
import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder", required=True)
    parser.add_argument("--output-folder", required=True)
    args = parser.parse_args()

    os.makedirs(args.output_folder, exist_ok=True)
    paths = glob.glob(os.path.join(args.input_folder, "*.json"))

    for path in paths:
        is_ignore = False
        clean_data = {}
        with open(path, 'r') as file:
            data_raw = json.load(file)

        for key, value in data_raw.items():
            text = value
            lines = [line.strip() for line in text.split("\n") if line.strip()]

            questions = []
            options = []
            correct_answers = []

            for line in lines:
                if line.startswith("Question_"):
                    questions.append(line.split(":")[1].strip())
                elif line.startswith("(A)") or line.startswith("(B)") or line.startswith("(C)") or line.startswith("(D)"):
                    opt = line.split(":")
                    if len(opt) == 1:
                        opt = line.split(')')
                    options.append(opt[1].strip())
                elif line.startswith("Correct_answer"):
                    correct_answers.append(line.split("answer:")[1].strip())

            chunked_options = [options[i:i+4] for i in range(0, len(options), 4)]

            data = {}
            try:
                for i, (question, option_set, correct_answer) in enumerate(zip(questions, chunked_options, correct_answers)):
                    correct_parts = correct_answer.split(":")
                    if len(correct_parts) == 1:
                        correct_parts = correct_answer.split(')')
                    correct_key = correct_parts[0].strip() if len(correct_parts) > 0 else None
                    correct_key = 'Option_' + correct_key.replace('(', '').replace(')', '')
                    correct_value = correct_parts[1].strip() if len(correct_parts) > 1 else None
                    data[f"Question_{i+1}"] = {
                        "Question": question,
                        "Option_A": option_set[0],
                        "Option_B": option_set[1],
                        "Option_C": option_set[2],
                        "Option_D": option_set[3],
                        "Correct_answer_key": correct_key,
                        "Correct_answer_value": correct_value
                    }
            except Exception:
                is_ignore = True
                break
            clean_data[key] = data
        if is_ignore:
            os.remove(path)
            print('Ignored', path)
        else:
            output_path = path.replace(args.input_folder.rstrip("/") + "/", args.output_folder.rstrip("/") + "/")
            with open(output_path, 'w') as file:
                json.dump(clean_data, file, indent=4)


if __name__ == "__main__":
    main()
