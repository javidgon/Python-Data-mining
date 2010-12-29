import numpy
import urllib2, urllib
import datetime
from numpy import linalg as LA

def main():
    id_list = [] # Valid films list.
    movies = {} # Films' dictionary with the different summaries.
    postings = {} # Dictionary with all the words' postings.
    lexico = [] # Lexico's list.
    bigDictionary = {} # Dictionary with the asociation between films and words repetition.
    exitWay = False # FALSE ---> NO EXIT
    commonP = [] # Common Posting list.

    print "--------------------------------------------------------------"
    print "-                                                            -"
    print "-                        Lab 2                               -"
    print "-                                                            -"
    print "--------------------------------------------------------------"

    # 1.- Loads movies from file.
    id_list = loadValidNumbers() # Returns id movies list.
    movies = loadMoviesSummaries(id_list)# Returns movies list, which contains every films' summary.
    # Important!: Movies list has as indexes the different movies' id. NOT START IN 0! NOT IS INCREMENTAL!

    # 2.- Processer data.
    postings = extractWords(lexico,movies,id_list,bigDictionary)

    # 3.- System options.
    queries = readQueries() # System asks about queries number.
    
    while exitWay != "y": # Type "y" for exit!
        answerd1 = queryType() # TermSearch or DocumentSearch???
        answerd2 = queryNumber() # What query??
        
        if answerd2 < len(queries.keys()): # if it isn't a valid query.
            if (answerd1 == 0):
                commonP = termSearch(postings,queries,answerd2,bigDictionary,lexico) # Common results.
                cos(commonP,lexico,queries,answerd2,bigDictionary,movies) # Sorts the results.
            elif(answerd1 == 1):
                commonP = documentSearch(postings,queries,answerd2,bigDictionary,lexico) # Common results.
                cos(commonP,lexico,queries,answerd2,bigDictionary,movies) # Sorts the results.
            else:
                print "Wrong method" # If method not valid.
        else:
            print "Pick again." # If query not valid.
            
        exitWay = queryExit() # Do you wish exit?.


# First step functions ------------------------------------------------------
def loadValidNumbers(path='data'):
        id_list = []
        file1 = open(path+'/valid_summaries.txt','r')
        for a1 in file1:
            id_list = a1.split(' ')
        file1.close()
        
        return id_list

def loadMoviesSummaries(id_list,path='data'):
        i = 0
        movies = {}
        file2 = open(path+'/film_summaries.txt','r')
        for a2 in file2:
            valor = str(a2.split('|')[0:1])
            if(len(valor)>20):
                text = formatWords(valor)
                movies[id_list[i]]=text
                i += 1
        file2.close()
        
        return movies

# Second step functions ------------------------------------------------------

def extractWords(lexico,movies,id_list,bigDictionary):
        formatedMovies = {} # Dictionary with formated movies' summaries.
        for i in id_list:
                formatedMovies[i]=[]
                insertWord(movies[i],lexico,formatedMovies[i]) # Inserts word into lexico and puts data into formatedMovies.

        dictionariesWords(id_list,lexico,bigDictionary,formatedMovies)
        print "Lexicon created successfully."
        print "Creating inverted file..."

        return createInvertedFile(id_list,formatedMovies,lexico)
        print "Inverted file created successfully."

def insertWord(description,lexico,individual):
    lower_description = description.lower() # Turns lower.
    array = lower_description.split(" ") # Divides the summary using " ".
    for i in array:
        if (find(i,lexico) == False): # Is there any word similar into lexico???
            value = formatWords(i) # Deletes some useless values.
            if(stopWords(i) == False): # If It's not a stopWord.
                    lexico.extend([value]) # Inserts word into lexico.
                    individual.extend([value]) # Inserts word into "individual", which is the individual summary for every film.


def dictionariesWords(id_list,lexico,bigDictionary,formatedMovies): # In this method we create a dictionary with the repetion between words values.
    print "Creating dictionaries for every film..."
    for i in id_list: # Every key is a film.
        bigDictionary[i]={} # Creates another dictionary inside.
        for j in lexico: # Among all the words in lexico.
                bigDictionary[i][j] = counter(j,formatedMovies[i]) # How many times the word appears in that summary?


def createInvertedFile(id_list,formatedMovies,lexico):
        aux=[] # Individual posting list.
        postings={} # General posting list.
        output = open('data/inverted_file.txt', 'w')
        output.write("Inverted File: ")
        for j in lexico: # Among all the words in lexico.
            if (j!=""): # If not null.
                aux = [] # Initializes individual posting list.
                postings[j]=[] # Creates a list inside.
                for k in id_list: # While exist summaries.
                    if(j in formatedMovies[k]): # If exists that word.
                        aux.append(k) # Inserts it.
                
                output.write("\n \t" + str(j) + "--> " ) # Writes into the file.
                for n in aux: # While exist "Postings" list.
                    postings[j].append(n) # Introduces in general posting list.
                    output.write( str(n) + ", " ) # Writes into the file.          
        return postings
    
# Third step functions --------------------------------------------------------

def readQueries(path='data'):
    queries={} # Queries' dictionary.
    aux = {}
    i=0
    for line in open(path+'/queries.txt'): # Reads queries from file.
        aux[i]=[]
        queries[i] = line.split(' ')
        for j in queries[i]:
            aux[i].append(formatWords(j.lower())) # Formats queries.
        i += 1    
    return aux

def queryNumber():
    print "What query do you want to compare with the films? (Write a number, please)"
    answerd = raw_input()
    return int(answerd)

def queryType():
    print "What method do you want to use? (0 -> Term-at-time, 1 -> Document-at-time)"
    answerd = raw_input()
    return int(answerd)

