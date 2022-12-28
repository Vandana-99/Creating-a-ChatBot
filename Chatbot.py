#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing required libraries - NLTK,io,random,string,numpy,pandas
import nltk
import io
import random
import string 
import numpy as np
import pandas as pd

#reading the training data
df=pd.read_csv("/Users/vandanabharatha/Desktop/training.csv",encoding="cp1252")
nltk.download('punkt') #divides text into list of sentences
nltk.download('wordnet') # to find the meanings of words, synonyms.

#accessing the training data 
question=df['question'].tolist() #accessing the question column data
answer=df['answer'].tolist()     #accessing the answer column data

remove_punctuation = dict((ord(punct), None) for punct in string.punctuation) #removing punctuation from the training data


#importing required libraries - WordNetLemmatizer
from nltk.stem import WordNetLemmatizer
lemmer = nltk.stem.WordNetLemmatizer() #for performing lemmatization


#Lemmatization
def Lem_Tokens(tokens):  #for generating tokens
    return [lemmer.lemmatize(token) for token in tokens] #returns a list of lemmatized tokens using the WordNet dictionary.

def Lem_Normalize(Text):  #for normalizing the lemmatized tokens
    return Lem_Tokens(nltk.word_tokenize(Text.lower().translate(remove_punctuation))) #returns the list of tokens in lower case with the punctuation marks removed


#Greeting responses
greeting_inputs = ["hello", "hi", "greetings","what's up","hey"]
greeting_responses = ["hi", "hey", "hi there", "hello", "Hi Vandana"]
def greetings(sentence):
    for word in sentence.split():
        if word.lower() in greeting_inputs:
            return random.choice(greeting_responses)
        

#importing required libraries - TfidfVectorizer,cosine_similarity,CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


#Chatbot replies to the user
def reply(input_text):        #used for bot replies
    text=input_text.lower()   #converting input text into lowercase
    
    noun=[]
    is_noun=lambda pos:pos[:2] == 'NN'        #generating singular nouns from the training data
    tokenized=nltk.word_tokenize(input_text)         
    nouns=[word for (word,pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
    
    if "he" in text.split():
        #print(noun)
        text=text.replace('he','noun[0]')
    
    #Generating response
    response=''
    question.append(text)
    vectorizer = CountVectorizer(min_df=1,tokenizer=Lem_Normalize, stop_words=remove_punctuation)  #transforming the text into array of vectors
    vectorized_data = vectorizer.fit_transform(question)               #converting the question(input_text) into array of vectors
    matrix = cosine_similarity(vectorized_data[-1],vectorized_data)    #for generating the question(input_text) into a matrix of TF-IDF features
    
    index=matrix.argsort()[0][-2]  #finding the index of question
    single_array = matrix.flatten() #To get a copy of genertaed array into one dimension
    single_array.sort()
    request = single_array[-2]      #for taking the user request

    if(request==0):                 #for checking the user request condition(if no match)
        robo_response=response+ "Iam sorry, I didn't understand that..."  #responds as sorry
        question.remove(text)
        return robo_response
    
    else:
        num1=""                   
        num2=""
        for i in input_text:      #used for checking the digits in the input text
               if i.isdigit():       
                      num1=num1+i 
        for i in question[index]: #used for checking the digits in the question 
               if i.isdigit():
                      num2=num2+i
                      
        n=0
        m=0
        if len(num1)>=1:
            n+=int(num1)
        if len(num2)>=1:
            m+=int(num2)
            
        if n:
            if input_text==question[index]:            # for digit in input_text and the question index matching 
                response=response+answer[index]
                question.remove(text)
                return response                        #returns answer as a response
            elif n>0 and m==0:                         # for digits with the paraphrase text
                response=response+answer[index]
                question.remove(text)
                return response
                
            else:
                chatbot_response=response+ "Iam sorry, I didn't understand that.."  #for responses with no matching of question and input data
                question.remove(text) 
                return chatbot_response
        else:
            response = response+answer[index]    #question and answer matches
            question.remove(text)
            return response                      #returns answer as a response
#importing required GUI library - tkinter        
import tkinter
from tkinter import *

def interact():                     #for interaction between user and the bot in the GUI
    ChatLog.config(state=NORMAL)
    ChatLog.tag_config('Bot',foreground='Light green',font=('bold'))           #for bot configuration
    ChatLog.tag_config('User',foreground='midnight blue',font=('bold'))        #for user confguration
    
    text=EntryBox.get("1.0","end-1c").strip()
    EntryBox.delete("0.0",END)
    #print("User:" + input_text)
    ChatLog.insert(END,"User: " + text + '\n','user')
    continue_discussion=True    #starting the conversation with the bot
    
    if(continue_discussion == True):               
        if(text=="bye"):                                                     #checks if  user input condition equals to bye
            ChatLog.insert(END,"BOT: Bye.. Its nice to chat with you"+ '\n','bot') #response in the GUI
        else:   
            if(text!='bye'):                                                           #for condition if user input not equal to bye
                if(text=='thanks' or text=='thank you very much' or text=='thank you'): #checks condition for thanks
                    continue_discussion = False          
                    ChatLog.insert(END,"BOT: You are welcome"+ '\n','bot')             #response in the GUI
                
                else:
                    if(greetings(text)!=None):           
                        ChatLog.insert(END,"BOT: "+greetings(text)+ '\n','bot')        #greeting response in the GUI
                    else:
                        ChatLog.insert(END,"BOT: "+reply(str(text))+ '\n','bot')     #answer response in the GUI
                    
                        
    else:
        continue_discussion=False                       #ending the bot conversation
        ChatLog.insert(END,"BOT: Bye.. Its nice to chat with you... Have a nice day..."+ '\n','bot')
        print("BOT: bye..")
        ChatLog.insert(END,"BOT: Thanks for chatting,bye" + '\n','bot')
        ChatLog.yview(END)
        ChatLog.config(state=DISABLED)
                           
#welcome message in the GUI                           
def welcome():
    ChatLog.tag_config('welcome',foreground='black',font=("Arial",20,'bold'))
    ChatLog.insert(END, 'Hi Vandana,Iam a chat bot' + '\n\n','welcome')
    ChatLog.insert(END,'How can I help you?' + '\n\n','welcome')

    
#Generating GUI 
base=Tk()               #for displaying the root window all the other components
base.title("Chatbot")   #setting the title of the GUI
base.geometry("600x800")
base.resizable(width=FALSE, height=FALSE)

#Creating chat window
ChatLog = Text(base, bd=0, bg="white",foreground='black', height="8", width="50",font=("Helvetica",18))
welcome()
ChatLog.config(state=DISABLED)

#Adding scrolllbar to Chat window
scroll_bar = Scrollbar(base, command=ChatLog.yview)
ChatLog['yscrollcommand'] = scroll_bar.set

#Creating send button
SendButton = Button(base, font=("verdana",18,'bold'), text ="Send",width="4", height=3,bd=0,bg="spring green",activebackground="sea green",fg='dark green',command=interact)

#Creating the box to enter search term
EntryBox = Text(base, bd=0, bg="white",width="30", height="5",font="Arial")

#placing all components on screen
scroll_bar.place(x=578,y=6,height=686)
ChatLog.place(x=8,y=6,height=686, width=568)
EntryBox.place(x=96, y=701, height=90,width=500)
SendButton.place(x=10,y=701,height=90)
base.mainloop()  #runs the GUI tkinter event loop












