# Pozostaw ten plik pusty, ew. wykorzystaj do własnych testów.

import unittest
import sort


class SortingTest(unittest.TestCase):
    def test_quicksort(self):
        unsorted_list = [38, 14, 1, 74, 24, 91, 63, 94, 47, 28, 25, 102,  73]
        sorted_list = [1, 14, 24, 25, 28, 38, 47, 63, 73, 74, 91, 94, 102]

        self.assertEqual(sort.quicksort(unsorted_list), sorted_list)  # sprawdzanie sortowania
        self.assertEqual(unsorted_list, [38, 14, 1, 74, 24, 91, 63, 94, 47, 28, 25, 102, 73])  # nie zmienianie listy
        # wejsciowej

    def test_bubblesort(self):
        unsorted_list = [38, 14, 1, 74, 24, 91, 63, 94, 47, 28, 25, 102, 73]
        sorted_list = [1, 14, 24, 25, 28, 38, 47, 63, 73, 74, 91, 94, 102]

        self.assertEqual(sort.bubblesort(unsorted_list)[0], sorted_list)
        # liczba porownan bedzie zalezala od opytmalizacji kodu
        self.assertEqual(isinstance(sort.bubblesort(unsorted_list)[1], int), True)
        self.assertEqual(isinstance(sort.bubblesort(unsorted_list), tuple), True)
        self.assertEqual(unsorted_list, [38, 14, 1, 74, 24, 91, 63, 94, 47, 28, 25, 102, 73])

