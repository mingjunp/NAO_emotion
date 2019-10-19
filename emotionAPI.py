########### Python 2.7 #############
import httplib, urllib, base64, ast, time, json

headers = {
    # Usage of octet-stream to allow the image to come from a file and not a URL
    'Content-type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'f7fc21ca05fc4150b409febc61151943',
}

params = urllib.urlencode({
    'returnFaceAttributes': 'age,gender,smile,emotion'
})

def detEmotion(image):
    f = open(image, "rb")
    body = f.read()
    try:
        i = time.time()
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse("")
        data = response.read()

        conn.close()

        response = json.loads(data)

        if response != []:
            faceAttributes = response[0]['faceAttributes']

            # other information
            smile = faceAttributes['smile']
            gender = faceAttributes['gender']
            age = faceAttributes['age']

            # emotions
            emotions = faceAttributes['emotion']
            anger = emotions['anger']
            contempt = emotions['contempt']
            disgust = emotions['disgust']
            fear = emotions['fear']
            happiness = emotions['happiness']
            neutral = emotions['neutral']
            sadness = emotions['sadness']
            surprise = emotions['surprise']

            emotion_names = ["Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise"]
            emotion_scores = [anger, contempt, disgust, fear, happiness, neutral, sadness, surprise]

            f = time.time()

            print(f-i)
            return emotion_names, emotion_scores
        else:
            emotion_names = ["Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise"]
            emotion_scores = []
            return emotion_names, emotion_scores

    except Exception as e:
        print(e)

        #print("[Errno {0}] {1}".format(e.errno, e.strerror))

    ####################################