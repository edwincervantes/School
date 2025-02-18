# Edwin Cervantes
# AI 6033
 
def quicksort(array):
    """
    An Algorithm to organize an array from low -> high via Quick Sort
    This utilizes recursion to sort each portion of the list

    array: The array to sort
    """
    less_than_pivot = []
    equal_to_pivot = []
    greater_than_pivot = []

    # If the array is of length 1 or less, just return, no sorting needed
    if len(array) > 1:
        # Use the first element of the array as the pivot
        pivot = array[0]
        for x in array:
            if x < pivot:
                less_than_pivot.append(x)
            elif x == pivot:
                equal_to_pivot.append(x)
            elif x > pivot:
                greater_than_pivot.append(x)
        return quicksort(less_than_pivot)+equal_to_pivot+quicksort(greater_than_pivot)  # Just use the + operator to join lists
    else:  
        return array

def bubblesort(array):
    """
    An Algorithm to organize an array from low -> high via Bubble Sort
    This algorithm compares two consecutive elements in the array, and if they are out of order,
    they get swapped, if not continue to the next element.

    array: The array to sort
    """
    # Get the length of the array
    l = len(array)
    for i in range(l-1):
        for j in range(0, l-i-1):
            # If true, swap the elements of the awway
            if array[j] > array[j + 1]:
                a = array[j]
                b = array[j + 1]
                array[j + 1] = a
                array[j] = b

    return array
 
array = [3, 4, 54, -6, -2, 0, 8, 12, 36, 24, -42]
print("Unsorted Array")
print(array)

print('\n')
 
print('Sorted Array utilizing Quick Sort:')
print(quicksort(array))

print('\n')

print('Sorted Array utilizing Bubble Sort:')
print(bubblesort(array))


"""
Unsorted Array
[3, 4, 54, -6, -2, 0, 8, 12, 36, 24, -42]


Sorted Array utilizing Quick Sort:
[-42, -6, -2, 0, 3, 4, 8, 12, 24, 36, 54]


Sorted Array utilizing Bubble Sort:
[-42, -6, -2, 0, 3, 4, 8, 12, 24, 36, 54]
"""