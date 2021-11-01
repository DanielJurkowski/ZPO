import unittest
import graphs_2
import networkx as nx


class NEIGHBORS_TEST(unittest.TestCase):
    def test_neighbors(self):
        G = {
            1: [2, 4],
            2: [3],
            4: [5],
            5: [2, 6],
            7: [1]
        }

        G_1 = {
            1: [2, 3, 4],
            2: [1, 5, 6],
            3: [1, 7],
            4: [1, 6],
            5: [2],
            6: [2, 4],
            7: [3]
        }

        a = {2, 4}

        b = {2, 3, 4, 5}

        c = {2, 3, 4, 5, 6}

        d = {2, 3, 4}

        e = {2, 3, 4, 5, 6, 7}

        self.assertEqual(graphs_2.neighbors(G, 1, 1), a)
        self.assertEqual(graphs_2.neighbors(G, 1, 2), b)
        self.assertEqual(graphs_2.neighbors(G, 1, 3), c)
        self.assertEqual(graphs_2.neighbors(G_1, 1, 1), d)
        self.assertEqual(graphs_2.neighbors(G_1, 1, 2), e)


class MULTI_GRAPH_TEST(unittest.TestCase):
    def test_load_from_file(self):
        G = nx.MultiDiGraph()
        G.add_weighted_edges_from([(1, 2, 0.5), (2, 3, 0.4), (2, 3, 0.3), (1, 3, 1.0)])

        G_test = graphs_2.load_multigraph_from_file('./directed_graph_blank_lines.dat')
        G_test_1 = graphs_2.load_multigraph_from_file('./directed_graph.dat')

        self.assertTrue(nx.is_isomorphic(G, G_test))
        self.assertTrue(nx.is_isomorphic(G, G_test_1))

    def test_find_min_trail(self):
        graph = graphs_2.load_multigraph_from_file('./directed_graph_blank_lines.dat')
        trail = graphs_2.find_min_trail(graph, 1, 3)
        trail_equal = [graphs_2.TrailSegmentEntry(start_vertex=1, end_vertex=2, edge_id=0, edge_weight=0.5),
                       graphs_2.TrailSegmentEntry(start_vertex=2, end_vertex=3, edge_id=1, edge_weight=0.3)]
        self.assertEqual(trail, trail_equal)

    def test_find_min_trail_total_weight(self):
        graph = graphs_2.load_multigraph_from_file('./test.dat')
        trail = graphs_2.find_min_trail(graph, 1, 4)

        total = 0
        for entry in range(len(trail)):
            total += trail[entry].edge_weight

        self.assertEqual(total, nx.dijkstra_path_length(graph, 1, 4))

    def test_trail_to_string(self):
        graph = graphs_2.load_multigraph_from_file('./directed_graph_blank_lines.dat')
        trail = graphs_2.find_min_trail(graph, 1, 3)
        trail_string = graphs_2.trail_to_str(trail)
        self.assertEqual(trail_string, '1 -[0: 0.5]-> 2 -[1: 0.3]-> 3  (total = 0.8)')
