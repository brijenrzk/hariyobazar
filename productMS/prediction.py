import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import *


def title_recommendations(title):
    mov = Product.objects.all()

    product = pd.DataFrame()
    lis = []
    for m in mov:
        lis.append(m.name)

    product['title'] = lis

    # Break up the big genre string into a string array
    # product['description'] = product['description'].str.split('|')
    # Convert description to string value

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2),
                         min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(product['title'])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Build a 1-dimensional array with movie titles
    titles = product['title']
    indices = pd.Series(product.index, index=product['title'])
    print(indices)

    # Function that get product recommendations based on the cosine similarity score of product description

    idx = indices[title]
    print(idx)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    print(sim_scores)
    product_indices = [i[0] for i in sim_scores]
    return titles.iloc[product_indices]
