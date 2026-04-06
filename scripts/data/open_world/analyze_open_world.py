import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from collections import Counter
import ast

# Ensure that the necessary NLTK tokenizers and taggers are downloaded
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

ego4d_narrations = pd.read_csv('open_world_Ego4D_test.csv')['action_narration'].tolist()
ek_narrations = pd.read_csv('open_world_EK.csv')['narration'].tolist()

# narrations = ego4d_narrations + ek_narrations
narrations = ek_narrations

narrations = pd.read_csv('open_world_EK.csv')['']

# Tokenize words and tag part of speech
words = nltk.word_tokenize(' '.join(narrations))
tagged_words = nltk.pos_tag(words)

# Separate words into nouns and verbs based on their POS tags
nouns = [word for word, pos in tagged_words if pos.startswith('NN')]  # Nouns
verbs = [word for word, pos in tagged_words if pos.startswith('VB')]  # Verbs

# Generate frequency distributions for nouns and verbs
noun_freq = Counter(nouns)
verb_freq = Counter(verbs)

# Create word cloud objects for nouns and verbs
noun_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(noun_freq)
verb_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(verb_freq)

# Display the generated Word Clouds
plt.figure(figsize=(15, 7.5))  # Increase figure size for better resolution
plt.imshow(noun_wordcloud, interpolation='bilinear')
plt.axis('off')  # Remove axis
# plt.title('Object Word Cloud')
plt.savefig('object_word_cloud.png', format='png', dpi=300)

plt.figure(figsize=(15, 7.5))  # Increase figure size for better resolution
plt.imshow(verb_wordcloud, interpolation='bilinear')
plt.axis('off')  # Remove axis
# plt.title('Action Word Cloud')
plt.savefig('action_word_cloud.png', format='png', dpi=300)
