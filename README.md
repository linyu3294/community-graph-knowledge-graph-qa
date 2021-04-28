# community-graph-knowledge-graph-qa
Implementing two data mining algorithms. knowledge graph and community detection (Girvan-Newman)



Social Community Detection --
Implement a community detection algorithm on the Flicker Graph. Use the betweenes idea on edges and the Girvan–Newman Algorithm. 
The original dataset graph has more than 5M edges; in DM_resources there are 4 different sub-sampled graphs with edge counts from 2K to 600K; 
you can use these if the original is too big.

You should use a library to support graph operations (edges, vertices, paths, degrees, etc). 
We used igraph in python which also have builtin community detection algorithms (not allowed); t
hese are useful as a way to evaluate communities you obtain




Knowledge Base Question Answering --
Given is knowledge graph with entities and relations, questions with starting entity and answers, and their word embedding . For each question, navigate the graph from the start entiry outwards until you find appropriate answer entities.

there might be multiple answers correct, use F1 to evaluate
utils functions (similarity, load_graphs) are given, but you can choose not to use them
answers are given to be used for evaluation only
your strategy should be a graph traversal augmented with scoring of paths; you might discard paths not promising along the way. This is similar to a focused crawl strategy.
for simplicity, the questions are picked so that the answer is always at the end of the relevant path (not intermediary)
