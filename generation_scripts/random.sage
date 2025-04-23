from sage.graphs.graph_generators import graphs

def generateRandomGraph(n, p):
    return graphs.RandomGNP(n, p)