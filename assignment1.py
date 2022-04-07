'''
FIT2004 Assignment 1
Student Name: Amir Adrian Amir Hamzah
Student ID: 32281994
'''

# Problem 1: Wordle Problem

def word_sorter(word: str) -> str: # Big-O: O(N)
    '''
    Precondition: The length of the string word should eb at least 2 in order to utilize the function properly.
    -----
    Description: This function is a modified version of a count sort and it takes in a string (word) as input with only alphabets ranging from {a-z}. Using the alphabets' hex code we will then return a sorted form of that word.
    -----
    Input: String (word) of any length. Strings with length 0 or 1 gets returned immediately.
    Output: The input string sorted in lexicographical order.
    -----
    Big-O: T(N + 26) -> O(N) based on the length of the string N. Reason for 26 is because the alphabet_list has a constant length of 26 (Based on the assumption allowed).
    '''
    if len(word)==0 or len(word) == 1: # Return since nothing to sort.
        return word
    else:
        res = ""
    
        letter_counter = [0]*(26) # Create count array for the alphabets.
    
        # Count occurences of each letter
        # Big-O -> O(N) where N is the length of the word
        for i in range(len(word)):
            letter_counter[ord(word[i])-97] += 1 # Using the hex code value of the alphabet we can decide its position in the count array.

        # Build the output string
        # Big-O -> T(26) -> O(1) where it is going through the list of alphabets which has a length of 26 (a constant)
        for i in range(len(letter_counter)): 
            res += chr(i+97)*letter_counter[i] # For each alphabet add it to the string count_array[position] times.

        return res

def wordlist_sorter(wordlist: list[str]) -> list[str]: # Big-O: O(NM)
    """
    Pre-conditions: All strings in wordlist must have equal length. wordlist must contain at least two elements, or else it will not need to sort and simply return the given array.
    -----
    Description: This function takes in a list of words, all of equal length, and sorts them in lexicographical order.
    -----
    Input: A list of strings, all of equal length.
    -----
    Output: The same list of strings sorted in lexicographical order.
    -----
    Big-O: T(NM + 26M) -> O(NM) where N is the size of the input list and M is the length of any word of the list.
    """
    # Return if the length of list is 0 or 1 (No need to sort)
    if len(wordlist) == 0 or len(wordlist) == 1:
        return wordlist
    else:
        # This section is essentially radix sorting the list of words starting for the words' least significant letter (rightmost). Overall, this runs in Big-O O(NM) where N is the size of the list and M is the length of all the strings in the array.
        for index in range(len(wordlist[0])-1,-1): # Going through each column of letters. Loops M times.
            wordbank = [[]] * (26) # Use the alphabet count to create 'buckets' to store strings in based on the current index letter.
    
            for word in wordlist: # Goes through the wordlist and adds them in the buckets based on their letter in the current column. Loops N times
                wordbank[ord(word[index]) - 97] = wordbank[ord(word[index]) - 97] + [word]
            wordlist = [] # Emptying the input wordlist
    
            for i in range(len(wordbank)): # Goes through the buckets and ads each in alphabetical order back into the wordlist.
                wordlist = wordlist + wordbank[i]
    
        return wordlist

def word_wordlist_compare(wordlist: list[str],word: str) -> list[str]: # Big-O: O(NM)
    """
    Precondition: wordlist must have at least 1 element in order for the function to be useful.
    -----
    Description: Function takes in a list of strings and checks if the sorted version of the string matches the given word. If it does it will be added into the output string.
    -----
    Input: A list of strings with at least one element in it and a string word.
    Output: A list of strings that when sorted match the sorted version of the given word.
    -----
    Big-O: T(M + NM) -> O(NM) where N is the length of the list and M is the length of the largest word (In our case it is the same throughout).
    """

    res = []

    
    sorted_word = word_sorter(word) # Big-O: O(M) where M is the length of the string. Needed to compare with the words in the list.
    # Begin comparing with all words in the list.
    # This has the worst-case complexity of O(NM) because the word sorter is based on the length of the word (M) and we will be going through the whole wordlist which has the size N.
    for i in range(len(wordlist)): 
        word_sorted = word_sorter(wordlist[i])
        if word_sorted == sorted_word:
            res += [wordlist[i]]
    return res

