'''
Created on 20.07.2017

@author: marisa


create a data matrix with cognate information
0=absence
1=presence

write a data matrix for each concept

'''
import itertools
from collections import defaultdict

from write_output import write_dataMatrix


def main_cog(data_dict, outfolder):
    '''
    use the data_dict with the cognate classes to create a data_matrix for langxcogs with 0=absence and 1=presence
    writes the matrix directly to a file
    :param data_dict: dict with key=concept value=dict with key=lang value=cc
    '''
    
    
    ##for each concept in the dictionary
    for concept,lang_dict in data_dict.items():
        #if concept == "Berg::N":
        #print concept
        print concept
        ##initialize the datamatrix as a default dict with integers
        data_matrix = defaultdict(lambda: defaultdict(int))
        ##get the list of languages from the dictionary
        langs_list = lang_dict.keys()
        ##get the cogantes classes for each language
        cc_list = lang_dict.values()
        ##get the unique list of cognate classes
        unique_cc= set(itertools.chain(*cc_list))
        #unique_cc = set(x for l in cc_list for x in l)
        
        
        ##for each language and each cogante class, fill the dictionary with 0 for absence
        for lang in langs_list:
            for cc in unique_cc:
                data_matrix[lang][cc]="0"

         
        ##for each language in the data_matrix, get the cognate class and replace the 0 with a 1 for presence
        for lang, new_dict in data_matrix.items():
            cc = lang_dict[lang]
            for c in cc:
                data_matrix[lang][c]="1"
            


        ##write the data_matrix to a nexus file for further analysis
        fout1 = outfolder+"dataMatrix_"+concept+".nex"
        write_dataMatrix(fout1, data_matrix, len(langs_list), len(unique_cc))

    
    
    
    
    

    
    

if __name__ == '__main__':
    pass
    
#     f_cogs = "../input/nelexAsjp.cognates"
#     dataName = "nelex"
#     
#     cog_dict = read_nelexCog(f_cogs)
#     main_cog(cog_dict, dataName)
    
    
    
    
    
    
    