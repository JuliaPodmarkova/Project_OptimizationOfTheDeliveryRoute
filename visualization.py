import matplotlib.pyplot as plt
import networkx as nx

def plot_graph(G):

    pos = {node: (data['coords'][1], data['coords'][0]) for node, data in G.nodes(data=True)}
    labels = {node: data['name'] for node, data in G.nodes(data=True)}
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=600, font_size=8)
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    plt.title("Граф пунктов доставки")
    plt.show()

def plot_route(G, path, show_weight=True):

    if not path or len(path) < 2:
        print("Маршрут слишком короткий для отображения.")
        return
    pos = {node: (data['coords'][1], data['coords'][0]) for node, data in G.nodes(data=True)}
    labels = {node: data['name'] for node, data in G.nodes(data=True)}
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightgrey', node_size=600, font_size=8)
    nx.draw_networkx_labels(G, pos, labels, font_size=10)

    route_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='r', width=2)

    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange', node_size=700)

    if show_weight:
        edge_labels = {(u, v): f"{G[u][v]['weight']:.1f}" for u, v in route_edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Оптимальный маршрут")
    plt.show()