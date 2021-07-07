'''
Created on 19.07.2017

@author: marisakoe

'''
from collections import defaultdict

from alignment import main_nw_align, main_ngrams, main_ngramsNW
from cognates import main_cog


unique_chars = []

def read_ielex(f):
    '''
    reads the data file, and returns a dictionary which includes all synonyms included in the data.
    The languages are edited accordingly to take care of the synonyms (lang+transcription).
    :param f: a file
    :return d: dictionary with key=concept value=dictionary with key=lang+transcription value=transcription
    '''
    
    f1 = open(f,'r')
    raw_data = f1.readlines()
    f1.close()
    
    #initialize a default dict
    d = defaultdict(dict)
    #for each line in the file
    for line in raw_data:
        line = line.strip()
        #split it by tab
        arr = line.split("\t")
        #language
        lang = arr[0]
        #iso-code
        iso = arr[1]
        #gloss
        gloss = arr[2]
        #concept number
        concept = arr[3]
        #local-id
        local_id=arr[4]
        #transcription
        trans = arr[5]
        #cognate class
        cogid = arr[6]
        #notes
        note=arr[-1]
        cogid = cogid.replace("-","")
        cogid = cogid.replace("?","")
        #word transcription
        asjp_word = arr[5].split(",")[0]
        asjp_word = asjp_word.replace(" ", "")
        asjp_word = asjp_word.replace("%","")
        asjp_word = asjp_word.replace("~","")
        asjp_word = asjp_word.replace("*","")
        asjp_word = asjp_word.replace("$","")
        asjp_word = asjp_word.replace("\"","")
        asjp_word = asjp_word.replace(""" " ""","")
        asjp_word = asjp_word.replace("K","k")
        if len(asjp_word) < 1:
            continue
        if "K" in asjp_word:
            print line
        for x in asjp_word:
            if x not in unique_chars:
                unique_chars.append(x)

        #fill the dictionary with key=concept val=newDict with key=language+transcription val=transcription
        d[concept.encode("iso-8859-1")][str(lang.encode("iso-8859-1"))+"_"+str(asjp_word.encode("iso-8859-1"))] = asjp_word.encode("iso-8859-1")    


    return d


def read_nelex(f):
    '''
    reads the nelex datafile, which can be downloaded from the homepage with the ASJP transcriptions
    :param f:
    '''
    
    
    f1 = open(f,'r')
    raw_data = f1.readlines()
    f1.close()
    
    #initialize a default dict
    data_synonyms = defaultdict(lambda: defaultdict(list))
    data_plain = defaultdict(dict)
    for line in raw_data[1:]:
        #print line
        line = line.strip()
        #split it by tab
        arr = line.split("\t")
        lang = arr[0]
        iso = arr[1]
        concept = arr[2]
        #ipa=arr[3]
        #asjp=arr[4]
        #sca=arr[5]
        #dolgo=arr[6]
        
        #word transcription
        asjp_word = arr[4].split(",")[0]
        asjp_word = asjp_word.replace(" ", "")
        asjp_word = asjp_word.replace("%","")
        asjp_word = asjp_word.replace("~","")
        asjp_word = asjp_word.replace("*","")
        asjp_word = asjp_word.replace("$","")
        asjp_word = asjp_word.replace("\"","")
        asjp_word = asjp_word.replace(""" " ""","")
        asjp_word = asjp_word.replace("K","k")
        if len(asjp_word) < 1:
            continue
        if "K" in asjp_word:
            print line

        data_synonyms[concept][iso].append(asjp_word)
        data_plain[concept][iso]=asjp_word

    

    return data_synonyms, data_plain

def read_nelexCogPMI(f):
    '''
    reads the cogante data created by Tarakas pmi method
    :param f:
    '''
    
    f1 = open(f,'r')
    raw_data = f1.readlines()
    f1.close()
    
    cog_dict = defaultdict(lambda: defaultdict(list))
    for line in raw_data[1:]:
        arr = line.strip().split("\t")
        
        concept = arr[0]
        lang = arr[1]
        word_asjp=arr[2]
        cc = arr[-1]
        
        cog_dict[concept][lang].append(cc)
    
    return cog_dict
        
        
def read_nelexCogJD(f): 
    '''
    reads the cognate data from Johannes (used for LDC) automatic inferred cognates with a threshold from 0.55
    :param f: name of the file
    '''
    
    f1 = open(f,'r')
    raw_data = f1.readlines()
    f1.close()
    
    cog_dict = defaultdict(lambda: defaultdict(list))
    
    for line in raw_data[1:]:
        arr = line.strip().split("\t")
        
        concept = arr[0]
        iso = arr[1]
        #wordOrg = arr[2]
        #wordIPA = arr[3]
        cc = arr[4]
        #lw=arr[5]
        
        cog_dict[concept][iso].append(cc)
        
    return cog_dict
        

if __name__ == '__main__':

        
    #####needed to compute the data matrices with alignments
    f = "input/northeuralex-cldf.tsv"
    data_synonyms, data_plain = read_nelex(f)
    dataName="nelex"
    pmi="pmi_matrix_nelex.txt"
    sounds = "sounds.txt"
      
    #main_ngrams(data_synonyms, sounds, dataName)
    #main_nw_align(data_synonyms, pmi, sounds, dataName)
    main_ngramsNW(data_synonyms, pmi, sounds, dataName)
    
    
    #######needed for comptuting the data matrices with the different cognate judgements
    #Taraks PMI method
#     dataName = "nelex"
#     f_cogsPMI = "input/nelexAsjp.cognates"
#     outfolderPMI = "output/"+dataName+"/data_matrices_cogantesPMI/"
#     cog_dictPMI = read_nelexCogPMI(f_cogsPMI)
#     main_cog(cog_dictPMI, outfolderPMI)

 
    
    

    
    
    
    
    
    
    