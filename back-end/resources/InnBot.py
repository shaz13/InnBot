import gensim
import nltk
import re
import pandas as pd
import numpy as np
import time
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from gensim.models import Word2Vec, doc2vec
from gensim.models.doc2vec import TaggedDocument
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
stops = set(stopwords.words("english"))

def cleanData(text, lowercase = False, remove_stops = False, stemming = False):
    txt = str(text)
    txt = re.sub(r'[^A-Za-z0-9\s]',r'',txt)
    txt = re.sub(r'\n',r' ',txt)
    
    if lowercase:
        txt = " ".join([w.lower() for w in txt.split()])
        
    if remove_stops:
        txt = " ".join([w for w in txt.split() if w not in stops])
    
    if stemming:
        st = PorterStemmer()
        txt = " ".join([st.stem(w) for w in txt.split()])

    return txt

print ("Loading data and preprocessing...")
data = pd.read_csv("data.csv", engine='python')
data = data.dropna(subset=['Title','Resolution'])

raw_body_corpus = []
for i, line in enumerate(data['Resolution']): 
    raw_body_corpus.append(TaggedDocument(gensim.utils.simple_preprocess(line), [i])) 

raw_title_corpus = []
for i, line in enumerate(data['Title']):
    raw_title_corpus.append(TaggedDocument(gensim.utils.simple_preprocess(line), [i]))

body_corpus = []
for i, line in enumerate(data['Resolution']): 
    body_corpus.append(gensim.models.doc2vec.TaggedDocument(word_tokenize(line), [i]))   

title_corpus = []
for i, line in enumerate(data['Title']):
    title_corpus.append(gensim.models.doc2vec.TaggedDocument(word_tokenize(line), [i]))
epoch_body= 600
print ("Training Doc2Vec Body Model for title and resolution")
start = time.time()
model_for_body = doc2vec.Doc2Vec(vector_size =10000 ,window=6,
                                               min_count=10, 
                                               epochs=epoch_body, alpha=.12)
model_for_body.build_vocab(body_corpus)
model_for_body.train(body_corpus, 
                     total_examples=model_for_body.corpus_count, 
                     epochs=epoch_body) 
end = time.time()
print("Model trained and ready.")
print ("Model trained in {:.3f} minutes".format((end - start) / 60))
print("Access the API from the URL below or lauch the front-end index.html page to access InnBot Search.")
def GetSolution(query):
    user_query = query
    user_body_vec = model_for_body.infer_vector(gensim.utils.simple_preprocess(user_query), steps=10000)
    body_sims = model_for_body.docvecs.most_similar([user_body_vec], topn=10 ) 
    solutions = []
    title_sols = []
    sim_score = []

    for i in body_sims:
        solutions.append(" ".join(raw_body_corpus[i[0]].words))
        title_sols.append(" ".join(raw_title_corpus[i[0]].words)) 
        sim_score.append(i[1]) 
    solution_df = pd.DataFrame()
    solution_df['Title'] = title_sols
    solution_df['Resolution'] = solutions
    solution_df['Sim Score'] = sim_score
    body_df = solution_df
    return body_df