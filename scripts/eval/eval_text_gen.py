import argparse
import json
import os

import nltk
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from rouge import Rouge

nltk.download("punkt", quiet=True)

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_scores(predicted_text, ground_truth_text):
    # Ensure neither text is empty
    if not predicted_text.strip() or not ground_truth_text.strip():
        return 0, {'rouge-1': {'f': 0}, 'rouge-2': {'f': 0}, 'rouge-l': {'f': 0}}

    # Tokenize the sentences for BLEU
    predicted_tokens = nltk.word_tokenize(predicted_text)
    ground_truth_tokens = [nltk.word_tokenize(ground_truth_text)]

    # Apply smoothing function for BLEU
    chencherry = SmoothingFunction()
    bleu_score = sentence_bleu(ground_truth_tokens, predicted_tokens, smoothing_function=chencherry.method1)

    # Calculate ROUGE scores
    rouge = Rouge()
    rouge_scores = rouge.get_scores(predicted_text, ground_truth_text)[0]

    return bleu_score, rouge_scores

def main(predicted_folder, groundtruth_folder_ek, groundtruth_folder_ego4d):
    bleu_scores = []
    rouge_1_scores = []
    rouge_2_scores = []
    rouge_l_scores = []

    print(predicted_folder)
    for filename in os.listdir(predicted_folder):
        predicted_file_path = os.path.join(predicted_folder, filename)
        if filename.startswith('P'):
            groundtruth_file_path = os.path.join(groundtruth_folder_ek, filename)
        else:
            groundtruth_file_path = os.path.join(groundtruth_folder_ego4d, filename)
        # groundtruth_file_path = os.path.join(groundtruth_folder, filename)
        if os.path.exists(groundtruth_file_path):
            predicted_data = read_json_file(predicted_file_path)
            groundtruth_data = read_json_file(groundtruth_file_path)

            for key in predicted_data:
                if (len(predicted_data[key])) < 3:
                    predicted_data[key] = 'No answer.'
                bleu, rouge_scores = calculate_scores(predicted_data[key], groundtruth_data[key])
                bleu_scores.append(bleu)
                rouge_1_scores.append(rouge_scores['rouge-1']['f'])
                rouge_2_scores.append(rouge_scores['rouge-2']['f'])
                rouge_l_scores.append(rouge_scores['rouge-l']['f'])

    avg_bleu = sum(bleu_scores) / len(bleu_scores)
    avg_rouge_1 = sum(rouge_1_scores) / len(rouge_1_scores)
    avg_rouge_2 = sum(rouge_2_scores) / len(rouge_2_scores)
    avg_rouge_l = sum(rouge_l_scores) / len(rouge_l_scores)

    print(f'Average BLEU score: {avg_bleu}')
    print(f'Average ROUGE-1 score: {avg_rouge_1}')
    print(f'Average ROUGE-2 score: {avg_rouge_2}')
    print(f'Average ROUGE-L score: {avg_rouge_l}')
    print('=============================\n\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--predicted-folder", required=True, type=str)
    parser.add_argument("--groundtruth-ek", required=True, type=str)
    parser.add_argument("--groundtruth-ego4d", required=True, type=str)
    args = parser.parse_args()
    main(args.predicted_folder, args.groundtruth_ek, args.groundtruth_ego4d)
