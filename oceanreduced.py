import time
import random
from naoqi import ALProxy

def intro(preg,answers):
    tts.say(archtest[preg])
    answers.append("-1")
    time.sleep(1)
    nextQuestion(preg,answers)

def askQuestion(preg,answers):

    available_questions = archtest[slice(1,len(archtest))]

    # random choose a question
    question = random.choice(available_questions)

    # if already asked, random another one
    while archtest.index(question) in questions_asked:
        question = random.choice(available_questions)

    # say question
    tts.say(question)
    # add question index into asked list
    questions_asked.append(archtest.index(question))

    asr.subscribe("ocean")
    time.sleep(5)
    asr.unsubscribe("ocean")
    data = memory.getData("WordRecognized")
    print(data)
    answers.append(data[0])
    nextQuestion(preg,answers)

def nextQuestion(preg,answers):
    preg+=1
    if preg<=10:
        askQuestion(preg,answers)
    else:
        tts.say("Thank you for answering these questions.")
        calcOCEAN(answers)

def calcOCEAN(answers):
    Answers = []
    for i in answers:
        if i==-1:
            Answers.append(-1)
        elif i=="one":
            Answers.append(1)
        elif i=="two":
            Answers.append(2)
        elif i=="three":
            Answers.append(3)
        elif i=="four":
            Answers.append(4)
        elif i== "five":
            Answers.append(5)
        else:
            Answers.append(0)
    oceanValue = calcOCEANValue(Answers)
    return oceanValue

def calcOCEANValue(Answer):
    E = 20+Answer[1]-Answer[6]
    A = 14-Answer[2]+Answer[7]

    C = 14+Answer[3]-Answer[8]

    N = 38-Answer[4]+Answer[9]

    O = 8+Answer[5]-Answer[10]

    return E,A,C,N,O



def main():
    #Init global variables
    preg = 0
    answers = []
    IP = "169.254.67.213"

    #Create proxies with NaoQi Modules needed
    #ALTextToSpeech, ALSpeechRecognition, #ALMemory
    try:
        global tts
        tts = ALProxy("ALTextToSpeech",IP , 9559)
    except Exception as e:
        print("Error: x",e)
    try:
        global asr
        asr = ALProxy("ALSpeechRecognition",IP,9559)
    except Exception as e:
        print("Error: ",e)
    try:
        global memory
        memory = ALProxy("ALMemory",IP, 9559)
    except Exception as e:
        print("Error: ",e)

    #Set language in which he speaks NAO
    tts.setLanguage("English")
    tts.setVolume(0.9)
    #Vocabulary to recognize
    vocabulary = ["one","two","three","four","five"]
    #Pause of the voice recognition system for configuration
    asr.pause(True)
    asr.setLanguage("English")
    asr.setVocabulary(vocabulary,False)
    asr.pause(False)
    #Reading file questions Test Ocean
    global archtest
    global questions_asked
    questions_asked = []
    archtest = open("oceanQuestions.txt").read().split(".")
    intro(preg,answers)

    o = calcOCEAN(answers)
    return o
