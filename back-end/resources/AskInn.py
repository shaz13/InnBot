import time
import os
import pickle
import gc
import gensim
import nltk
import re
import pandas as pd
import numpy as np
import warnings; warnings.simplefilter('ignore')
from flask_restful import Resource
from flask import request
from ast import literal_eval
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from gensim.models import Word2Vec, doc2vec
from gensim.models.doc2vec import TaggedDocument
from nltk.tokenize import word_tokenize
from .InnBot import GetSolution

class AskInn(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        try:
        	query = json_data["query"]
        	# print ()
        	body_df = GetSolution(str(query))
        	# print (sols)
        	return body_df["Resolution"].iloc[:5].to_dict()
        except:
            return {'message': 'Error contacting the API'}, 404
