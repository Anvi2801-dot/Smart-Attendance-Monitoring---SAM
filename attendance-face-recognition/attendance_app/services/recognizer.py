import numpy as np

def compare_embeddings(embed1, embed2, threshold=0.6):
    embed1 = np.array(embed1)
    embed2 = np.array(embed2)
    distance = np.linalg.norm(embed1 - embed2)
    return distance < threshold
