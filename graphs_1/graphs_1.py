# Daniel Jurkowski 407200

from typing import List, Dict


def adjmat_to_adjlist(adjmat: List[List[int]]) -> Dict[int, List[int]]:
    adj_list = {}
    edges = [[] for x in range(0, len(adjmat))]  # utworzenie pustej listy złożonej z list wierzchołków

    for i, row in enumerate(adjmat, 1):
        for j, element in enumerate(row, 1):
            if element != 0:
                if element > 1:
                    for x in range(0, element):
                        edges[i - 1].append(j)
                else:
                    edges[i - 1].append(j)

        if sum(row) != 0:  # sprawdzenie czy wiersz nie jest zerowy
            adj_list[i] = edges[i - 1]

    return adj_list


def dfs_recursive(G: Dict[int, List[int]], s: int) -> List[int]:

    # implementacja zgodnie z pseudokodem

    def dfs_recursive_inplace(Graph: Dict[int, List[int]], vertex: int, visited=None) -> List[int]:
        if visited is None:
            visited = []

        visited.append(vertex)

        for u in Graph[vertex]:
            if u not in visited:
                visited = dfs_recursive_inplace(G, u, visited)

        return visited

    return dfs_recursive_inplace(G, s)


def dfs_iterative(G: Dict[int, List[int]], s: int) -> List[int]:

    # implementacja zgodnie z pseudokodem

    visited = []

    stack = [s]

    while stack:
        v = stack.pop()

        if v not in visited:
            visited.append(v)

            for u in reversed(G[v]):
                stack.append(u)

    return visited


def is_acyclic(G: Dict[int, List[int]]) -> bool:

    # wykorzystanie DFS do sprawdzenia czy graf posiada cykl

    def dfs(Graph: Dict[int, List[int]], vertex: int, visited=None) -> bool:

        if visited is None:
            visited = [vertex]

        if vertex in Graph:
            for v in Graph[vertex]:
                if v in visited:
                    return True
                if dfs(Graph, v, visited[:]):
                    return True
        else:
            return False

    for n in G:
        if dfs(G, n):
            return False

    else:
        return True
