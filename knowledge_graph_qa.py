import gensim
from nltk import word_tokenize
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

foler = '/content/drive/MyDrive/NEU ALIGN CS Masters/CS6220 Data Mining/Colab Notebooks/knowledge_graph/'
annotations_path = foler + 'annotations.txt'
graph_path = foler + 'graph.txt'
utils_path = foler + 'util.py'
word2vec_train_dev_path = foler + 'word2vec_train_dev.dat'


# Function to get the cosine similarity between a relation and query
# Note: Be sure to prepend the relation with ns:
word2vec_model = gensim.models.Word2Vec.load('word2vec_train+dev')
def get_rel_score_word2vecbase(rel, query):
    if rel not in word2vec_model.wv:
        return 0.0
    words = word_tokenize(query.lower())
    w_embs = []
    for w in words:
        if w in word2vec_model.wv:
            w_embs.append(word2vec_model.wv[w])
    return np.mean(cosine_similarity(w_embs, [word2vec_model.wv[rel]]))


# Function to load the graph from file
def load_graph():
    # Preparing the graph
    graph = defaultdict(list)
    for line in open('graph'):
        line = eval(line[:-1])
        graph[line[0]].append([line[1], line[2]])
    return graph


# Function to load the queries from file
# Preparing the queries
def load_queries():
    queries = []
    for line in open('annotations'):
        line = eval(line[:-1])
        queries.append(line)
    return queries