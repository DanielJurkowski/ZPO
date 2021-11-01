import unittest
import graphs_1


class ADJMAT_TO_ADJLIST_TEST(unittest.TestCase):
    def test_adjmat_to_adjlist(self):
        a = [
            [0, 1, 0, 1],
            [0, 1, 1, 3],
            [1, 2, 0, 2],
            [1, 1, 1, 1]
        ]

        b = {
            1: [2, 4],
            2: [2, 3, 4, 4, 4],
            3: [1, 2, 2, 4, 4],
            4: [1, 2, 3, 4]
        }

        c = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]

        d = {
            1: [1],
            2: [2],
            3: [3]
        }

        e = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 3]
        ]

        f = {
            3: [3, 3, 3]
        }

        self.assertEqual(graphs_1.adjmat_to_adjlist(a), b)
        self.assertEqual(graphs_1.adjmat_to_adjlist(c), d)
        self.assertEqual(graphs_1.adjmat_to_adjlist(e), f)


class DFS_TRAVERSE_TEST(unittest.TestCase):
    def test_dfs_traverse(self):
        G = {
            1: [2, 3, 5],
            2: [1, 4, 6],
            3: [1, 7],
            4: [2],
            5: [1, 6],
            6: [2, 5],
            7: [3]
        }

        self.assertEqual(graphs_1.dfs_recursive(G, 1), [1, 2, 4, 6, 5, 3, 7])
        self.assertEqual(graphs_1.dfs_iterative(G, 1), [1, 2, 4, 6, 5, 3, 7])


class DFS_ACYCLIC_TEST(unittest.TestCase):
    def test_dfs_acyclic(self):
        self.assertEqual(graphs_1.is_acyclic({1: [2, 3], 3: [4]}), True)
        self.assertEqual(graphs_1.is_acyclic({1: [2], 2: [3], 3: [1]}), False)
        self.assertEqual(graphs_1.is_acyclic({2: [1, 3], 3: [2]}), False)
        self.assertEqual(graphs_1.is_acyclic({1: [2], 3: [2, 4], 4: [3]}), False)
        self.assertEqual(graphs_1.is_acyclic({1: [2, 3], 2: [4], 3: [4]}), True)
        self.assertEqual(graphs_1.is_acyclic({1: [2, 3], 2: [3]}), True)
        self.assertEqual(graphs_1.is_acyclic({1: [2], 2: [3], 3: [1, 4]}), False)

