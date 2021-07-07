'''
Created on 19.07.2017

@author: marisakoe

creates a data matrix with nw alignments and ngrams for each concepts
matrices can be used as input to bayesian tree reconstruction
'''
import codecs
import itertools as it
from collections import defaultdict
from numpy import *

from computation_methods import nw, string_similarity
from write_output import write_dataMatrix

unique_chars = []
gp1 = -2.49302792222
gp2 = -1.70573165621

lodict={}

def main_ngramsNW(data_dict, pmi, sounds, dataName):
    '''
    Get the ngrams from the strings which where aligned by NW before (they have gaps in them).
    Creates a data matrix for each concept and saves it in a folder.
    :param data: data file
    '''
    d = nw_align(data_dict,pmi, sounds)
    #for each concept in the dictionary
    for concept in d:
        alg_dict = defaultdict()
        list_langs=[]
        #get the dictionray with all languages
        langs_dict = d[concept]
        #get all the languages in one list
        list_langPairs = langs_dict.keys()
        #make language pair for each possible combination
        for pair in list_langPairs:
            l1, l2 = pair 
            if not l1 in list_langs:
                list_langs.append(l1)
            elif not l2 in list_langs:
                list_langs.append(l2)

            #get the words
            word_list = langs_dict[pair]
            if len(word_list)==1:
                match = string_similarity("^"+word_list[0][0]+"$", "^"+word_list[0][1]+"$")
                alg_dict[pair] = match
            else:
                match_list = []
                for words in word_list:
                    match_pair = string_similarity("^"+words[0]+"$", "^"+words[1]+"$")
                    match_list.append(match_pair)
                match = list(it.chain(*match_list))
                alg_dict[pair] = match
        print "concept: ", concept
        print "number of matches: ", len(alg_dict.values())
        create_dataMatrix(concept, list_langs, alg_dict,sounds, dataName)
        
            
def create_dataMatrix(concept, list_langs, alg_dict, sounds, dataName):
    '''
    creates a dictionary of dictionary which is the data matrix, key=language value=dictionary with key=soundpair value=0 (if not present) or 1 (if present)
    we can do it in two ways:
    1. compute a matrix with all possible sounds from ASJP
    2. compute a reduced matrix only with the sounds possible in the example -> this is done right now
    :param concept: the number of the concpet for storing the data in a file
    :param list_sounds: the list of all ASJP sounds
    :param sounds_gap: the list of all ASJP sounds plus a gap symbol
    :param list_langs: the list of the languages in the sample
    :param alg_dict: the dictionary for the alignments key=tuple with the language pair value=tuple of alignment score and a list of lists with the character alignments
    '''
    
    #reads the file with the 41 sounds of ASJP
    f = open('input/'+sounds)
    sounds = [x.strip() for x in f.readlines()]
    f.close()
    sounds.append("^")
    sounds.append("$")
    sounds.append("-")
    #create a list for all pairs of sounds  
    sound_pairs = [p[0]+p[1] for p in it.combinations(sounds,r=2)]
    #combinde all sounds (unigrams and bigrams) into a list
    all_sounds = sounds+sound_pairs
    #initialize the data matrix
    dataMatrix = defaultdict(dict)
    ####needed if we want to compute the matrix with all possible sound pairs
#     for langs in list_langs:
#         #for each pair in the list
#         for pair in all_sounds:
#             #set the default value to 0
#             dataMatrix[langs][pair] = "0"
     
     
    #for each lang in the list (only needed for the reduced matrix)
    for langs in list_langs:
        dataMatrix[langs]=defaultdict(int)
    #only needed for the reduced matrix
    overall_soundpairs=[]
    #for lang pairs and alignments in the alignment dictionary
    for langs, algs in alg_dict.items():
        ##get the first and the second language
        l1,l2 = langs
         
        #get the alignment score and the character alignment in a list of lists
        matches = algs
        #initialize a new list for storing the sound pairs of the alignments
        new_alg=[]
        #for each sound alignment in the list
        for a in matches:
            #check if string is in the list of sound pairs and append it to the new list
            if a in all_sounds:
                new_alg.append(a) 
            #otherwise reverse the string, check it again and append it to the list
            else:
                a = a[::-1]
                if a in all_sounds:
                    new_alg.append(a)
         
        #for each sound alignment in the new list
        for a1 in new_alg:
            #set the value in the dictionary of dicts to 1
            dataMatrix[l1][a1] = "1"
            dataMatrix[l2][a1] = "1"
            #only needed in the reduced matrix to get the list of all sound pairs in the concept
            if not a1 in overall_soundpairs:
                overall_soundpairs.append(a1)
     
    #only needed for the reduced matrix to fill the matrix with 0
    for lang,pairs in dataMatrix.items():
        list_pairs = pairs.keys()
        for sound in overall_soundpairs:
            if not sound in list_pairs:
                pairs[sound]="0"
    
    
    #create an output file for storing the matrix
    fout1 = "output/"+dataName+"/data_matrices_ngramsNW/"+"dataMatrix_"+concept+".nex"
    #call the function to write the data matrix to a file
    write_dataMatrix(fout1, dataMatrix,len(list_langs),len(overall_soundpairs))
    
    
