% Define a dynamic predicate to store the list
:- dynamic(randomList/1).

% Here we create a new predicate named randomList/2
% The purpose of random list is to generate a list of random length and values
% N - The number of elements to be in the list
% List - The actual list to return
% We also use random/3, which will provide a random value to include as an element in List
% When N is greater than 0, generate a random number (X),
% and add it to the head of List. Recursively generate the rest
% of List with N1 elements.
randomList(0, []).
randomList(N, [X|List]) :-
    N > 0,
    random(1, 500, X),  % Change the range (1, 100) to your desired lower and upper bounds
    N1 is N - 1,
    randomList(N1, List).

% Store the list as a fact in the knowledge base
storeRandomList(N) :-
    randomList(N, List),
    assertz(randomList(List)).

/*swap the first two elements if they are not in order*/ 
 swap([X, Y|T], [Y, X | T]):- 
            Y =< X. 
/*swap elements in the tail*/ 
 swap([H|T], [H|T1]):- 
              swap(T, T1). 


/* bubbleSort sorts a list using the bubble sort algorithm.

   It repeatedly performs pairwise swaps to move the largest elements to the end of the list.
   When no swaps are needed, the list is considered sorted, and the sorted list is returned.

   - L: Input list to be sorted.
   - SL: Sorted list (output).
 */
bubbleSort(L,SL):- 
            swap(L, L1), % at least one swap is needed 
             !, 
             bubbleSort(L1, SL). 
bubbleSort(L, L). % here, the list is already sorted


/* ordered checks whether a list is ordered (sorted) in ascending order. */
ordered([]).
ordered([_X]).
ordered([H1, H2|T]):-
    H1 =< H2, 
    ordered([H2|T]).

/*  

   - E: The element to be inserted.
   - SL: The sorted list.
   - SLE: The resulting sorted list after insertion.
   
*/

/*Comment describing the 1st clause of insert …*/

insert(X, [],[X]). 
insert(E, [H|T], [E,H|T]):- 
      ordered(T),
      E =< H.

/*   If the target list SL is empty, the element E is simply inserted as the
   only element in the result SLE, effectively creating a new sorted list.*/

insert(E, [H|T], [H|T1]):- 
      ordered(T),
      insert(E, T, T1). 

/* insertionSort/2 sorts a list using the insertion sort algorithm.

   Parameters:
   - List: The input list to be sorted.
   - SORTED: The sorted list (output).
   
 */
insertionSort([], []). 
insertionSort([H|T], SORTED) :- 
          insertionSort(T, T1), 
          insert(H, T1, SORTED). 

/* mergeSort/2 sorts a list using the merge sort algorithm.

   Parameters:
   - List: The input list to be sorted.
   - SortedList: The sorted list (output).
 */
mergeSort([], []).    %the empty list is sorted 
mergeSort([X], [X]):-!.
mergeSort(L, SL):- 
             split_in_half(L, L1, L2), 
             mergeSort(L1, S1), 
             mergeSort(L2, S2),
             merge(S1, S2, SL). 


/* split_in_half divides a list into two halves.*/

intDiv(N,N1, R):- R is div(N,N1).
split_in_half([], _, _):-!, fail.
split_in_half([X],[],[X]). 
split_in_half(L, L1, L2):- 
             length(L,N), 
             intDiv(N,2,N1),
             length(L1, N1), 
             append(L1, L2, L). 

/*  merge/3 combines two sorted lists, S1 and S2, into a single sorted list S.
   Parameters:
   - S1: The first sorted list.
   - S2: The second sorted list.
   - S: The merged sorted list (output).
   
 */
merge([], L, L). % comment
merge(L, [],L).  % comment 
merge([H1|T1],[H2|T2],[H1| T]):-
	 H1 =<H2,
	merge(T1,[H2|T2],T).

merge([H1|T1], [H2|T2], [H2|T]):-
	H2 =< H1
	merge([H1|T1], T2, T).
   

/* split divides a list into two parts with respect to a pivot element. */

split(_, [],[],[]). 
 split(X, [H|T], [H|SMALL], BIG):- 
	H =< X, 
    split(X, T, SMALL, BIG).    
 
 split(X, [H|T], SMALL, [H|BIG]):-
    X =< H,
    split(X, T, FILLINHERE, BIG). 

/* quickSort/2 sorts a list using the quicksort algorithm.
   
   Parameters:
   - List: The input list to be sorted.
   - SortedList: The sorted list (output).

 */
quickSort([], []).
quickSort([H|T], LS):-
        split(H, T, SMALL, BIG)
        quickSort(SMALL, S), 
        quickSort(BIG, B), 
        append(S, [H|B], LS). 


hybridSort(LIST, bubbleSort, BIGALG, THRESHOLD, SLIST):-
	length(LIST, N), N=< THRESHOLD,      
      bubbleSort(LIST, SLIST).

hybridSort(LIST, insertionSort, BIGALG, THRESHOLD, SLIST):-
	length(LIST, N), N=<T,
      insertionSort(LIST, SLIST).

hybridSort(LIST, SMALL, mergeSort, THRESHOLD, SLIST):-
	length(LIST, N), N> THRESHOLD,      
	split_in_half(LIST, L1, L2),
    	hybridSort(L1, SMALL, mergeSort, THRESHOLD, S1),
    	hybridSort(L2, SMALL, mergeSort, THRESHOLD, S2),
    	merge(S1,S2, SLIST).

hybridSort([H|T], SMALL, quickSort, THRESHOLD, SLIST):-
	length(LIST, N), N > THRESHOLD,      
	split(H, T, L1, L2),
      quickSort(L1, S1), 
      quickSort(L2, S2),  
    	append(S1, [H|S2], SLIST).

hybridSort([H|T], SMALL, quickSort, THRESHOLD, SLIST):-
	FILLINHERE the full body of this clause


% Below are the queries to run against this Prolog code.
storeRandomList(50), % Generate a random list of length 50
randomList(StoredList), % Retrieve the stored list
write('List Unordered:'),
write(StoredList),
nl,
randomList(StoredList),
bubbleSort(StoredList, bubbleList),
write(bubbleList)
nl,
randomList(StoredList),
insertionSort(StoredList, insertionList),
write(insertionList)
nl,
randomList(StoredList),
mergeSort(StoredList, mergeList),
write(mergeList)
nl,
randomList(StoredList),
quickSort(StoredList, quickList),
write(quickList)
storeRandomList(50), % Generate a random list of length 50
randomList(StoredList), % Retrieve the stored list
write('List Unordered:'),
write(StoredList),
nl,
% Hybrid sort using bubbleSort as the small algorithm
hybridSort(List, bubbleSort, mergeSort, 5, SList),
write(SList),
nl,

% Hybrid sort using insertionSort as the small algorithm
hybridSort(List, insertionSort, mergeSort, 5, SList),
write(SList),
nl,

% Hybrid sort using mergeSort as the small algorithm
hybridSort(List, mergeSort, quickSort, 5, SList),
write(SList),
nl,
% Hybrid sort using quickSort as the small algorithm
hybridSort(List, quickSort, bubbleSort, 5, SList),
write(Slist)