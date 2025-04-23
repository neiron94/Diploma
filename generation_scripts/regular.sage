from sage.graphs.graph_generators import graphs

def generateRegular(d, n):
    if (d*n) % 2 != 0:
        raise ValueError("degree * n must be even!")
    return graphs.RandomRegular(d, n)