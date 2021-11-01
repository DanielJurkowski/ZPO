# Daniel Jurkowski, 407200

from typing import List, Tuple


def quicksort(input_array: List[int]) -> List[int]:
    def quicksort_inplace(list_to_sort: List[int], start: int, stop: int) -> List[int]:
        i = start
        j = stop
        pivot = (start + stop) // 2  # wymagana liczba calkowita jako indeks listy

        pivot_value = list_to_sort[pivot]

        # implemntacja zgodnie z pseudokodem z skryptu, zmienione argumenty wejsciowe fun. quicksort

        while i < j:
            while list_to_sort[i] < pivot_value:
                i += 1
            while list_to_sort[j] > pivot_value:
                j -= 1

            if i <= j:
                list_to_sort[i], list_to_sort[j] = list_to_sort[j], list_to_sort[i]
                i += 1
                j -= 1

        if start < j:
            quicksort_inplace(list_to_sort, start, j)

        if i < stop:
            quicksort_inplace(list_to_sort, i, stop)

        return list_to_sort

    # plytka kopia w celu nie zamieniania listy wejsciowej
    input_array_copy = input_array[:]

    return quicksort_inplace(input_array_copy, 0, len(input_array_copy) - 1)


def bubblesort(input_array: List[int]) -> Tuple[List[int], int]:
    input_array_copy = input_array[:]
    n = len(input_array_copy)

    # implementacja na wzór pseudokodu z skryptu, dodana optymalizacja

    counter = 0

    while n > 1:
        swapped = False

        for i in range(1, n):
            counter += 1
            if input_array_copy[i - 1] > input_array_copy[i]:
                input_array_copy[i - 1], input_array_copy[i] = input_array_copy[i], input_array_copy[i - 1]
                swapped = True

        n -= 1

        if not swapped:
            break

    return input_array_copy, counter
