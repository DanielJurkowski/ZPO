# Daniel Jurkowski 407200
from typing import List, Set, Dict, NamedTuple
import networkx as nx
from enum import Enum, auto

Distance = int
VertexID = int
EdgeID = int


class vertex_distance(NamedTuple):
    vertex_id: VertexID
    distance: Distance


class TrailSegmentEntry(NamedTuple):
    start_vertex: VertexID
    end_vertex: VertexID
    edge_id: EdgeID
    edge_weight: float


AdjList = Dict[VertexID, List[VertexID]]
Trail = List[TrailSegmentEntry]


def neighbors(adjlist: AdjList, start_vertex_id: VertexID,
              max_distance: Distance) -> Set[VertexID]:
    # typ wyliczeniowy dla kolorów wierzchołków
    class COLOR(Enum):
        WHITE = auto()  # nieodwiedzony
        GREY = auto()  # odwiedzony lecz sąsiednie wierzchołki nie
        BLACK = auto()  # odwiedzony

    # zwracany zbiór
    neighbors_list = set()

    # słownik wierzchołek: kolor
    color = {}

    # przypisanie koloru białego do każdego występującego wierzchołka
    for vertex in adjlist:
        color[vertex] = COLOR.WHITE
        for v in adjlist[vertex]:
            color[v] = COLOR.WHITE

    # oznaczenie początkowego wierzchołka
    color[start_vertex_id] = COLOR.GREY

    # kolejka
    queue = [vertex_distance(vertex_id=start_vertex_id, distance=0)]

    while queue:
        vertex_id, current_distance = queue.pop(0)

        # działanie tylko dla określonej odległości od wierzchołka początkowego
        if current_distance > max_distance:
            break

        # dodawanie wierzchołka do listy sąsiadów
        if vertex_id != start_vertex_id:
            neighbors_list.add(vertex_id)

        # implementacja zgodnie z pseudokodem
        if vertex_id in adjlist:
            for v_id in adjlist[vertex_id]:
                if color[v_id] == COLOR.WHITE:
                    color[v_id] = COLOR.GREY
                    queue.extend([vertex_distance(vertex_id=v_id, distance=current_distance + 1)])

            color[vertex_id] = COLOR.BLACK

    return neighbors_list


def load_multigraph_from_file(filepath: str) -> nx.MultiDiGraph:
    # otwarcie pliku
    with open(filepath, 'r') as file:
        file_data = file.readlines()  # czyta linie, pomijając przerwy

    # utworzenie grafu
    graph = nx.MultiDiGraph()

    # wczytanie wierzchołków wraz z wagami krawędzi
    nx.read_edgelist(file_data, create_using=graph, nodetype=VertexID, data=(('weight', float),))

    return graph


def find_min_trail(g: nx.MultiDiGraph, v_start: VertexID, v_end: VertexID) -> Trail:
    trail = []

    # znalezienie najkrótszej drogi oraz zamienienie na format (start, koniec) dla jednej krawędzi
    dijkstra_path_nodes = nx.dijkstra_path(g, v_start, v_end)
    edges_in_path = list(zip(dijkstra_path_nodes[0:], dijkstra_path_nodes[1:]))

    for (s_v, e_v) in edges_in_path:
        if len(g[s_v][e_v]) > 1:  # sprawdzenie czy występuje wiele krawędzi dla połączenie dwóch wierzchołków
            edge_weights = {}

            # przypisanie wagi dla danej krawędzi
            for edge_id in g[s_v][e_v]:
                edge_weights[edge_id] = g[s_v][e_v][edge_id]['weight']

            # znalezienie krawędzi o najmniejszej wadze
            min_edge = min(edge_weights, key=edge_weights.get)

            trail.extend([TrailSegmentEntry(start_vertex=s_v, end_vertex=e_v, edge_id=min_edge,
                                            edge_weight=edge_weights[min_edge])])

        else:
            for edge in g[s_v][e_v]:
                trail.extend([TrailSegmentEntry(start_vertex=s_v, end_vertex=e_v, edge_id=edge,
                                                edge_weight=g[s_v][e_v][edge]['weight'])])

    return trail


def trail_to_str(trail: Trail) -> str:
    str_trail = ''

    sum_of_weights = 0

    # znalezienie całkowitej wagi drogi oraz dodanie wierzchołków do stringa
    for entry in range(len(trail)):
        sum_of_weights += trail[entry].edge_weight
        str_trail += f'{trail[entry].start_vertex} -[{trail[entry].edge_id}: {trail[entry].edge_weight}]-> '

    str_trail += f'{trail[-1].end_vertex}  (total = {sum_of_weights})'  # dodanie całkowitej wagi drogi do stringa

    return str_trail
