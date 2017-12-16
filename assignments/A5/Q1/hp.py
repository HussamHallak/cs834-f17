import sys
import os
import networkx as nx

def pagerank(G, alpha=0.85, personalization=None, iterations_count=11, nstart=None, weight='weight', dangling=None):
    if len(G) == 0:
        return {}

    if not G.is_directed():
        D = G.to_directed()
    else:
        D = G
    W = nx.stochastic_graph(D, weight=weight)
    N = W.number_of_nodes()
    if nstart is None:
        x = dict.fromkeys(W, 1.0 / N)
    else:
        s = float(sum(nstart.values()))
        x = dict((k, v / s) for k, v in nstart.items())

    if personalization is None:
        p = dict.fromkeys(W, 1.0 / N)
    else:
        missing = set(G) - set(personalization)
        if missing:
            raise nx.NetworkXError('Personalization dictionary '
                                'must have a value for every node. '
                                'Missing nodes %s' % missing)
        s = float(sum(personalization.values()))
        p = dict((k, v / s) for k, v in personalization.items())

    if dangling is None:
        dangling_weights = p
    else:
        missing = set(G) - set(dangling)
        if missing:
            raise nx.NetworkXError('Dangling node dictionary '
                                'must have a value for every node. '
                                'Missing nodes %s' % missing)
        s = float(sum(dangling.values()))
        dangling_weights = dict((k, v/s) for k, v in dangling.items())
    dangling_nodes = [n for n in W if W.out_degree(n, weight=weight) == 0.0]

    for _ in range(iterations_count):
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        danglesum = alpha * sum(xlast[n] for n in dangling_nodes)
        for n in x:
            for nbr in W[n]:
                x[nbr] += alpha * xlast[n] * W[n][nbr][weight]
            x[n] += danglesum * dangling_weights[n] + (1.0 - alpha) * p[n]

    return x

def hits(G, iterations_count=11, nstart=None, normalized=True):
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("hits() not defined for graphs with multiedges.")
    if len(G) == 0:
        return {},{}
    if nstart is None:
        h=dict.fromkeys(G,1.0/G.number_of_nodes())
    else:
        h=nstart
        s=1.0/sum(h.values())
        for k in h:
            h[k]*=s
    i=0
    while True: 
        if i >= iterations_count: break

        hlast=h
        h=dict.fromkeys(hlast.keys(),0)
        a=dict.fromkeys(hlast.keys(),0)
        for n in h:
            for nbr in G[n]:
                a[nbr]+=hlast[n]*G[n][nbr].get('weight',1)
        for n in h:
            for nbr in G[n]:
                h[n]+=a[nbr]*G[n][nbr].get('weight',1)
        s=1.0/max(h.values())
        for n in h: h[n]*=s
        s=1.0/max(a.values())
        for n in a: a[n]*=s

        i+=1
    if normalized:
        s = 1.0/sum(a.values())
        for n in a:
            a[n] *= s
        s = 1.0/sum(h.values())
        for n in h:
            h[n] *= s
    return h,a

if __name__ == '__main__':
    iterations_count = 5
    G = nx.Graph()
    G.add_nodes_from(range(1,8))
    G.add_edges_from([(1,2), (3,1), (3,2), (3,4), (5,4), (6,4)])

    pr = pagerank(G, iterations_count=iterations_count)

    print 'Pagerank Algorithm ({} iterations)'.format(iterations_count)
    print '============='
    print 'Pagerank values = {}'.format(pr)
	
    h, a = hits(G, iterations_count=iterations_count)

    print 'HITS Algorithm ({} iterations)'.format(iterations_count)
    print '============='
    print 'Hubs values = {}'.format(h)
    print 'Authorities values = {}'.format(a)
    print ''