def trainer(wordlist: list[str],word: str,marker: list[int]) -> list[str]: # Big-O: O(NM)
    """
    Pre-conditions: The wordlist cannot be empty. The length of the word, marker and all words in wordlist must be equal. Marker can only contain 1s and 0s.
    ----
    Description: This function takes a list of strings (wordlist) of size N with strings of length M, a string (word) of length M, and a list of markers (0s and 1s) of size M. It returns a, potentially, smaller list of words that are deemed to be the possible correct answer based on the guessed word and marker.
    ----
    Input: A list of strings of size N where all strings has a length of M (wordlist), a string of length M (word) and a list of integers 0 or 1 of size M (marker).
    Output: A list of strings which are a subset of wordlist which are the potential answers to out Wordle problem.
    ----
    Big-O: T(3NM) -> O(NM) where N is the size of the input wordlist and M is the length of the guessed word/size of marker/length of all words in wordlist. This leads to having the worst-case complexity of O(NM). 
    """
    if len(wordlist) == 0: # If the wordlist is empty, simply return it.
        return wordlist
    else:
        wordlist = wordlist_sorter(wordlist) # Sort the wordlist. Big-O: O(NM) where N is the size of wordlist and M is the length of the strings in wordlist. Big-O: O(NM)
    
        half_res = word_wordlist_compare(wordlist, word) # Prune the list of words to contain only the strings that have the same letter count as the given word. Big-O O(NM)
        res = []

        # This segment is to further prune the remaining words based on the marker and the current letter on that marker spot. 
        # #This has a complexity of worst-case O(NM) where N is the size of the wordlist and M is the size of the marker (also the length of the any word in wordlist).
        for currentword in half_res: 
            answer = True
            for M in range(len(currentword)): # Compare marker with current letter in guessed word and word in wordlist.
                if marker[M] == 1 and currentword[M] != word[M]: # If marker is 1, but letters are not the same. Word is not possible.
                    answer = False
                    break
                elif marker[M] == 0 and currentword[M] == word[M]: # If marker is 0, but the letters are the same. Word is not possible.
                    answer = False
                    break
            if answer == True: # If word is possible, add to final output list.
                res+=[currentword]
    
        return res

# Problem 2: Find Local Maximum in NxN Grid

def local_maximum(M: list[list[int]]) -> list[int]:
    """
    Pre-Conditions: All numbers in matrix must be unique. The matrix is an NxN matrix. The matrix cannot be empty resulting in a 0x0 matrix.
    ----
    Description: Taking in the matrix, this function will give the position of one of the matrix's local maximum.
    ----
    Input: An NxN matrix with distinct number values.
    Output: A list containing the position of the local maximum in the matrix using row and column coordinates (x and y).
    ----
    Big-O: T(N+N) -> O(N) worst-case complexity where N is the length of the matrix in 1st dimension.
    """
    if M == [[]]: # If it is an empty matrix (i.e. 0X0) simply return an empty list.
        return []
    else:
        # This segment is to find the maximum in the middle row and middle column.= of the matrix
        middle_col = len(M)//2
        middle_row = len(M)//2
        max_value_row = M[middle_row][0]
        max_value_row_index = [middle_row,0]
        max_value_col = M[0][middle_col]
        max_value_col_index = [0,max_value_col]
        for i in range(len(M)): # Big-O O(N) where N is the length of the matrix.
            if M[middle_row][i] > max_value_row:
                max_value_row = M[middle_row][i]
                max_value_row_index = [middle_row,i]
            if M[i][middle_col] > max_value_col:
                max_value_col = M[i][middle_col]
                max_value_col_index = [i,middle_col]
        if max_value_row > max_value_col:
            row = max_value_row_index[0]
            col = max_value_row_index[1]
        else:
            row = max_value_col_index[0]
            col = max_value_col_index[1]
        
        return find_next_element(M, row, col) # This will check the neighbours of our current maximmum value and if there are others we will check their neighbours too. Eventually it will return the local maximum position. Big-O: O(N)

def find_next_element(M, row: int, col: int) -> list:
    """
    Description: Given a matrix and a row and column position it will check if its adjacent neighbours are larger than it. If it is then we recursively check their neighbour too. If none of the neighbours are larger than the given position, it will return that position.
    ----
    Input: An NxN matrix with distinct number values, 2 integers for 
    ----
    Output: A list containing the position of the local maximum in the matrix using row and column using (x,y) coordinates.
    ----
    Big-O: O(N) worst-case complexity where N is the length of the matrix (1 dimensional).
    """

    # Check if no neightbour is larger than current number
    if (col == 0 or M[row][col-1] < M[row][col]) and (col == len(M)-1 or M[row][col+1] < M[row][col]) and (row == 0 or M[row-1][col] < M[row][col]) and (row == len(M)-1 or M[row+1][col]<M[row][col]):
        return [row,col]
    # Find next larger neighbour. If such neighbour exists, recall the function with the respective row and column of that neighbour.
    elif col > 0 and M[row][col-1] > M[row][col]:
        return find_next_element(M,row,col-1)
    elif col < (len(M)-1) and M[row][col+1] > M[row][col]:
        return find_next_element(M,row,col+1)
    elif row > 0 and M[row-1][col] > M[row][col]:
        return find_next_element(M,row-1,col)
    elif row < (len(M)-1) and M[row+1][col] > M[row][col]:
        return find_next_element(M,row+1,col)