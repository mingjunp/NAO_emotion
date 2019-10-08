def emotionResponse(emotion):
    def anger():
        return "Why are you being so angry?"

    def contempt():
        return "What is going on?"

    def disgust():
        return "What is going on?"

    def fear():
        return "Don't worry. I am here."

    def happiness():
        return "I am glad to see you are happy."

    def neutral():
        return "Do you want to play with me?"

    def sadness():
        return "I am sorry that you had a bad day."

    def surprise():
        return "Surprise!"

    options = {
        "Anger": anger,
        "Contempt": contempt,
        "Disgust": disgust,
        "Fear": fear,
        "Happiness": happiness,
        "Neutral": neutral,
        "Sadness": sadness,
        "Surprise": surprise
    }

    return options[emotion]()
