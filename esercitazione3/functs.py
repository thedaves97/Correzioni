import string
import spacy
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
from wordcloud import WordCloud
import matplotlib.pyplot as plt


nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')


def read_sentences(file_name):
    '''
    Questa funzione legge il file Csv. Si effettua già una prima preparazione del corpus all'elaborazione.
    :param file_name: nome del file scelto;
    :return: le frasi contenute nel corpus appena letto.
    '''
    sents = []

    with open(file_name, 'r', encoding="utf-8") as lines:
        for line in lines :
            if len(line.split('<s>')) > 1:
                sents.append(line.split('<s>')[1].replace('</s>','').strip())
    return sents


def preprocessing(sentence):
    '''
    Questa funzione rimuove la punteggiatura e trasforma ogni carattere della frase in minuscolo.
    :param sentence: frase del corpus;
    :return: frase senza punteggiatura.
    '''

    sentence = [s.lower() for s in sentence]
    sentence = [''.join(c for c in s if c not in string.punctuation) for s in sentence]

    return sentence


p_subj = {'subj', 'nsubjpass', 'nsubj'}
p_obj = {'pobj', 'dobj', 'obj', 'iobj'}


def parse_find_subj_obj(sent, i):
    '''
    Attraverso questa funzione si effettua il parsing della frase atraverso la funzione nlp della libreria Spacy.
    In questo modo è possibile trovare le dipendenze di ogni parola e quindi trovare il soggetto e l'oggetto della
    frase.
    :param sent: frase su cui effettuare il parsing;
    :param i: contatore per risultati intermedi (utile solo a fini di stampa);
    :return: soggetto e oggetto della frase.
    '''
    o = None
    s = None

    sent = nlp(sent)
    #print(elem.text, elem.lemma_, elem.pos_, elem.tag_, elem.dep_, elem.shape_, elem.is_alpha, elem.is_stop)
    '''
    Risultato della funzione nlp della libreria Spacy
    elem.text: parola, elem.lemma_: parola lemmatizata, 
    elem.pos_: PoS della parola, elem.tag_: PoS più dettagliato,
    elem.dep_: dipendenza della parola nella frase, elem.shape_: indica la forma della parola (maiuscole, cifre, punteggiatura)
    elem.is_alpha: , elem.is_stop: True/False, indica se la parola è una stopword o no
    '''

    for elem in sent:
            if elem.dep_ in p_subj:
                if elem.lemma_ != "-PRON-":
                    s = elem.lemma_
                else:
                    s = elem.text
            if elem.dep_ in p_obj:
                if elem.lemma_ != "-PRON-":
                    o = elem.lemma_
                else:
                    o = elem.text

    parsed_sent(sent)

    #print("It ", i, "subj", s, " obj ", o)
    return s, o


def parsed_sent(sent):
    '''
    Questa funzione crea la lista delle frasi parsificate.
    :param sent: frase del corpus appena parsificata;
    :return:
    '''
    psd_sent = []
    psd_sent.append(sent)


def wsd(sent, subj, obj):
    '''
    Questa funzione effettua la WordSenseDisambiguation mediante il metodo lesk() fornito da WordNet restituendo il
    synset delle parole disambiguate.
    :param sent: frase del corpus;
    :param subj: soggetto della frase;
    :param obj: oggetto della frase;
    :return: synset relativi al soggetto ed oggetto.
    '''
    possible_subj = ["i", "you", "he", "she", "it", "we", "they"]
    sing_subj = ["i", "he", "she", "it"]
    plural_subj = ["we", "you" "they"]

    if subj in possible_subj or subj is None:
        if subj in plural_subj:
            ris = wn.synsets('people')[0]
        else:
            ris = wn.synsets('person')[0]
    elif subj is not None:
        ris = lesk(sent, subj)
        if ris is None:
            ris = wn.synsets('people')[0]
    else:
        ris = None
    if obj is not None:
        ris1 = lesk(sent, obj)
        if ris1 is None:
            #ris1 = wn.synsets('thing')[0]
            ris1 = wn.synsets('food')[0]
    else:
        ris1 = wn.synsets('food')[0]
        #ris1 = wn.synsets('thing')[0]


    #print("Ris ", ris, "Ris1 ", ris1)
    return ris, ris1


def super_sense(ris, ris1):
    '''
    Questa funzione prende i supersensi dei synset forniti dalla funzione wsd. Essi sono il risultato della funzione
    lexname().
    :param ris: synset disambiguato del soggetto;
    :param ris1: synset disambiguato dell' oggetto;
    :return: supersensi di soggetto e oggetto.
    '''
    #Prendiamo i supersensi
    if ris is not None or ris1 is not None:
        #print("Supersense/Tipo semantico per il filler")
        if ris is not None:
            ss1 = ris.lexname()
        else:
            ss1 = None
        if ris1 is not None:
            ss2 = ris1.lexname()
        else:
            ss2 = None
        #print("Subj supersense", ris.lexname())
        #print("Obj supersense", ris1.lexname(), "\n")
    else:
        #print("\nDisambiguazione = None\n")
        ss1 = None
        ss2 = None

    return ss1, ss2


def generate_word_cloud(slot):
    '''
    Genera la WordCloud relativa agli slot di filler di soggetto e oggetto trovati.
    :param slot: può essere l'insieme di soggetti/oggetti.
    :return:
    '''
    proc = list_to_string(slot)

    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stop_words,
                          min_font_size=10).generate(proc)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


def list_to_string(lista):
    '''
    Trasforma la lista in input in una stringa per la creazione della WordCloud.
    :param lista: lista di filler, ovvero lo slot di cui stiamo generando la WordCloud;
    :return: stringa composta da tutte le parole nella lista.
    '''
    trs = " ".join(lista)

    return trs


def menu():
    '''
    Mostra il menù iniziale per la scelta del corpus.
    :return:
    '''
    print("Choose the corpus to analyze: ")
    print("1 - To build;")
    print("2 - To cook;")

