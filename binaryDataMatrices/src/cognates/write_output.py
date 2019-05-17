'''
Created on 21.07.2017

@author: marisa

write data matrix into a file
'''


import codecs

def write_dataMatrix(fout1, dataMatrix,numLangs, numCC):
    '''
    write the data matrix to a file ready for Mr Bayes, which is similar to a nexus file
    :param fout1: the name of the output file
    :param dataMatrix: the datamatrix as a dict of dicts
    :param numLangs: the number of languages in this concept
    :param numSoundPairs: the number of sound pairs
    '''
    #open the file
    fout = codecs.open(fout1,"wb","utf-8")
    #write the first lines of the nexus file
    fout.write("#NEXUS"+"\n"+"\n")
    fout.write("BEGIN DATA;"+"\n"+"DIMENSIONS ntax="+str(numLangs)+" NCHAR="+str(numCC)+";\n"+"FORMAT DATATYPE=Restriction GAP=- MISSING=? interleave=yes;\n"+"MATRIX\n\n")
    #go through the languages and the dictionary of sound pairs
    for lang,sounds in dataMatrix.items():
        #write the first part of the row, which is the language name, 40 white spaces and a tab
        row = lang.ljust(40)+"\t"
        #go through the sound pairs
        for sp in sounds:
            #append the value of the language and the sound pair to the row
            row=row+str(dataMatrix[lang][sp])
        #write the row and a new line
        fout.write(row+"\n")
    #write the end of the nexus file
    fout.write("\n"+";\n"+"END;")
    fout.close()


if __name__ == '__main__':
    pass