def nw_align(data_dict,pmi, sounds):
    '''
    main function to create an alignment dictionary and give it back to a helper function to create a data matrix for the alignments
    :param data: the name of the data file
    '''
    #reads the file with the 41 sounds of ASJP
    f = open("input/"+sounds)
    sounds = array([x.strip() for x in f.readlines()])
    f.close()
    
    #create two lists, one where the gap symbol is added (sounds_gaps), which is needed for the data matrix 
    list_sounds = []
    sounds_gap = []
    for s in sounds:
        new_s = s.tostring()
        list_sounds.append(new_s)
        sounds_gap.append(new_s)
    sounds_gap.append("-")

    #reads the log odds scores for the whole word languages
    f = open('input/'+pmi,'r')
    l = f.readlines()
    f.close()
    logOdds = array([x.strip().split() for x in l],double)
    
    #assigns the log odds to the sound pairs to create the lodict
    for i in xrange(len(sounds)):#Initiate sound dictionary
        for j in xrange(len(sounds)):
            lodict[sounds[i],sounds[j]] = logOdds[i,j]




    #for each concept in the dictionary, count is just for controlling the process
    count = 0
    overall_algDict = defaultdict()
    for concept,langs in data_dict.items():
        count += 1
        #initialize the alignment dictionary
        alg_dict = defaultdict()
        #initializing the list of languages
        langs_list = []
        #for each language in the dictionary, append it to a list
        for lang in langs:
            if lang not in langs_list:
                langs_list.append(lang)
     
        #for each language in the list, make pairs of languages
        #append the language pair to a list
        #append the language pair and their corresponding words to a list
        for lang_pair in it.combinations(langs_list,r=2):
            l1, l2 = lang_pair
            word = langs[l1]
            word2 = langs[l2]
             
    #                 ####method 1: if there are synonyms take only the word pair with the highest similarity
    #                 ##if the languages both have one word for the concept, compute nw
    #                 if len(word)==1 and len(word2) == 1:
    #                     wrd_score, algNotNeeded, alg = nw(word[0], word2[0], lodict, gp1, gp2)
    #                     alg_dict[lang_pair]=[list(alg)]
    #                     
    #                 ##elif one or both languages have more than one word for the concept, compute nw and take the pair with the higher similarity
    #                 else:
    #                     combination_list = list(it.product(word, word2))
    #                     list_score=[]
    #                     for word_pair in combination_list:
    #                         wrd_score1, algNotNeeded1, alg1 = nw(word_pair[0], word_pair[1], lodict, gp1, gp2)
    #                         list_score.append((wrd_score1,list(alg1)))
    # 
    #                     alg_dict[lang_pair]=[list(max(list_score)[1])]
                 
                 
            ##########method 2: take all alignments of the synonyms and their possible combinations into account
            if len(word)==1 and len(word2) == 1:
                wrd_score, algNotNeeded, alg = nw(word[0], word2[0], lodict, gp1, gp2)
                
                alg_dict[lang_pair]=[list(alg)]
            ##elif one or both languages have more than one word for the concept, compute nw and take the pair with the higher similarity
            elif len(word) > 1 or len(word2) >1:
                combination_list = list(it.product(word, word2))
                list_alg=[]
                for word_pair in combination_list:
                    wrd_score1, algNotNeeded1, alg1 = nw(word_pair[0], word_pair[1], lodict, gp1, gp2)
                    list_alg.append(list(alg1))
     
                alg_dict[lang_pair]=list_alg
        overall_algDict[concept] = alg_dict
                 
    return overall_algDict

if __name__ == '__main__':
    pass