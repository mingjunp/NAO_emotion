import time
import sys
import oceanreduced as ocean
#import OCEANv2 as ocean
import emotionAPI as emotion
import takephoto
import NaoResponse as naoResponse
from random import randint


from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker

from optparse import OptionParser


class FaceDetModule(ALModule):

    def __init__(self,name):
        self.IP = "169.254.67.213"
        self.PORT = 9559
        ALModule.__init__(self, name)
        try:
            global memory
            memory = ALProxy("ALMemory",self.IP,self.PORT)
        except Exception as e:
            print("Error: ",e)
        try:
            global faceProxy
            faceProxy = ALProxy("ALFaceDetection",self.IP,self.PORT)
        except Exception as e:
            print("Error: ",e)
        try:
            global asr
            asr = ALProxy("ALSpeechRecognition",self.IP,self.PORT)
        except Exception as e:
            print("Error: ",e)
        try:
            global tts
            tts = ALProxy("ALTextToSpeech",self.IP,self.PORT)
        except Exception as e:
            print("Error: ",e)

        vocabulary = ["x"]
        asr.pause(True)
        asr.setLanguage("English")
        asr.setVocabulary(vocabulary,False)
        asr.pause(False)
        memory.subscribeToEvent("FaceDetected","FaceDet","onFaceDetected")
        tts.setVolume(0.9)

    # This will be called each time a face is detected.
    def onFaceDetected(self, eventName, value, subscriberIdentifier):
        # Unsubscribe to the event when talking, to avoid repetitions
        try:
            memory.unsubscribeToEvent("FaceDetected","FaceDet")
        except IndexError as e:
            print(e)

        tts.say("face detected success")

        try:
            persona = value[1][0][1][2] #see if this person is exist
            if persona == "":
                valOcean = ocean.main()
                #Preguntar nombre persona
                nombre = crearNombre(valOcean)
                print(nombre)

                #Puede to open in the main and here (twice) problems
                #"oceanProfiles.txt"

                OCEANProfiles = open("oceanProfiles.txt","a")
                # Escribimos values of the person in the file
                #perfiles OCEAN
                OCEANProfiles.write(nombre+"\n")
                OCEANProfiles.write(str(valOcean)+"\n")
                OCEANProfiles.close()

                #Nao learns the person's face
                faceProxy.learnFace(nombre)

            else:
                #open ocean file
                archnombres = open("OCEANProfiles.txt").read().split()
                #obtain file name position
                #de profiles ocean
                nom = archnombres.index(persona)
                valPersona = archnombres[nom+1]
                #Take photo for this person
                takephoto.main()
                #send to Microsoft API
                emotions,values = emotion.detEmotion("./emotion.png")
                if values == []:
                    tts.say("the photo is too blurry to detect emotion")
                else:
                    print(emotions)
                    print(values)
                    x = max(values)
                    pos = values.index(x)
                    print(emotions[pos]+": "+str(x))
                    tts.say("Emotion detection success.")
                    tts.say("Emotion: "+emotions[pos])
                    # nao responses to different emotions
                    tts.say(naoResponse.emotionResponse(emotions[pos]))
                #archnombres.close()
        except IndexError as e:
            print(e)
        # Subscribe again to the event
        memory.subscribeToEvent("FaceDetected","FaceDet","onFaceDetected")

def crearNombre(valOcean):
    nombre = "persona"+str(randint(10,99))
    for i in valOcean:
        nombre+=str(i)
    return nombre

def main():
    print("control+c to ShutDown")

    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip="169.254.67.213",
        pport=9559)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port


    # Warning: FaceDet must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global FaceDet
    FaceDet = FaceDetModule("FaceDet")

    global OCEANProfiles
    OCEANProfiles = open("oceanProfiles.txt","a")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")
        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()
