from flask_restful import Resource, request

import pandas as pd
import numpy as np
from flask import Response
import re
from sklearn.feature_extraction.text import TfidfVectorizer

class IdfGenratorResource(Resource):

    def get(self):

        mode = request.args.get('mode')
       
        df = self.get_dataset()

        if(mode == 'manual'):
            self.create_idf_manually(df)
        else:
            self.create_idf_sklearn(df)

        return Response('successfully created', mimetype='application/json')

       

    def create_idf_sklearn(self, df):
        
        # Create TfidfVectorizer object, remove stop_words, convert in lowercase.
        vector = TfidfVectorizer(
                            stop_words='english', 
                            lowercase=True,
                            use_idf=True, 
                            norm=u'l2',
                            smooth_idf=True
                            )
        vector.fit_transform(df['content'])   

        # Create a dataframe with words and idf value
        idf = pd.DataFrame({'feature_name':vector.get_feature_names(), 'idf_weights':vector.idf_})
        idf = idf.sort_values('idf_weights', ascending=True)

        idf.to_csv("datasets/idf.csv", index = False)

        return idf

    def create_idf_manually(self, df):

        # Create new column with a list of words, Keeping only letters, numbers and blanks
        df['tokens'] = [re.sub(r'[^A-Za-z0-9 ]+', '', x).lower().split() for x in df.content.values]

        # Create list with all words without duplicates
        tokens = list(set([item for sublist in df.tokens for item in sublist]))
        
        # Calculate idf
        idf = pd.Series([np.log((float(df.shape[0])+1)/(len([x for x in df.tokens.values if token in x])+1))+1 for token in tokens])

        # Define the words as index to concatenate it with tf
        idf.index = tokens
        idf = idf.reset_index()

        idf.rename(columns={ idf.columns[0]: "feature_name" }, inplace = True)
        idf.rename(columns={ idf.columns[1]: "idf_weights" }, inplace = True)

        idf.to_csv("datasets/idf.csv", index = False)

        return idf

    def get_dataset(self):
        df1 = pd.read_csv("datasets/articles1.csv")
        df2 = pd.read_csv("datasets/articles2.csv")
        df3 = pd.read_csv("datasets/articles3.csv")

        frames = [df1, df2, df3]
        df = pd.concat(frames, axis=0, ignore_index=True)

        # Remove rows with title or content nulls
        df = df[pd.isna(df['title'])==False]
        df = df[pd.isna(df['content'])==False]

        return df
