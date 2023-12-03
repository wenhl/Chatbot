# I copied code from chatgpt, and I haven't try it


import numpy as np
from scipy.spatial.distance import cdist

# Load your reference dataset with embeddings and corresponding text
# The reference dataset should be a list or array where each element contains both the embedding and the text representation
reference_dataset = [
    {'embedding': np.array([0.1, 0.2, 0.3]), 'text': 'example 1'},
    {'embedding': np.array([0.4, 0.5, 0.6]), 'text': 'example 2'},
    {'embedding': np.array([0.7, 0.8, 0.9]), 'text': 'example 3'},
    # Add more elements as needed
]

# Example embedding obtained from openai.Embedding.create
input_embedding = np.array([0.55, 0.65, 0.75])

# Find the closest matching embedding in the reference dataset
distances = cdist([input_embedding], [data['embedding'] for data in reference_dataset], metric='cosine')
closest_index = np.argmin(distances)

# Retrieve the corresponding text from the reference dataset
closest_text = reference_dataset[closest_index]['text']

# Print the result
print("Input Embedding:", input_embedding)
print("Closest Text:", closest_text)
