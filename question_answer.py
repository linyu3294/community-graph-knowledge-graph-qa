import gensim
from collections import Counter
from utils import load_graph, load_queries, get_rel_score_word2vecbase


def find_answer_bfs(model, graph, query, root, theta):
    model = model
    answers = set()
    visited = []
    queue = [root]
    query = query
    while len(queue) != 0:
        first_out = queue.pop(0)
        visited.append(first_out)
        # print('first out : ', first_out)
        neighbours_list = graph.get(first_out[0].strip('ns:'))
        if neighbours_list is not None:
            for neighbour in neighbours_list:
                relation = 'ns:' + neighbour[0]
                # print(relation)
                relevance_score = get_rel_score_word2vecbase(model, relation, query)
                # print(relevance_score)
                if neighbour[1] not in answers and neighbour[1] not in visited and relevance_score > theta:
                    # print('neighbours : ', neighbours_list)
                    queue.append(neighbour[1])
        else:
            answers.add(first_out)
            # print('answer node: ', first_out)
    return answers


def get_topic_tag(topic_code, graph):
    for out_nodes in graph.values():
        for node in out_nodes:
            if node[1] == topic_code:
                return node
    print('Can\'t retrieve node from graph')
    return ''


# Python program to illustrate the intersection
# of two lists in most simple way
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


if __name__ == '__main__':
    graph = load_graph('graph.txt');
    queries = load_queries('annotations.txt')
    # for k, v in graph.items():
    #     print('source : ', k,  ' | destinations : ', v)
    word2vec_model = gensim.models.Word2Vec.load('word2vec_train_dev.dat')

    overlap_len = 0
    my_estimate_pool_len = 0
    ground_truth_pool_len = 0
    for query in queries:
        my_estimate_pool = []
        ground_truth_pool = []

        root = query[3][0]
        question = query[1]
        print('\n' + question)
        print('root : ', root)
        my_answers = find_answer_bfs(word2vec_model, graph, question, root, 0.3)
        print('My answers : ', my_answers)
        my_estimate_pool.extend(my_answers)
        real_answer = [q.get('AnswerArgument') for q in query[5]]
        print('Real answers : ', real_answer, '\n')
        ground_truth_pool.extend(real_answer)

        overlap_len += len(intersection(my_estimate_pool, ground_truth_pool))
        my_estimate_pool_len += len(my_estimate_pool)
        ground_truth_pool_len += len(ground_truth_pool)

    precision = overlap_len / my_estimate_pool_len
    print('precision : ', precision)
    recall = overlap_len / ground_truth_pool_len
    print('recall : ', recall)