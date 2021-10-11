from urllib import request

STOP_WORDS = request.urlopen(
    "https://raw.githubusercontent.com/stopwords-iso/stopwords-el/master/raw/stop-words-greek.txt").read().decode("utf8").split("\r")
STOP_WORDS = [stop_word.strip()
              for stop_word in STOP_WORDS if len(stop_word.strip()) > 0]
STOP_WORDS.append('αὐτός')
