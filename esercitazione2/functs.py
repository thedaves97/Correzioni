import csv
import string
from collections import Counter


from nltk import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet



def read_load_csv():
    '''
    Questa funzione legge il file Csv.
    :return: le definizioni contenute mel file file appena letto.
    '''
    with open('Input\content2form.csv', 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        definitions = []

        for col in csv_reader:
            definitions.append(col)

    return definitions

stop_words = stopwords.words('english')


def preprocessing(sent):
    '''
    Questa funzione viene richiamata quando si vogliono filtrare da una frase punteggiatura e stopword.
    Viene effettuata la riduzione di ogni carattere maiuscolo a minuscolo e la Lemmatizzazione.
    :param sent: singola frase presa dalla lista di frasi lette dal Csv;
    :return: frase preprocessata.
    '''
    sent = list(map(lambda a: a.lower(), sent))
    sent = list(filter(lambda a: a not in string.punctuation and a not in stop_words, sent))
    lemmatizer = WordNetLemmatizer()
    sent = list(map(lambda a: lemmatizer.lemmatize(a), sent))

    return sent


def get_genus(candidate_genus):
    '''
    Questa funzione cerca nella lista di parole, relative ad una definizione, il possibile genus.
    :param candidate_genus: passiamo le parole filtrate nel preprocessing tra cui scegliere il genus;
    :return: un certo numero di genus tra cui scegliere poi quello definitivo.
    '''

    dim = len(candidate_genus)
    n = int((dim*10)/100)
    most_frequent = Counter(candidate_genus).most_common(n)

    return [g[0] for g in most_frequent]


def get_synset(word):
    '''
    Questa funzione trova il synset della parola passata come parametro.
    :param word: si tratta di uno dei possibili genus appena trovati;
    :return: uno o più synsets relativi al parametro in input.
    '''
    return wordnet.synsets(word)


def get_hyp(synset):
    '''
    Questa funzione trova gli iponimi di un synset.
    :param synset: relativo ad un determinato genus;
    :return: uno o più iponimi.
    '''
    return synset.hyponyms()


def get_examples(synset):
    '''
    Questa funzione trova le frasi di esempio in WordNet relative ad un certo synset.
    :param synset: relativo ad un determinato genus.
    :return: il primo esempio relativo al synset preprocessato.
    '''
    ex = synset.examples()
    param = []
    if ex:
        return preprocessing(synset.examples()[0].split())
    return []


def get_definitions(synset):
    '''
    Questa funzione prende la definizione relativa al synset in WordNet.
    :param synset: relativo ad un determinato genus.
    :return: definizione preprocessata.
    '''
    return preprocessing(synset.definition().split())


def get_best_synset(candidate, genus):
    '''
    Questa funzione cerca il synset da restituire in output.
    :param candidate: lista di parole relativa ad un concetto;
    :param genus: lista di synset relativi alle parole di un concetto;
    :return: sysnet della parola più aderente alla lista di parole dei concetti fornita in input.
    '''
    res = None
    max_val = 0

    for g in genus:
        for synset in g:
            for hyp in get_hyp(synset):
                defs = set(get_definitions(hyp))
                ex = set(get_examples(hyp))

                if ex is not None:
                    defs = defs.union(ex)

                crs = len(defs.intersection(set(candidate)))

                if crs > max_val:
                    max_val = crs
                    res = hyp

    return res













