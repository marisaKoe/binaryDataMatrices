'''
Created on 19.07.2017

@author: marisakoe
'''
from numpy import *



def nw(x,y,lodict,gp1,gp2):
    """
    Needleman-Wunsch algorithm for pairwise string alignment
    with affine gap penalties.
    'lodict' must be a dictionary with all symbol pairs as keys
    and match scores as values.
    gp1 and gp2 are gap penalties for opening/extending a gap.
    Returns the alignment score and one optimal alignment.
    """
    #length of the words
    n,m = len(x),len(y)
    dp = zeros((n+1,m+1))
    pointers = zeros((n+1,m+1),int)
    for i in xrange(1,n+1):
        dp[i,0] = dp[i-1,0]+(gp2 if i>1 else gp1)
        pointers[i,0]=1
    for j in xrange(1,m+1):
        dp[0,j] = dp[0,j-1]+(gp2 if j>1 else gp1)
        pointers[0,j]=2
    for i in xrange(1,n+1):
        for j in xrange(1,m+1):
            match = dp[i-1,j-1]+lodict[x[i-1],y[j-1]]
            insert = dp[i-1,j]+(gp2 if pointers[i-1,j]==1 else gp1)
            delet = dp[i,j-1]+(gp2 if pointers[i,j-1]==2 else gp1)
            dp[i,j] = max([match,insert,delet])
            pointers[i,j] = argmax([match,insert,delet])
    alg = []
    i,j = n,m
    while(i>0 or j>0):
        pt = pointers[i,j]
        if pt==0:
            i-=1
            j-=1
            alg = [[x[i],y[j]]]+alg
        if pt==1:
            i-=1
            alg = [[x[i],'-']]+alg
        if pt==2:
            j-=1
            alg = [['-',y[j]]]+alg
    return dp[-1,-1],alg,array([''.join(x) for x in array(alg).T])


########################################## ngrams ##############################################

def get_unigrams(string):
    '''
    Takes the string and returns s list of unigrams
    :param string: a word
    :return list: list of all unigrams
    '''
    return [string[i] for i in xrange(len(string))]


def get_bigrams(string):
    '''
    Takes a string and returns a list of bigrams
    :param string: a word
    :return list: a list with all bigrams
    '''
    #s = string.lower()
    return [string[i:i+2] for i in xrange(len(string) - 1)]

def get_gappyBigrams(string):
    '''
    Takes a string and return a list of gappy bigrams (skipping one char)
    :param string: a word
    :return list: a list of all gappy bigrams
    '''
    return [string[i]+string[i+2] for i in xrange(len(string) - 2)]


def string_similarity(str1, str2):
    '''
    Perform bigram comparison between two strings
    Returns a list with all matches
    
    #return a percentage match in decimal form
    :param str1: first word
    :param str2: second word
    '''
    #print str1, str2
    pairs1 = get_bigrams(str1)
    pairs2 = get_bigrams(str2)
    #print pairs1, pairs2
    uni1 = get_unigrams(str1[1:-1])
    uni2 = get_unigrams(str2[1:-1])
    #print uni1, uni2
    gappyPairs1 = get_gappyBigrams(str1)
    gappyPairs2 = get_gappyBigrams(str2)
    #print gappyPairs1, gappyPairs2
    matches = []
    #check bigram matches
    for x in pairs1:
        for y in pairs2:
            if x==y:
                matches.append(x)
    #check unigram matches
    for a in uni1:
        for b in uni2:
            if a==b:
                matches.append(a)
    #check gappy bigram matches
    for c in gappyPairs1:
        for d in gappyPairs2:
            if c==d:
                matches.append(c)
    
    #print matches           
    return matches
    
    
    '''calculates the precantage match
    union  = len(pairs1) + len(pairs2)+ len(uni1) + len(uni2)
    hit_count = 0
    for x in pairs1:
        for y in pairs2:
            if x == y:
                hit_count += 1
                break
    for a in uni1:
        for b in uni2:
            if a==b:
                hit_count += 1
                break
    #print hit_count
    return (2.0 * hit_count) / union '''

if __name__ == '__main__':
    pass