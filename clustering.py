from models import Products, Categories
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
import re

mystem = Mystem()
russian_stopwords = stopwords.words("russian")


class Clustering(object):
    """docstring for Clustering."""
    categories = dict()

    def __init__(self):
        super(Clustering, self).__init__()
        self.get_names()
        self.categories = {c.wb_id: c.name for c in Categories.objects.all()}

    def get_names(self):
        skip = 0
        while True:
            products = Products.objects.skip(skip).limit(1000)
            for product in products:
                if len(product.sizes) > 2:
                    if (product.sizes[-1].quantity is not None
                            and product.sizes[-2].quantity is not None):
                        with open('out.csv', 'a') as file:
                            line = str(product.sizes[-2].quantity) + ';'
                            line += str(product.sizes[-1].quantity) + ';'
                            line += str(product.category_wb_id) + ';'
                            line += product.name + '\n'
                            file.write(line)
                            file.close()
            skip += 1000
            print('+ 10 00')

    def preprocess_text(self, text):
        text = re.sub(r'\W+', ' ', text)
        tokens = mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token not in russian_stopwords
                  and token != " "
                  and token.strip() not in punctuation]
        text = " ".join(tokens)
        return text


clusters = Clustering()
