import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize, RegexpTokenizer, sent_tokenize
from nltk.corpus import stopwords


#remove punctuation and \n tokens '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
#    sent=[w for w in sentence if w.isalnum()]##not effective
def remove_punct(sentence):
    punctuations = ['.',':',',',';','?'
                    ,'!','/','[',']',
                    '(',')','{','}','"','-','|','`','^','~','<','>']
    sentence = [w for w in sentence if w not in punctuations]

    return sentence

def remove_stops(sentence): #Remove stop words
    stop_words = set(stopwords.words('english'))
    sentence = [w for w in sentence if w not in stop_words]
    return sentence

def preprocess(raw_input):
    sentences = sent_tokenize(raw_input)

    sentences = [word_tokenize(sent) for sent in sentences]
    sentences = [remove_punct(sent) for sent in sentences]##remove punctuations
    sentences = [remove_stops(sent) for sent in sentences]##remove stopwords
    #Add pos_tag for sentences
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def get_all_numerals(sentence):
    numbers_context = []
    for w in range(0,len(sentence)):
        ##Check for CD as POS tag of each word of the sentence
        if sentence[w][1]=='CD':
            ##push in context. Ensure the context exists irrespective of position of 'CD' within a sentence
            if w > 1:
                numbers_context.append(sentence[w-2])
            if w > 0:
                numbers_context.append(sentence[w-1])
            numbers_context.append(sentence[w])
            if w < len(sentence)-1:
                numbers_context.append(sentence[w+1])
            if w < len(sentence)-2:
                numbers_context.append(sentence[w+2])
    return numbers_context