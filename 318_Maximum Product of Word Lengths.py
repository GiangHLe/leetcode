# Bitmask method

import string

# encode whole alphabet
ch_to_bit = {ch: 1<<i for i,ch in enumerate(string.ascii_lowercase)}
# Example: a: 0000...0001
#          b: 0000...0010
# if 'ab': 0000...0011

def Compact(words): # remove the duplicate, take the longer
    '''
    Example: ["a","aa","ab","abc","d","cd","bcd","abcd"]
        Between "a" and "aa", Compact will remove "a", keep "aa"
        Output will be: {1: 2, 3: 2, 7: 3, 8: 1, 12: 2, 14: 3, 15: 4} 
            where 1 is 000...0001 of 'a', 3 is 000...0011 of 'ab' and so on
    '''
    # Word as int ==> wint
    wint_to_len = {}
    for w in words:
        w_n = len(w)
        wint = sum([ch_to_bit[ch] for ch in set(w)]) # turn on the bit vector
        # among duplicates, only the largest length is used.
        wint_to_len[wint] = max(w_n, wint_to_len.get(wint, 0))

    return wint_to_len


def CompareUntilUseless(wint_to_len):
    max_product = 0

    # Sorting the list allows skipping entries too small to make a difference
    wint_len_pairs = [(wint,w_len) for wint,w_len in wint_to_len.items()]
    wint_len_pairs.sort(reverse=True, key=lambda x: x[1])  # x[1] is length

    num_pairs = len(wint_len_pairs)
    for i in range(0, num_pairs - 1):
        wint,w_len = wint_len_pairs[i]
        # All remaining entries are size w_len or smaller
        if w_len * w_len <= max_product: # because it is already sort so cannot get final result which is square of an element length
            break
        for cmpint,cmp_len in wint_len_pairs[i+1:]:
            if wint & cmpint == 0: # check if is there any bit is the same
                max_product = max(max_product, w_len * cmp_len)

    return max_product


class Solution:
    def maxProduct(self, words):
        return CompareUntilUseless(Compact(words))