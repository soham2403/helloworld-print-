import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('popular')
# nltk.download('averaged_perceptron_tagger')
#Importing the needed files and packages 

import pke
from nltk.corpus import stopwords
import string
from flashtext import KeywordProcessor
from nltk.tokenize import sent_tokenize
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
from nltk.corpus import wordnet as wn
import requests
import json
import re
import random
import sys
import io
import random
import json
# Create a StringIO object to store the MCQs
mcq_string = io.StringIO()

# Redirect stdout to the StringIO object
sys.stdout = mcq_string




# Step 1- Import the text file/article that has to be used for MCQ generation 
import sys

if __name__ == "__main__":
    # Retrieve the text passed from the GUI
    text = sys.argv[1]

    # Use the text as needed in the main file
    # print("Received text from GUI:", text)
   




#Step 2- Extract the important words(keywords) from the text article that can be used to create MCQ using PKE (Python Keyword Extraction)
def getImportantWords(art):
    extractor = pke.unsupervised.MultipartiteRank()
    extractor.load_document(input=art, language='en')
    pos = {'PROPN'}
    stops = list(string.punctuation)
    stops += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
    stops += stopwords.words('english')

    extractor.candidate_selection(pos=pos)
    selected_candidates = [candidate for candidate in extractor.candidates if candidate[0] not in stops]

    extractor.candidate_weighting()

    result = []
    for keyphrase in extractor.get_n_best(n=25):
        result.append(keyphrase[0])

    return result



impWords = getImportantWords(text)





#Step 3- Split the whole text article into an array/list of individual sentences. This will help us fetch the sentences related to the keywords easily
def splitTextToSents(art):
    s=[sent_tokenize(art)]
    s=[y for x in s for y in x]
    s=[sent.strip() for sent in s if len(sent)>15] #Removes all the sentences that have length less than 15 so that we can ensure that our questions have enough length for context
    return s
sents=splitTextToSents(text) #Achieve a well splitted set of sentences from the text article
#print(sents)





#Step 4- Map the sentences which contain the keywords to the related keywords so that we can easily lookup the sentences related to the keywords
def mapSents(impWords,sents):
    processor=KeywordProcessor() #Using keyword processor as our processor for this task
    keySents={}
    for word in impWords:
        keySents[word]=[]
        processor.add_keyword(word) #Adds key word to the processor
    for sent in sents:
        found=processor.extract_keywords(sent) #Extract the keywords in the sentence
        for each in found:
            keySents[each].append(sent) #For each keyword found, map the sentence to the keyword
    for key in keySents.keys():
        temp=keySents[key]
        temp=sorted(temp,key=len,reverse=True) #Sort the sentences according to their decreasing length in order to ensure the quality of question for the MCQ 
        keySents[key]=temp
    return keySents
mappedSents=mapSents(impWords,sents) #Achieve the sentences that contain the keywords and map those sentences to the keywords using this function
#print(mappedSents)



#Step 5- Get the sense of the word. In order to attain a quality set of distractors we need to get the right sense of the keyword. This is explained in detail in the seperate alogrithm documentation
def getWordSense(sent,word):
    word=word.lower() 
    if len(word.split())>0: #Splits the word with underscores(_) instead of spaces if there are multiple words
        word=word.replace(" ","_")
    synsets=wn.synsets(word,'n') #Sysnets from Google are invoked
    if synsets:
        wup=max_similarity(sent,word,'wup',pos='n')
        adapted_lesk_output = adapted_lesk(sent, word, pos='n')
        lowest_index=min(synsets.index(wup),synsets.index(adapted_lesk_output))
        return synsets[lowest_index]
    else:
        return None
#print("fin")


#Step 6- Get distractor from WordNet. These distractors work on the basis of hypernym and hyponym explained in detail in the documentation.
def getDistractors(syn,word):
    dists=[]
    word=word.lower()
    actword=word
    if len(word.split())>0: #Splits the word with underscores(_) instead of spaces if there are multiple words
        word.replace(" ","_")
    hypernym = syn.hypernyms() #Gets the hypernyms of the word
    if len(hypernym)==0: #If there are no hypernyms for the current word, we simple return the empty list of distractors
        return dists
    for each in hypernym[0].hyponyms(): #Other wise we find the relevant hyponyms for the hypernyms
        name=each.lemmas()[0].name()
        if(name==actword):
            continue
        name=name.replace("_"," ")
        name=" ".join(w.capitalize() for w in name.split())
        if name is not None and name not in dists: #If the word is not already present in the list and is different from he actial word
            dists.append(name)
    return dists
#print("fin")




