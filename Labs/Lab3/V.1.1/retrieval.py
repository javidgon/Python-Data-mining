def main():
    phrases={} # Phrases' dictionary.
    formatedPhrases={} # Formated phrases' dictionary.
    coincidences={} # Coincidences' dictionary.
    print "--------------------------------------------------------------"
    print "-                                                            -"
    print "- Lab 3: An Association Thesaurus for Information Retrieval  -"
    print "-                                                            -"
    print "--------------------------------------------------------------"
    # Step 1: Opens file and extracts words. Forming associations.
    phrases = extraction() # Extracts data and creates a "rude" dictionary.
    formatedPhrases = formatW(phrases) # Returns a formated dictionary.
    coincidences=lookCoincidences(formatedPhrases) # Searches words' coincidences.
    # Step 2: Writes data into a document.
    writeDocument(formatedPhrases,coincidences)


# Functions ------------------------------------------------------------

def extraction(path='data'): # Extracts words from file.
    phrases={} # Structure: D[Phrase_id]={'word1','word2','word3'....}
    i=0
    for line in open(path+'/text.txt'): # Adds the word, but not the coincidence.
        phrases[i]=[]
        phrases[i] = line.split(' ')
        i += 1
    print "Extraction completed successfully."
    return phrases # Returns dictionary.

def formatW(phrases): # Formating extracted words.
    aux={}

    for i in phrases.keys():
        aux[i]=[]
        for j in phrases[i]:
            if (stopWords(j) == False): # Delete stop words.
                p = formatWords(j.lower()) # Turns into lower.
                aux[i].append(p)

            
    print "File formated successfully."
    return aux

def lookCoincidences(lexico): # Searches coincidences.
    aux=[]
    coincidences={} # Structure example: coincidences['Hello']= 4
    count=0

    for i in lexico.keys():
        for j in lexico[i]:
            if(j not in aux):
                for n in lexico.keys():
                    for x in lexico[n]:
                        if(x == j):
                            count += 1 # If appears +1if(j not in aux):
                coincidences[j]=count
                count=0
                aux.append(j)
    print "Coincidences' search completed successfully."
    return coincidences

def writeDocument(dictionary,coincidences):
    output = open('data/results.txt', 'w') # Creates a new file.

    output.write("Built document:")
    for i in dictionary.keys():
        output.write("\n ")
        for j in dictionary[i]:
            output.write(j + ' (' + str(coincidences[j]) + '),')

    output.close()
    print "Results' file created successfully."

def formatWords(word): # Deletes some useless values.
        value= word
        if (word.endswith(".")or word.endswith(",") or word.endswith(")") or word.endswith("\"")or word.endswith("'") or word.endswith(":")):
                value = word[0:-1]
        elif(word.startswith("'") or word.startswith("(") or word.startswith("\"")):
                value = word[1:0]
        elif(word.endswith(".\n")):
                value = word[0:-2]
        elif(word.startswith("[") and word.endswith("]")):
                value = word[1:-1]
        return value

def stopWords(word): # Removes useless values.
        if(word == "a" or word == "an" or word == "the" or word == "to" or word == "from" or word == "-"):
                return True
        else:
                return False
   

if __name__ == "__main__":
    main()
