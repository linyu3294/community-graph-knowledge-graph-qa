import csv
import networkx as nx

_DEBUG_ = None


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# _DEBUG_ = 1

def build_graph(graph, file, delimiter):
    reader = csv.reader(open(file), delimiter=delimiter)
    for line in reader:
        if len(line) > 2:
            if float(line[2]) != 0.0:
                graph.add_edge(int(line[0]), int(line[1]), weight=float[line[2]])
        else:
            graph.add_edge(int(line[0]), int(line[1]), weight=1.0)


def cmtyGirvanNewmanStep(G):
    # if _DEBUG_:
    #   # print('calling CmtyGirvanNewmanStep')
    init_ncomp = nx.number_connected_components(G)
    ncomp = init_ncomp
    while ncomp <= init_ncomp:
        bw = nx.edge_betweenness_centrality(G, weight='weight')
        print(bw.values())
        max_ = max(bw.values())
        for k, v in bw.items():
            if float(v) == max_:
                G.remove_edge(k[0], k[1])
        ncomp = nx.number_connected_components(G)


def getGNModularity(G, deg_, m_):
    new_adj_matrix = nx.adj_matrix(G)
    new_degree = {}
    new_degree = updateDeg(new_adj_matrix, G.nodes())
    communities = nx.connected_components(G)
    total_communities = nx.number_connected_components(G)
    print('number of communities in partitioned graph : ', total_communities)
    mod = 0

    # the equation that professor went over in class
    for c in communities:
        intra_edges = 0
        rand_edges = 0
        for u in c:
            # print('new degree ', new_degree)
            intra_edges += new_degree[u]
            rand_edges += deg_[u]
        # this is the adjacy list minus a random graph
        mod += (float(intra_edges) - float(rand_edges * rand_edges) / float(2 * m_))
    mod = mod / (2 * m_)
    if _DEBUG_:
        print('partition : %f' % mod)
    return mod


def updateDeg(adj_matrix, nodes):
    deg_dict = {}
    n = len(nodes)
    b = adj_matrix.sum(axis=1)
    for i in range(n):
        deg_dict[i] = b[i, 0]
    return deg_dict


def runGirvanNewman(G, org_degree, m_):
    best_q = 0.0
    Q = 0.0
    while True:
        cmtyGirvanNewmanStep(G)
        Q = getGNModularity(G, org_degree, m_)
        # print('modularity of decomposed G : %f' % Q)
        if Q > best_q:
            best_q = Q
            best_communities = nx.connected_components(G)
            # print('commnunities : %f' % best_communities)
        if G.number_of_edges() == 0:
            break

    if best_q > 0.0:
        print('max modularity (Q) : %f' % best_q)
        print('graph communities', best_communities)
    else:
        print('max modularity (Q) : %f' % best_q)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    path = 'edges_sampled_map_2K.csv'
    G = nx.Graph()
    build_graph(G, path, ',')

    if _DEBUG_:
        print('G nodes', G.nodes())
        print('G number of nodes', G.number_of_nodes())

    n = G.number_of_nodes()
    adj_matrix = nx.adj_matrix(G)

    m_ = 0.0

    for i in range(0, n):
        for j in range(0, n):
            m_ += adj_matrix[i, j]
    m_ = m_ / 2.0

    if _DEBUG_:
        print('m : %f' % m_)

    org_degree = {}
    org_degree = updateDeg(adj_matrix, G.nodes)

    runGirvanNewman(G, org_degree, m_)


