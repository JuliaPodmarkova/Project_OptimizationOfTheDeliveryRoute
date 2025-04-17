import networkx as nx

def find_shortest_path_dijkstra(G, start, end):

    try:
        path = nx.dijkstra_path(G, start, end, weight='weight')
        distance = nx.dijkstra_path_length(G, start, end, weight='weight')
        return path, distance
    except nx.NetworkXNoPath:
        print("Путь не найден.")
        return None, None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None, None

def find_shortest_path_bellman_ford(G, start, end):

    try:
        path = nx.bellman_ford_path(G, start, end, weight='weight')
        distance = nx.bellman_ford_path_length(G, start, end, weight='weight')
        return path, distance
    except nx.NetworkXNoPath:
        print("Путь не найден.")
        return None, None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None, None

def find_optimal_route_through_all_points(G, points_to_visit):

    try:
        subgraph = G.subgraph(points_to_visit)
        path = nx.approximation.traveling_salesman_problem(
            subgraph, cycle=False, weight='weight'
        )
        distance = sum(
            G[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1)
        )
        return path, distance
    except Exception as e:
        print(f"Ошибка TSP: {e}")
        return None, None

def find_best_path_tsp(G):

    try:
        nodes = list(G.nodes)
        if len(nodes) <= 1:
            return nodes, 0.0
        path = nx.approximation.traveling_salesman_problem(
            G, cycle=True, weight='weight'
        )
        distance = sum(
            G[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1)
        )
        return path, distance
    except Exception as e:
        print(f"Ошибка TSP: {e}")
        return None, None