import gensim
from nltk import word_tokenize
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict


# Function to get the cosine similarity between a relation and query
# Note: Be sure to prepend the relation with ns:
word2vec_model = gensim.models.Word2Vec.load('word2vec_train_dev.dat')
def get_rel_score_word2vecbase(model, rel, query):
    if rel not in word2vec_model.wv:
        return 0.0
    words = word_tokenize(query.lower())
    w_embs = []
    for w in words:
        if w in word2vec_model.wv:
            w_embs.append(word2vec_model.wv[w])
    return np.mean(cosine_similarity(w_embs, [word2vec_model.wv[rel]]))


# Function to load the graph from file
def load_graph(file):
    # Preparing the graph
    graph = defaultdict(list)
    for line in open(file):
        line = eval(line[:-1])
        graph[line[0]].append([line[1], line[2]])
    return graph


# Function to load the queries from file
# Preparing the queries
def load_queries(file):
    queries = []
    for line in open(file):
        line = eval(line[:-1])
        queries.append(line)
    return queries