import json
import glob
import requests
import os
import random
import argparse

ENDPOINT = "https://api.openai.com/v1/chat/completions"

PROMPT_PREFIX = """
        From this caption, give me 10 multiple-choice question and answer focusing on the object’s state. The answer needs to be found in the caption, and the questions can also serve as a suggestion to generate this caption and do not mention the caption in question.Each question has 4 choice. Output should follow the format
    Question_1: Generate a question here
    (A): Answer A
    (B): Answer B
    (C): Answer C
    (D): Answer D
    Correct_answer: (Choice) : Correct answer
    Question_2: Generate a question here
    (A): Answer A
    (B): Answer B
    (C): Answer C
    (D): Answer D
    Correct_answer: (Choice) : Correct answer
    Question_3: Generate a question here
    (A): Answer A
    (B): Answer B
    (C): Answer C
    (D): Answer D
    Correct_answer: (Choice) : Correct answer
    Question_4: Generate a question here
    (A): Answer A
    (B): Answer B
    (C): Answer C
    (D): Answer D
    Correct_answer: (Choice) : Correct answer
    Question_5: Generate a question here
    (A): Answer A
    (B): Answer B
    (C): Answer C
    (D): Answer D
    Correct_answer: (Choice) : Correct answer
    Question_6: Generate a question here
    (A): Answer A
    (B): Answer B
    (C): Answer C
    (D): Answer D
    Correct_answer: (Choice) : Correct answer
    Question_7: Generate a question here
    (A): Answer A
    (B): Answer B
    (C): Answer C
    (D): Answer D
    Correct_answer: (Choice) : Correct answer
    Question_8: Generate a question here
    (A): Answer A
    (B): Answer B
    (C): Answer C
    (D): Answer D
    Correct_answer: (Choice) : Correct answer
    Question_9: Generate a question here
    (A): Answer A
    (B): Answer B
    (C): Answer C
    (D): Answer D
    Correct_answer: (Choice) : Correct answer
    Question_10: Generate a question here
    (A): Answer A
    (B): Answer B
    (C): Answer C
    (D): Answer D
    Correct_answer: (Choice) : Correct answer
    Where question is the question, A,B,C,D are 4 choice for the question, Correct_answer is the correct answer. The answer should be long and questions should look like a conversation.
"""


def build_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "OSCaR Release"
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder", required=True)
    parser.add_argument("--output-folder", required=True)
    parser.add_argument("--model", default="gpt-3.5-turbo-0613")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY must be set to run question generation.")

    os.makedirs(args.output_folder, exist_ok=True)
    paths = glob.glob(os.path.join(args.input_folder, "*.json"))
    random.shuffle(paths)
    headers = build_headers(api_key)

    for path in paths:
        is_success = True
        output_path = path.replace(args.input_folder.rstrip("/") + "/", args.output_folder.rstrip("/") + "/")
        if os.path.isfile(output_path):
            print(path + " is already processed!")
            continue
        print(path)
        with open(path, "r") as file:
            data = json.load(file)

        responses = {}
        for key, value in data.items():
            print(key)
            prompt = PROMPT_PREFIX + "\n" + value
            data = {
                "model": args.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            response = requests.post(ENDPOINT, headers=headers, data=json.dumps(data))
            response_json = response.json()
            if 'error' in response_json:
                print(response_json['error'])
                is_success = False
                break

            assistant_response = response_json['choices'][0]['message']['content']
            responses[key] = assistant_response

        if is_success:
            with open(output_path, 'w') as file:
                json.dump(responses, file, indent=4)


if __name__ == "__main__":
    main()
