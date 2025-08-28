from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import numpy as np

def cluster_paragraphs(paragraphs, model_name='all-MiniLM-L6-v2', relax_pages=1):
    """Cluster paragraphs sequentially with boundary relaxation"""
    model = SentenceTransformer(model_name)
    embeddings = model.encode(paragraphs)
    
    # Initial clustering
    clustering = AgglomerativeClustering(
        n_clusters=None,
        metric='cosine', # cosine, euclidean, manhattan - cosine is used for sentence embeddings, euclidean for word embeddings, manhattan for BERT embeddings
        linkage='average', # average, complete, single - average is used for sentence embeddings, complete for word embeddings, single for BERT embeddings
        distance_threshold=0.65, # lower this value to get more clusters
    )
    labels = clustering.fit_predict(embeddings)
    
    # Find sequential boundaries
    boundaries = []
    current_label = labels[0]
    start_idx = 0
    
    for i in range(1, len(labels)):
        if labels[i] != current_label:
            boundaries.append((start_idx, i-1))
            start_idx = i
            current_label = labels[i]
    boundaries.append((start_idx, len(labels)-1))
    
    # Relax boundaries
    relaxed_boundaries = []
    prev_end = -1
    
    for i, (start, end) in enumerate(boundaries):
        # Don't relax the start of first cluster
        if i == 0:
            new_start = start
        else:
            # Try to extend start backwards up to relax_pages
            potential_start = max(prev_end - relax_pages + 1, prev_end + 1)
            new_start = potential_start
            
        # Don't relax the end of last cluster    
        if i == len(boundaries) - 1:
            new_end = end
        else:
            # Try to extend end forward up to relax_pages
            next_start = boundaries[i+1][0]
            potential_end = min(end + relax_pages, next_start)
            new_end = potential_end
            
        relaxed_boundaries.append((new_start, new_end))
        prev_end = new_end
        
    # Create final clusters based on relaxed boundaries
    final_clusters = []
    for start, end in relaxed_boundaries:
        cluster_items = [(i, paragraphs[i]) for i in range(start, end + 1)]
        final_clusters.append(cluster_items)
        
    return final_clusters