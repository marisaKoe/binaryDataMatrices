'''
Created on 19.07.2017

@author: marisakoe

computes a data matrix only with ngram alignments for each concept
the matrices can be used for bayesian tree reconstruction
'''
import codecs
import itertools as it
from numpy import * 
from collections import defaultdict

from computation_methods import string_similarity
from write_output import write_dataMatrix

def main_ngrams(data_dict,sounds, dataName):
    '''
    aligns two strings according to their unigrams, bigrams and gappy bigrams.
    Checks the similarity to create a data matrix.
    :param f: the name of the file
    '''

    #for each concept in the dictionary
    for concept in data_dict:
        #if concept is mountain (just for testing)
        #if concept == "Bogen[Waffe]::N":
        alg_dict = defaultdict()
        #get the dictionray with all languages
        langs_dict = data_dict[concept]
        #get all the languages in one list
        list_langs = langs_dict.keys()
        #make language pair for each possible combination
        for pair in it.combinations(list_langs,r=2):
            #print pair
            #get the languages
            l1, l2 = pair
            #get the words
            word1 = langs_dict[l1]
            word2 = langs_dict[l2]
            ####take synonyms into account and take all matched between all combinations into account
            if len(word1)==1 and len(word2)==1:
                #pass
                ##get the alignment
                match = string_similarity("^"+word1[0]+"$", "^"+word2[0]+"$")
                alg_dict[pair] = match
            else:
                combination_list = list(it.product(word1, word2))
                match_list=[]
                for word_pair in combination_list:
                    match_pair = string_similarity("^"+word_pair[0]+"$", "^"+word_pair[1]+"$")
                    match_list.append(match_pair)
                match = list(it.chain(*match_list))
                alg_dict[pair] = match
        
                        
            print "concept: ", concept
            print "number of matches ", len(alg_dict.values())
            create_dataMatrix(concept, list_langs, alg_dict,sounds,dataName)
                
                
def create_dataMatrix(concept, list_langs, alg_dict,sounds,dataName):
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
    #create a list for all pairs of sounds  
    sound_pairs = [p[0]+p[1] for p in it.combinations(sounds,r=2)]
    #combine all sounds (unigrams and bigrams) into a list
    all_sounds = sounds+sound_pairs
    #print all_sounds
    all_sounds.remove("^")
    all_sounds.remove("$")
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
        #print langs
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
            #check if the string is in the list of sound pairs and append it to the new list
            if a in all_sounds:
                new_alg.append(a)
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
    fout1 = "output/"+dataName+"/data_matrices_ngrams/"+"dataMatrix_"+concept+".nex"
    #call the function to write the data matrix to a file
    write_dataMatrix(fout1, dataMatrix,len(list_langs),len(overall_soundpairs))

if __name__ == '__main__':
    pass