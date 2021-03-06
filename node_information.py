import networkx
import random
import numpy
import scipy
import dgl

def normalize(l):
    return (l - numpy.mean(l)) / (numpy.std(l) if numpy.std(l) > 1e-6 else 1)

def get_nodes_degree(graph):
    return [x for _,x in graph.degree]

def get_nodes_closeness_centrality(graph):
    return list(networkx.closeness_centrality(graph).values())

def get_nodes_betweenness_centrality(graph):
    return list(networkx.betweenness_centrality(graph).values())

def get_nodes_pagerank(graph):
    return list(networkx.algorithms.link_analysis.pagerank_alg.pagerank(graph).values())

def get_nodes_triangles(graph):
    return list(networkx.algorithms.cluster.triangles(graph).values())

def get_nodes_random(graph):
    return list([random.random() for _ in graph.nodes()])

def get_ones(graph):
    return list([1.0 for _ in graph.nodes()])

def get_nodes_eigenvector(graph, k=1):
    A = networkx.convert_matrix.to_scipy_sparse_matrix(graph).astype(float)
    N = scipy.sparse.diags(numpy.array(get_nodes_degree(graph)).clip(1), dtype=float)
    L = N * scipy.sparse.eye(graph.number_of_nodes()) - A

    EigVal, EigVec = scipy.sparse.linalg.eigs(L, k+1, which='SR', tol=5e-1)
    EigVec = EigVec[:, EigVal.argsort()]
    return numpy.absolute(numpy.real(EigVec[:, -1]))

NODE_INFORMATION = {'degree' : get_nodes_degree, 'closeness_centrality' : get_nodes_closeness_centrality,
                    'betweenness_centrality' : get_nodes_betweenness_centrality, 'pagerank' : get_nodes_pagerank,
                    'triangles' : get_nodes_triangles, 'random' : get_nodes_random, 'ones' : get_ones,
                    'eig1' : (lambda g : get_nodes_eigenvector(g, 1)),
                    'eig2' : (lambda g : get_nodes_eigenvector(g, 2)),
                    'eig3' : (lambda g : get_nodes_eigenvector(g, 3)),
                    'degree_normalized' : (lambda g : normalize(get_nodes_degree(g))),
                    'triangles_normalized' : (lambda g : normalize(get_nodes_triangles(g)))
                   }