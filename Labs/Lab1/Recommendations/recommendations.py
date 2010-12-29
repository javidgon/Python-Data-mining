# To change this template, choose Tools | Templates
# and open the template in the editor
__author__="Urgencia"
__date__ ="$21-abr-2010 13:57:39$"



from UserList import *
import urllib2, urllib
import numpy
from numpy import linalg as LA

# -*- coding: cp1252 -*-

def main():
        lexico=[] # Creates a list called "lexico"
        dictionary={} # Creates a dictionary
        summaries=[] # Creates another list for summaries.
        
        print "--------------------------------------------------------------"
        print "-                                                            -"
        print "- Lab 1: Collaborative Filtering                             -"
        print "-                                                            -"
        print "--------------------------------------------------------------"
        movies = loadMovieLens() # We extract the information from the website. And we return a dictionary called "movies"
        keyslistMovies = createFileMovies(movies,summaries) # We create a file completely formated. With a special structure for be analyzed. And we return a list with the dictionary "keys".
        extractWords(lexico,summaries,keyslistMovies,movies) # In this method, we do several things. It's better see the explanations inside.
        print "Processes completed successfully"
        
def cos(keys,lexico,dictionary,movies):
        output = open('data/results.txt', 'w') # Creates a new file.
        i=0
        print "Performing comparisons..."
        while i < len(keys):
                cosValues ={}
                listValues=[]
                listIndex=[]
                j = 0
                x = 0
                stopResults = 10 # Shown results.
                while j < len(keys):
                        if (i != j):
                                cosValues[j]=(compareSummaries(dictionary[i],dictionary[j],lexico)) # Adds "cos" value to the list.
                        j += 1
                        
                createLists(listValues,listIndex,cosValues) # Sorts "Similarity Cos" list.
                burbujamejoradov2(listValues,listIndex)
                output.write("\n Film: " + movies[i+1] + ' -- Its films more similar are: \n')
                #De 0 a 19
                x = len(listIndex)-1
                while(x>=0 and stopResults > 0):
                        n = listIndex[x]
                        output.write(' \t ' + movies[n+1] + ": " + ' Cos: ' + str(listValues[x]) + " \n")
                        x -= 1
                        stopResults -= 1
                i += 1
        print "Results document created successfully."
        print >>output
        output.close()
        
def createLists(listValues,listIndex,cosValues): #Inserts values on the lists.
        keys = cosValues.keys()
        v = sorted(keys)
        for i in v:
                if(cosValues[i] != 0.0 and isNaN(cosValues[i]) == False):
                        listValues.insert(i,cosValues[i])
                        listIndex.insert(i,i)
        

def isNaN(num):
       return num != num

def burbujamejoradov2(l,indices):  #Sorts both lists.
        intercambios=1 
        pasada=1 
        while pasada<len(l) and intercambios==1: 
                intercambios=0 
                for i in range(0,len(l)-pasada): 
                        if l[i] > l[i+1]: 
                                l[i], l[i+1] = l[i+1], l[i]
                                indices[i],indices[i+1],indices[i]
                                intercambios=1 
                pasada += 1 



def loadMovieLens(path='data'):
        # Gets movies information.
        movies={} # Dictionary for save films.
        for line in open(path+'/short.txt'):
                (id,title)=line.split('|')[0:2]
                print title
                print id
                movies[int(id)]=title
        return movies


def loadMovieDescription(nome):
    # Load movie description from the website.
        page = urllib2.urlopen('http://www.imdb.com/find?' + urllib.urlencode({'q':nome}))
        web = urllib2.urlopen(page.url + "plotsummary")
        summary = selectPartWeb(web)
        print summary 
        return summary

def selectPartWeb(web): # We extract the really useful information (Plot Summary). SOME FILMS ARE NOT WORKING CORRECTELY.
        pagina = ""
        for line in web:
                pagina += line
        pos1 = pagina.find('<p class="plotpar">')+19 # Begin
        pos2 = pagina.find('<i>') # Finish
        if (len(pagina[pos1:pos2]) > 1000): # With that we control "loading" errors. (HTML)
                return ""
        else:
        
                return pagina[pos1:pos2]


def createFileMovies(movies,summaries):
        j = 0
        keylist = sorted(movies.keys()) # We sort the list.
        output = open('data/film_summaries.txt', 'w') # We start to create the formated file.
        print "Downloading summaries from IMDb..."
        for i in keylist:
            page = loadMovieDescription(movies[i])
            summaries.append(page)
            output.write(str(i) + ' | ' + movies[i] + ' | ' + summaries[j] + ' | ' + '\n')
            j += 1
        print "Summaries' extraction from IMDb completed."
        print >>output, i
        output.close()
        return keylist


def extractWords(lexico, summaries,keys,movies):
        i = 0
        globalList=[] # List with all the summaries.
        dictionary = {} # Dictionary for save the comparison values.
        while i < len(summaries): # With that we create "lexico" list. 
                individual=[] # Individual summary, used for make the comparison.
                insertWord(summaries[i],lexico,individual) # Inserts word into lexico.
                globalList.append(individual) # We save the individual summary.
                i += 1
        print "Lexicon created successfully."
        dictionariesWords(keys,lexico,dictionary,globalList) # How many times a word appears in one summary?
        cos(keys,lexico,dictionary,movies) # We make comparisons and
        
                

def insertWord(description,lexico,individual):
    lower_description = description.lower() # Turns lower.
    array = lower_description.split(" ") #We divide the summary using " ".
    for i in array:
        if (find(i,lexico)== False):
            value = formatWords(i) # Deletes some useless values.
            if(stopWords(i)==False): # If It's not a stopWord.
                    lexico.extend([value]) # Inserts word into lexico.
                    individual.extend([value]) # Inserts word into "individual", which is the individual summary for every film.

def find(value, list): # is the value in the list yet?.
    if (value in list) or (revision(value) == False):
        return True
    else:
        return False

def revision(valor): # Removes useless values.
    if (valor == "['") or (valor == '[]') or (valor == "']"):
        return False
    else:
        return True

def formatWords(word): # Deletes some useless values.
        value= word
        if (word.endswith(".")or word.endswith(",") or word.endswith(")") or word.endswith("'") or word.endswith(":")):
                value = word[0:-1]
        elif(word.startswith("'") or word.startswith("(")):
                value = word[1:0]
        elif(word.endswith(".\n")):
                value = word[0:-2]
        return value

def stopWords(word):
        if(word == "a" or word == "an" or word == "the" or word == "to" or word == "from" or word == "-"):
                return True
        else:
                return False

def dictionariesWords(keys,lexico,dictionary,summaries): # In this method we create a dictionary with the repetion between words values.
    i = 0
    print "Creating dictionaries for every film..."
    while i < len(keys): # Every key is a film.
        dictionary[i]={} # Creates another dictionary inside.
        for j in lexico: # Among all the words in lexico.
                dictionary[i][j] = seek(j,summaries[i]) # How many times the word appears in that summary?
        i += 1
        
def seek(j,description):
    count = 0
    for value in description:
            if(value == j):
                    count += 1 # If appears +1
    return count

def compareSummaries(film1,film2,lexico): # Film1 = dictionary[i]
        v1=[]
        v2=[]
        
        for word in lexico: # Adds the repetion value to every vector.
                v1.append(film1[word])
                v2.append(film2[word])
                
        result = float(numpy.dot(v1,v2) / (LA.norm(v1)*LA.norm(v2))) # Similarity formula.

        #print result (If it's necessary show the result)
       
        return result


                
if __name__ == "__main__":
    main()
