from models import Products
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
import re

mystem = Mystem()
russian_stopwords = stopwords.words("russian")


class Clustering(object):
    """docstring for Clustering."""

    def __init__(self):
        super(Clustering, self).__init__()
        self.get_names()

    def get_names(self):
        skip = 0
        while True:
            products = Products.objects.skip(skip).limit(10000).only('name')
            names = [p.name for p in products]
            with open('out.csv', 'a') as file:
                file.write('\n'.join(names).strip())
                file.close()
            skip += 10000
            print('+ 10 000')

    def preprocess_text(self, text):
        text = re.sub(r'\W+', ' ', text)
        tokens = mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token not in russian_stopwords
                  and token != " "
                  and token.strip() not in punctuation]
        text = " ".join(tokens)
        return text


clusters = Clustering()
