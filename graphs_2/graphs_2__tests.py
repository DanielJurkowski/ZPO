# Daniel Jurkowski 407200

import unittest
import graphs_2
import networkx as nx


class FIND_MIN_TRAIL_TEST(unittest.TestCase):
    def test_find_min_trail(self):
        graph = graphs_2.load_multigraph_from_file('directed_graph_blank_lines.dat')
        trail = graphs_2.find_min_trail(graph, 1, 3)

        total = 0
        for entry in range(len(trail)):
            total += trail[entry].edge_weight

        self.assertEqual(total, nx.dijkstra_path_length(graph, 1, 3))
