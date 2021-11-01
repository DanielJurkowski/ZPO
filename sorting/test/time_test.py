import random
import sort
from timeit import timeit

MAX_SAMPLE_VALUE = 1000
ELEMENTS = 1000


list_not_sorted = random.sample(range(0, MAX_SAMPLE_VALUE), ELEMENTS)
list_sorted = sorted(list_not_sorted)  # wykorzystanie wbudowanego sortowania pythona
list_reverse = list_sorted[::-1]  # odwrocenie listy
list_same_elements = [1] * 1000

t1_bubble = timeit("sort.bubblesort(list_not_sorted)", number=1000, globals=globals()) / 1000
t1_quick = timeit("sort.quicksort(list_not_sorted)",
                  number=1000, globals=globals()) / 1000

t2_bubble = timeit("sort.bubblesort(list_sorted)", number=1000, globals=globals()) / 1000
t2_quick = timeit("sort.quicksort(list_sorted)",
                  number=1000, globals=globals()) / 1000

t3_bubble = timeit("sort.bubblesort(list_reverse)", number=1000, globals=globals()) / 1000
t3_quick = timeit("sort.quicksort(list_reverse)",
                  number=1000, globals=globals()) / 1000

t4_bubble = timeit("sort.bubblesort(list_same_elements)", number=1000, globals=globals()) / 1000
t4_quick = timeit("sort.quicksort(list_same_elements)",
                  number=1000, globals=globals()) / 1000

print('Czas dla nieposortowanej listy')
print('bubblesort: ', t1_bubble)
print('quicksort: ', t1_quick, '\n')

print('Czas dla posortowanej listy')
print('bubblesort: ', t2_bubble)
print('quicksort: ', t2_quick,'\n')

print('Czas dla posortowanej-odwrotnej listy')
print('bubblesort: ', t3_bubble)
print('quicksort: ', t3_quick,'\n')

print('Czas dla listy tych samych elementów')
print('bubblesort: ', t4_bubble)
print('quicksort: ', t4_quick, '\n')


"""
Tabele 1000 elementow, 1000 razy, wyciągnieta średnia

Czas dla nieposortowanej listy
bubblesort:  0.048046824200000005
quicksort:  0.0009597695000000001 

Czas dla posortowanej listy
bubblesort:  5.2232799999998745e-05
quicksort:  0.0005044936999999976 

Czas dla posortowanej-odwrotnej listy
bubblesort:  0.061451488400000004
quicksort:  0.0005285135000000025 

Czas dla listy tych samych elementów
bubblesort:  5.144299999999191e-05
quicksort:  0.000955366600000005 
"""

