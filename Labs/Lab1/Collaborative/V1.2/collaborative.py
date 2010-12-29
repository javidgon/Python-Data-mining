import numpy


def main():
    film = 0 # The film choosen by the user.
    films = [] # Double dictionary.
    users = [] # Users keys.
    avg_dict = {} # Average users' rate.
    bigDict = {}
    print "--------------------------------------------------------------"
    print "-                                                            -"
    print "- Lab 1B: Item Based                                         -"
    print "-                                                            -"
    print "--------------------------------------------------------------"
    # 1ﾺ Step.
    film = query() # Query.
    # 2ﾺ Step.
    films = load_data(users,bigDict)# Loads and saves data from the file. Also creates an users keys list.
    createDict(bigDict,films,users)
    print "Data have been loaded successfully."
    print "Users list created successfully."
    print "Films list created successfully."
    # 3ﾺ Step. Calculates users' average.
    print "Creating average list..."
    avg_dict = user_avg(films,users,bigDict)
    print "Users' average list created successfully."
    # 4ﾺ Step. Calculates a-cos(x,y).
    print "Performing comparisons..."
    comparison(users,film,films,avg_dict,bigDict)
    print "Completed processes."

# Functions. ----------------------------------------------------------------

def query():
    print "What film do you want to compare with the rest?"
    answerd = raw_input()
    return answerd


def load_data(users,bigDict, path='data'): # User/Item/Rating
        films=[] # Films list.

        for line in open(path+'/u.data'):
            (value1,value2,value3) = line.split('\t')[0:3]
            bigDict[value2]={}
            bigDict[value2][value1]= int(value3)
            if (value1 not in users):
                users.append(value1)
            if (value2 not in films):
                films.append(value2)

        return films

def user_avg(films,users,bigDict): # Users' average. Main function.
    avg_dict={}
    for i in users:
            valor = avg(films,i,bigDict)
            #print "Usuario: " + i + ' Valor: ' + str(valor)
            avg_dict[i] = valor
    return avg_dict
    

def avg(films,user,bigDict,path='data'): # Users' average. Secondary function.
    cont = 0
    valor = 0
    for line in open(path+'/u.data'):
        (aux_user,aux_film,aux_vote) = line.split('\t')[0:3]
        bigDict[aux_film][aux_user]=int(aux_vote)
        if(user == aux_user):
            valor += int(aux_vote)
            cont += 1
    if(valor !=0 and cont != 0):
        return valor/float(cont)
    else:
        return 0

def createDict(bigDict,films,users,path='data'):
    for i in films:
        bigDict[i]={}
        for j in users:
            bigDict[i][j]=0
    print "Formatting is complete."
            
    for line in open(path+'/u.data'):
        (value1,value2,value3) = line.split('\t')[0:3]
        bigDict[value2][value1]= int(value3)
    print "Successfully added values."


    
def isNaN(num): # Is NaN?
       return num != num

def comparison(users,film,films,avg_dict,bigDict): # Performs comparisons.
    valueList = [] # Values list
    indexList = [] # Indexes list.
    result = 0
    maxResults = 10 # Max results.
    combination = []
    re1 = {}
    for i in films:
        if (i!=film):
            result = adjusted_cosine(i,film,avg_dict,users,films,bigDict)
            print "For films... nº: " + i + " y nº: " + film + " el cos es: " + str(result)
            if (isNaN(result) == False):
                valueList.append(result) # Introduces into values list.
                indexList.append(i) # Introduces into indexes list.

    print "Comparisons done successfully."
    combination = zip(valueList,indexList) # Merges both lists.
    sortedC = sorted(combination) # Sorts merged list.

    # Shows 10 best results.
    
    print "-------------------- Results --------------------"
    print("Film nﾺ: " + str(film) + " according by users' votes, is similar to: ")

    x = len(sortedC)-1

    while(x>=0 and maxResults > 0):
        res = sortedC[x]
        print("\t Film nﾺ: " + str(res[1]) + " -- a-coseno: " + str(res[0]))
        x -= 1
        maxResults -= 1


def adjusted_cosine(x,y,avg_dict,users,films,bigDict,path='data'): # Adjusted cosine method.
    sum1 = 0
    sum2 = 0
    sum3 = 0
    
    for i in users:   # Every user
        sum1 += float(bigDict[x][i]-avg_dict[i])*float(bigDict[y][i]-avg_dict[i]) # Numerator
        sum2 += float((bigDict[x][i]-avg_dict[i])**2) # Denominator 1.
        sum3 += float((bigDict[y][i]-avg_dict[i])**2) # Denominator 2.

    result = (sum1)/((numpy.sqrt(sum2))*(numpy.sqrt(sum3))) # Comparison results.
    
    return result
              
if __name__ == "__main__":
    main()
