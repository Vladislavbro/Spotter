from models import Products, Categories
from nltk.corpus import stopwords
from pymystem3 import Mystem
import spacy
from string import punctuation
import re
import pandas as pd
from sklearn.cluster import DBSCAN, OPTICS, KMeans, Birch
import os
import numpy as np

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

mystem = Mystem()
russian_stopwords = stopwords.words("russian")

nlp = spacy.load('ru_core_news_md')


class Clustering(object):
    """docstring for Clustering."""
    categories = dict()
    df = None
    vectors = []
    eps = 0.5

    def __init__(self):
        super(Clustering, self).__init__()
        # self.categories = {c.wb_id: c.name for c in Categories.objects.all()}
        self.get_data()

    def get_data(self):
        skip = 0
        while True:
            products = Products.objects.filter(category_wb_id__gt=0).skip(skip).limit(1000)
            if len(products) == 0:
                break
            for product in products:
                if len(product.sizes) > 2:
                    if (product.sizes[-1].sales is not None
                            and product.sizes[-2].sales is not None):
                        with open('out.csv', 'a') as file:
                            line = str(product.sizes[-1].sales - product.sizes[-2].sales) + ';'
                            line += str(product.sizes[-2].sales) + ';'
                            line += str(product.sizes[-1].sales) + ';'
                            line += str(product.articul) + ';'
                            line += str(product.category_wb_id) + ';'
                            line += self.preprocess_text(product.name) + '\n'
                            file.write(line)
                            file.close()
            skip += 1000
            print('+ 10 00', skip)

    def preprocess_text(self, text):
        text = re.sub(r'\W+', ' ', text)
        tokens = mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token not in russian_stopwords
                  and token != " "
                  and token.strip() not in punctuation]
        text = " ".join(tokens)
        return text

    def get_vector(self, tokens):
        doc = nlp(tokens)
        return doc.vector

    def process(self):
        self.df = pd.read_csv(
            'out.csv',
            delimiter=';',
            names=['diff', 'day1', 'day2', 'articul', 'category_id', 'tokens']
        )
        self.df = self.df[self.df['diff'] > 0]
        self.df = self.df[self.df.tokens.str.len() > 1]
        self.df['vector'] = self.df.tokens.apply(self.get_vector)
        # for index, row in self.df.iterrows():
        #     self.vectors.append(self.get_vector(row['tokens']))

    def clustering(self):
        # encodings = np.array([d['encoding'] for d in self.data])
        df = pd.read_hdf('vectors.hdf')
        # clustering = DBSCAN(eps=2, min_samples=2)
        # clustering = OPTICS(n_jobs=-1)
        # clustering = KMeans()
        clustering.fit(np.array([v.tolist() for v in df.vector.to_numpy()]))
        df['labels'] = clustering.labels_
        for label in range(df.labels.min(), df.labels.max()):
            df[df.labels == label].tokens.to_csv(f'clusters/{label}.csv')

    def categories_clustering(self):
        df = pd.read_hdf('vectors.hdf')
        # df.drop(df.index[71208], inplace=True)
        # df['category_id'] = pd.to_numeric(df['category_id'])
        ids = list(set([int(id) for id in df.category_id.unique() if id != 'None']))
        for id in ids:
            subdf = df[(df['category_id'] == int(id)) | (df['category_id'] == str(id))]
            s = subdf.vector
            alg = 'KMeans'
            os.makedirs(f'out/{alg}/{id}', exist_ok=True)
            # clustering = DBSCAN(eps=1.5, min_samples=2)
            # clustering = OPTICS()
            clustering = KMeans(n_clusters=15)
            # clustering = Birch(n_clusters=30)
            clustering.fit(np.array([v.tolist() for v in s.to_numpy()]))
            subdf['labels'] = clustering.labels_
            print(id, len(clustering.labels_))
            for label in range(subdf.labels.min(), subdf.labels.max()):
                subdf[subdf.labels == label].tokens.to_csv(f'out/{alg}/{id}/{label}.csv')


clusters = Clustering()
