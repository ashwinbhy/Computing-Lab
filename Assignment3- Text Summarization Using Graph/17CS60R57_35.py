#Assignment3
#Suyog Chadawar
#roll no 17CS60R57
#Ashwin Bhoyar
#roll no 17CS60R35

import nltk
import string
import collections
import math
import operator
from nltk.corpus import stopwords
import sys
reload(sys)
from pyrouge import Rouge155
sys.setdefaultencoding('utf8')


def pageRankReverse(matrix):#finding pagerank for backword graph
    n = len(matrix)
    prb = [1 for x in range(n)]
    bprb = [1 for x in range(n)]
    l = 0
    count = 0
    while True:#running the loop untill it gets stebalized
        i = 0
        prb = [x for x in bprb]
        count = count + 1
        while (i < n):#finding pagerank for every vertex
            j = i+1
            sumw = 0
            # print "v", i
            while (j < n):#for every vertex finding the incoming edges
                if matrix[j][i] != 0:#removing non edge pairs
                    sum = 0
                    k = 0
                    while (k < j):#finding out links of j
                        sum = sum + matrix[j][k]
                        k = k + 1
                    sumw = sumw + (matrix[j][i] * prb[j] / sum)
                j = j + 1
            bprb[i] = 0.15 + 0.85 * sumw#implementing the formula 10 in the paper
            i = i + 1
        if customCompare(prb, bprb):#cheking wether pagerank has stebalized or not
            break

    tuplesb = list()
    for index in range(0, n):#creating a tupple having its pagerank and vertex number
        tupleb = (prb[index], index)
        tuplesb.append(tupleb)
    return tuplesb

def pageForward(matrix):
    n = len(matrix)
    pr = [1 for x in range(n)]
    bpr = [1 for x in range(n)]
    l = 0
    count = 0
    while True:
        i = 0
        pr = [x for x in bpr]
        count = count + 1
        while (i < n):#finding pagerank for every vertex
            j = 0
            sumw = 0
            while (j < i):#for every vertex finding the incoming edges
                if matrix[j][i] != 0:#removing non edge pairs
                    sum = 0
                    k = j + 1
                    while (k < n):#finding out links of j
                        sum = sum + matrix[j][k]
                        k = k + 1
                    sumw = sumw + (matrix[j][i] * pr[j] / sum)
                j = j + 1
            bpr[i] = 0.15 + 0.85 * sumw#implementing the formula 10 in the paper
            i = i + 1
        if customCompare(pr, bpr):#cheking wether pagerank has stebalized or not
            break

    tuples = list()
    for index in range(0, n):#creating a tupple having its pagerank and vertex number
        tuple = (pr[index], index)
        tuples.append(tuple)
    return tuples



def customCompare(list1, list2):
    for i in range(0, len(list1)):
        if list1[i] != list2[i]:
            return False
    return True




#Class to store pre processed
#and post processed sentences
class SentenceCollection:

    def __init__(self,original,trimmed):
        self.original=original
        self.trimmed=trimmed
    def getOriginal(self):
        return self.original
    def getTrimmed(self):
        return self.trimmed

#Main method
if __name__ == '__main__':
    #Reading inputdoc summary size and golden summary path
    inputDoc=sys.argv[1]
    sumSize=int(sys.argv[2])
    goldSummary=sys.argv[3]
    STOP_WORDS= set(stopwords.words('english'))
    portStem = nltk.PorterStemmer()

    #Reading and storing the golden summary
    file_object = open(goldSummary, "r")
    gsummery=''
    for line in file_object:
        gsummery+=line.encode('ascii', 'ignore')+"\n"

   #Reading the input Doc
    f = open(inputDoc)
    raw = f.read()
    allSentList=list()

    #Reading the sentences from the doc
    rawSentence = nltk.sent_tokenize(raw)
    sentences = list()

    # On each sentence doing
    # Removing punctuation
    # Case folding
    # Stemming
    for sen in rawSentence:
        tokenizedSent=nltk.word_tokenize(sen.translate(None,string.punctuation))
        filtered_words = [portStem.stem(word.lower()).encode('ascii', 'ignore') for word in tokenizedSent if word.lower() not in STOP_WORDS]
        sentences.append(filtered_words)
        allSentList.append(SentenceCollection(sen.encode('ascii', 'ignore'),filtered_words))

    n = len(sentences)

    #Creating a weight matrix
    #as per the equation given in the paper
    # to get the intersection between two sentences and dividing by log to normalize
    weightMat = [[0 for x in range(n)] for y in range(n)]
    for i in range(0,len(allSentList)):
        for j in range(i+1,len(allSentList)):
            iIndex=collections.Counter(allSentList[i].getTrimmed())
            jIndex=collections.Counter(allSentList[j].getTrimmed())
            interSection= len(list((iIndex & jIndex).elements()))
            if interSection != 0:
                weight= (interSection)/(math.log(len(sentences[i]))+math.log(len(sentences[j])))
                weightMat[i][j]=weight
                weightMat[j][i]=weight

    #Performing a forward edged summary
    tupleList = pageForward(weightMat)

    fSummaryString=''
    bSummaryString=''

    #Selecting top nodes for summary
    tupleList = sorted(tupleList, reverse=True)
    selectedTupleList=list()
    selectedTupleList=tupleList[:sumSize]
    #Sorting by index to have the order
    selectedTupleList.sort(key=operator.itemgetter(1))

    #Displaying the forward summary
    print '\nForward Summary\n'
    for tup in selectedTupleList:
        print allSentList[tup[1]].getOriginal()
        fSummaryString+=allSentList[tup[1]].getOriginal()+"\n"

    print "\n Backward summary\n"

    #Calculate reverse edge summary
    tupleList=pageRankReverse(weightMat)
    #Sort according to score descending and take top n sentences
    tupleList = sorted(tupleList, reverse=True)
    selectedTupleList = list()
    selectedTupleList = tupleList[:sumSize]
    #Order according to original order for top n sentences
    selectedTupleList.sort(key=operator.itemgetter(1))
    for tup in selectedTupleList:
        print allSentList[tup[1]].getOriginal()
        bSummaryString+=allSentList[tup[1]].getOriginal()+"\n"

    r = Rouge155(rouge_home="/home/suyog/Downloads/pyrouge-master/tools/ROUGE-1.5.5")
    hase=fSummaryString
    d = {'A':gsummery}

    #Calculating forward summary rouge-2 score
    dct=r.score_summary(hase,d)
    print "\nforward summary"
    print "score", dct["rouge_2_f_score"]
    print "precision",dct["rouge_2_precision"]
    print "recall", dct["rouge_2_recall"]

    hase=bSummaryString

    #Calculating backward summary-2 rouge score
    dct= r.score_summary(hase,d)
    print "\nbackward summary"
    print "score", dct["rouge_2_f_score"]
    print "precision",dct["rouge_2_precision"]
    print "recall", dct["rouge_2_recall"]