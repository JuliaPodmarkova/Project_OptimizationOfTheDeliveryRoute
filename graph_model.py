import networkx as nx
from math import radians, sin, cos, sqrt, atan2

def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def build_graph_from_points(points):
    G = nx.Graph()
    for p in points:
        G.add_node(p['id'], name=p['name'], coords=p['координаты'], вес=p['вес'], объем=p['объем'])
    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
            if i < j:
                dist = haversine(p1['координаты'], p2['координаты'])
                G.add_edge(p1['id'], p2['id'], weight=dist)
    return G