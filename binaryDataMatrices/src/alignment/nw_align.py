'''
Created on 19.07.2017

@author: marisakoe


creates a data matrix with the alignments of Needleman-Wunsch and the sound alignments present for the language in the concept
the matrices can be used for bayesian tree reconstruction

'''

from numpy import *
import itertools as it
from collections import defaultdict
import codecs

from computation_methods import nw
from write_output import write_dataMatrix

unique_chars = []
gp1 = -2.49302792222
gp2 = -1.70573165621

lodict={}

def main_nw_align(data_dict, pmi,sounds, dataName):
    '''
    main function to create an alignment dictionary and give it back to a helper function to create a data matrix for the alignments
    :param data: the name of the data file
    '''
    #reads the file with the 41 sounds of ASJP
    f = open('input/'+sounds)
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
#                 ##############################method 1: take the word pair with the highest similarity#################################
#                 ##if the languages both have one word for the concept, compute nw
#                 if len(word)==1 and len(word2) == 1:
#                     wrd_score, alg, algNotNeeded = nw(word[0], word2[0], lodict, gp1, gp2)
#                     alg_dict[lang_pair]=alg
#                 ##elif one or both languages have more than one word for the concept, compute nw and take the pair with the higher similarity
#                 elif len(word) > 1 or len(word2) >1:
#                     
#                     combination_list = list(it.product(word, word2))
#                     
#                     list_score=[]
#                     for word_pair in combination_list:
#                         wrd_score1, alg1, algNotNeeded1 = nw(word_pair[0], word_pair[1], lodict, gp1, gp2)
#                         list_score.append((wrd_score1,alg1))
#                     
#                     alg_dict[lang_pair]=max(list_score)[1]
                
        
            ############method 2: take all synonyms and their alignments into account#####################
            if len(word)==1 and len(word2) == 1:
                wrd_score, alg, algNotNeeded = nw(word[0], word2[0], lodict, gp1, gp2)
                # alg
                alg_dict[lang_pair]=alg
            ##elif one or both languages have more than one word for the concept, compute nw and take the pair with the higher similarity
            elif len(word) > 1 or len(word2) >1:
                combination_list = list(it.product(word, word2))
                list_alg=[]
                for word_pair in combination_list:
                    wrd_score1, alg1, algNotNeeded1 = nw(word_pair[0], word_pair[1], lodict, gp1, gp2)
                    list_alg.append(alg1)
                    
                match = list(it.chain(*list_alg))
                alg_dict[lang_pair]=match


            #create data matrix for the concept (in helper methods)
        create_dataMatrix(concept, list_sounds, sounds_gap, langs_list, alg_dict, dataName)
        print count




def create_dataMatrix(concept,list_sounds, sounds_gap, list_langs, alg_dict, dataName):
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
    
    #get the product of the two sound lists, which is a list with unique sound pairs
    sound_pairs_product = it.product(list_sounds, sounds_gap)
    #transform the itertools object into a list
    sound_pairs = list(sound_pairs_product)
    #initialize the data matrix
    dataMatrix = defaultdict(dict)
    ####needed if we want to compute the matrix with all possible sound pairs
#     for langs in list_langs:
#         #for each pair in the list
#         for pair in sound_pairs:
#             #set the default value to 0
#             dataMatrix[langs][pair] = "0"
    
    
    #for each lang in the list (only needed for the reduced matrix)
    for langs in list_langs:
        dataMatrix[langs]=defaultdict(int)
    #only needed for the reduced matrix
    overall_soundpairs=[]
    #for lang pairs and alignments in the alignment dictionary
    for langs, alg in alg_dict.items():
        ##get the first and the second language
        l1,l2 = langs
        #get the alignment score and the character alignment in a list of lists
        #wrd_score, alg = algs
        #initialize a new list for storing the sound pairs of the alignments
        new_alg=[]
        #for each sound alignment in the list
        for a in alg:
            #make a tuple out of the list
            new_a = tuple(a)
            #check if the tuple is in the list of sound pairs and append it to the new list
            if new_a in sound_pairs:
                new_alg.append(new_a) 
            #otherwise reverse the tuple and append it to the list
            else:
                new_alg.append(new_a[::-1])
        
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
    fout1 = "output/"+dataName+"/data_matrices_nw/"+"dataMatrix_"+concept+".nex"
    #call the function to write the data matrix to a file
    write_dataMatrix(fout1, dataMatrix,len(list_langs),len(overall_soundpairs))

if __name__ == '__main__':
    pass