def queryExit():
    print "do you wish exit? (Yes --> y)"
    answerd = raw_input()
    return answerd

def termSearch(postings,queries,number,bigDictionary,lexico):
    commonP = []
    rest = [] # Rest of postings values.
    i = 0
    condition = False

    now = datetime.datetime.now() # Initial time.
    print "Start! " + str(now)

    # 1 and 2.- Steps.
    while (condition == False):
        if (queries[number][i] in postings.keys()): # If exists in keys.
            postingT0 = postings[queries[number][i]] # Returns the posting list of the first word.
            condition = True # We found a valid first value.
        i += 1 # If we didn't find it...
        
    rest = queries[number][1:] # Rest of posting values. Words, not numbers.

    # 4 Step.
    for i in rest: # Rest or words.
        if (i in postings.keys()):
            p1 = postings[i] # Devuelve una lista de posting.

            for j in p1: # Posting list of every word.
                for x in postingT0: # Every number of the posting list.
                    if (j == x): # If they have the same number in both lists. 
                        if(j not in commonP): # If It isn't already.
                            commonP.append(j) # Adds number.
                            

    now2 = datetime.datetime.now() # Final time.
    print "Finish! " + str(now2)
    return commonP


def documentSearch(postings,queries,number,bigDictionary,lexico):
    commonP = []
    now = datetime.datetime.now() # Initial time.
    print "Start! " + str(now) 
    
    for i in queries[number]: # Do while lenght is good.
        if (i in postings.keys()):
            p1 = postings[i] # Iterates.
            if (p1[0] not in commonP): # If It's not in the list.
                commonP.append(p1[0]) # Adds the first IDocs.
    now2 = datetime.datetime.now()
    print "Finish! " + str(now2) # Final time.
    return commonP

def compareSummaries(film1,film2,lexico):
        v1=[]
        v2=[]
        
        for word in lexico: # Adds the repetion value to every vector.
                v1.append(film1[word])
                v2.append(film2[word])
                
        result = float(numpy.dot(v1,v2) / (LA.norm(v1)*LA.norm(v2))) # Similarity formula.

        return result
        
def cos(postings,lexico,queries,number,bigDictionary,movies):
                dictQueries={} # Query dictionary.
                cosValues ={} # COS values.
                listValues=[]
                listIndex=[]
                combination = [] # ZIP
                sortedC = [] # Sorted zip.
                x = 0 # Counter.
                stopResults = 5 # Shown results.
                
                # 1º Step: Opens file and creates dictionary.
                output = open('data/results.txt', 'w') # Creates a new file.
                dictQueries = dictionariesQueries(number,lexico,queries) # Creates a Query dictionary.                
                print "Performing comparisons..."
                
                # 2º Step: Calculates "Cos" between the query and films.
                for j in postings:
                    cosValues[j]=(compareSummaries(dictQueries,bigDictionary[j],lexico)) # Adds "cos" value to the list.

                # 3º Step: Creates lists and sorts them.
                createLists(listValues,listIndex,cosValues) # Sorts "Similarity Cos" list.
                combination = zip(listValues,listIndex)
                sortedC = sorted(combination)

                # 4º Step: Writes results in a file.
                output.write("\n Query: " + str(number) + ' -- Its films more similar are: \n')
                x = len(sortedC)-1 # highest to lowest.
                while(x>=0 and stopResults > 0):
                        n = sortedC[x][1]
                        output.write(' \t Film nº: ' + str(sortedC[x][1]) + '  Cos: ' + str(sortedC[x][0]) + ' \n')
                        x -= 1
                        stopResults -= 1
                
                print "Results document created successfully."
                print >>output
                output.close()



# Tools functions -------------------------------------------------------------
def formatWords(word): # Deletes some useless values.
        value= word
        if (word.endswith(".")or word.endswith(",") or word.endswith(")") or word.endswith("\"")or word.endswith("'") or word.endswith(":")):
                value = word[0:-1]
        elif(word.startswith("'") or word.startswith("(") or word.startswith("\"")):
                value = word[1:0]
        elif(word.endswith(".\n")):
                value = word[0:-2]
        elif(word.endswith("\n")):
                value = word[0:-2]
        elif(word.startswith("[") and word.endswith("]")):
                value = word[1:-1]
        return value

def find(value,a): # is the value in the list yet?.
    if (value in a) or (stopWords2(value) == False):
        return True
    else:
        return False

def stopWords(word): # Removes useless values.
        if(word == "a" or word == "an" or word == "the" or word == "to" or word == "from" or word == "-"):
                return True
        else:
                return False

def stopWords2(valor): # Removes useless values.
    if (valor == "['") or (valor == '[]') or (valor == "']" or (valor == " ")):
        return False
    else:
        return True

        
def counter(j,description):
    count = 0
    for value in description:
            if(value == j):
                    count += 1 # If appears +1
    return count

def dictionariesQueries(number,lexico,queries): # In this method we create a dictionary with the repetion between words values.
        dictionary ={} # Creates another dictionary inside.
        for j in lexico: # Among all the words in lexico.
                dictionary[j] = counter(j,queries[number]) # How many times the word appears in that summary?
        return dictionary

def createLists(listValues,listIndex,cosValues): #Inserts values on the lists.
        id_list = intoInteger(cosValues.keys())
        v = sorted(id_list)
        for i in v:
            listValues.insert(i,cosValues[str(i)])
            listIndex.insert(i,i)

def intoInteger(id_list):
    integer_list = []
    for i in id_list:
        integer_list.append(int(i))
    return integer_list


if __name__ == "__main__":
    main()