#Step 7- The primary goal of this step is to take our MCQ quality one step further. The WordNet might some times fail to produce a hypernym for some words.
#In that case the ConcepNet comes into play as they help achieve our distractors when there are no hypernyms present for it in the WordNet. More about this is discussed in the algorithm documentation.
def getDistractors2(word):
    word=word.lower()
    actword=word
    if len(word.split())>0: #Splits the word with underscores(_) instead of spaces if there are multiple words
        word=word.replace(" ","_")
    dists=[]
    url= "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5"%(word,word) #To get ditractors from ConceptNet's API
    obj=requests.get(url).json()
    for edge in obj['edges']:
        link=edge['end']['term']
        url2="http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10"%(link,link)
        obj2=requests.get(url2).json()
        for edge in obj2['edges']:
            word2=edge['start']['label']
            if word2 not in dists and actword.lower() not in word2.lower(): #If the word is not already present in the list and is different from he actial word
                dists.append(word2)
    return dists




#Step 8- Find and map the distractors to the keywords
mappedDists={}
for each in mappedSents:
    wordsense=getWordSense(mappedSents[each][0],each) #gets the sense of the word
    if wordsense: #if the wordsense is not null/none
        dists=getDistractors(wordsense,each) #Gets the WordNet distractors
        if len(dists)==0: #If there are no WordNet distractors available for the current word
            dists=getDistractors2(each) #The gets the distractors from the ConceptNet API
        if len(dists)!=0: #If there are indeed distractors from WordNet available, then maps them
            mappedDists[each]=dists
    else: #If there is no wordsense, the directly searches/uses the ConceptNet
        dists=getDistractors2(each)
        if len(dists)>0: #If it gets the Distractors then maps them
            mappedDists[each]=dists
#print(mappedDists)





mcqs_list = []

# Step 9: Present MCQs in a nice and readable manner
iterator = 1  # To keep the count of the questions
for each in mappedDists:
    sent = mappedSents[each][0]
    p = re.compile(each, re.IGNORECASE)  # Converts into regular expression for pattern matching
    op = p.sub("________", sent)  # Replaces the keyword with underscores(blanks)
    question = {"question_number": iterator, "question_text": op, "options": []}
    options = [each.capitalize()] + mappedDists[each]  # Capitalizes the options
    options = options[:4]  # Selects only 4 options
    opts = ['a', 'b', 'c', 'd']
    random.shuffle(options)  # Shuffle the options so that the order is not always the same
    for i, ch in enumerate(options):
        question["options"].append({"option_letter": opts[i], "option_text": ch})
    mcqs_list.append(question)
    iterator += 1  # Increase the counter

# Convert the list of MCQs to JSON format
mcqs_json = json.dumps(mcqs_list, indent=4)

# Save the MCQs to a file
with open('mcqs.json', 'w') as file:
    file.write(mcqs_json)

# Display a confirmation message
print("MCQs saved to mcqs.json")


# # Step 9: Present MCQs in a nice and readable manner
# # print("**************************************        Multiple Choice Questions        *******************************")
# # print()
# iterator = 1  # To keep the count of the questions
# for each in mappedDists:
#     sent = mappedSents[each][0]
#     p = re.compile(each, re.IGNORECASE)  # Converts into regular expression for pattern matching
#     op = p.sub("________", sent)  # Replaces the keyword with underscores(blanks)
#     print("Question %s-> " % (iterator), op)  # Prints the question along with a question number
#     options = [each.capitalize()] + mappedDists[each]  # Capitalizes the options
#     options = options[:4]  # Selects only 4 options
#     opts = ['a', 'b', 'c', 'd']
#     random.shuffle(options)  # Shuffle the options so that the order is not always the same
#     for i, ch in enumerate(options):
#         print("\t", opts[i], ") ", ch)  # Print the options
#     print()
#     iterator += 1  # Increase the counter

# # Get the MCQs as a string
# mcqs = mcq_string.getvalue()

# # Restore stdout to its original value
# sys.stdout = sys.__stdout__

# # Save the MCQs to a file
# with open('mcqs.txt', 'w') as file:
#     file.write(mcqs)

# # Display a confirmation message
# print("MCQs saved to mcqs.txt")



# #Step 9- The final step is to present our MCQ in a nice and readable manner.
# print("**************************************        Multiple Choice Questions        *******************************")
# print()
# iterator = 1 #To keep the count of the questions
# for each in mappedDists:
#     sent=mappedSents[each][0]
#     p=re.compile(each,re.IGNORECASE) #Converts into regular expression for pattern matching
#     op=p.sub("________",sent) #Replaces the keyword with underscores(blanks)
#     print("Question %s-> "%(iterator),op) #Prints the question along with a question number
#     options=[each.capitalize()]+mappedDists[each] #Capitalizes the options
#     options=options[:4] #Selects only 4 options
#     opts=['a','b','c','d']
#     random.shuffle(options) #Shuffle the options so that order is not always same
#     for i,ch in enumerate(options):
#         print("\t",opts[i],") ", ch) #Print the options
#     print()
#     iterator+=1 #Increase the counter


