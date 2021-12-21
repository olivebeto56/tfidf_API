from flask_restful import Resource, request
from flask import Response
import re
import pandas as pd
import json     
from bs4 import BeautifulSoup
from urllib.request import urlopen

class TfidfResource(Resource):

    def get(self):
        url = request.args.get('url')
        limit = request.args.get('limit')

        text = self.get_text_url(url)
        tf = self.get_tf(text)
        idf = self.get_idf_stored()

        tfidf = self.calculate_tfidf(tf, idf)

        # Limit the number of terms requested
        tfidf = tfidf[:int(limit)]

        result = {
            "terms": tfidf.to_dict(orient="records")
        }

        return Response(json.dumps(result), mimetype='application/json')


    def get_idf_stored(self):
        idf = pd.read_csv("datasets/idf.csv", index_col=0)

        # Remove duplicate terms
        idf = idf.loc[~idf.index.duplicated(keep='first')]

        return idf

    def calculate_tfidf(self, tf, idf):

        tfidf = pd.concat([tf, idf], axis=1, join="inner")
        tfidf['tf-idf'] = tfidf['tf'] * tfidf['idf_weights']
        tfidf = tfidf.sort_values('tf-idf', ascending=False)
                
        # Reset the index to use it as a column
        tfidf = tfidf.reset_index()
        tfidf = tfidf.rename({'feature_name': 'term'}, axis=1)

        # Keep only columns term and tf-idf
        tfidf = tfidf[['term', 'tf-idf']]

        return tfidf

    def get_tf(self, text):
        # Add text to a dataframe to handle it easier
        df =  pd.DataFrame({'content': [text]})

        # Convert text to lowercase and divide it by word to return list
        df['tokens'] = [x.lower().split() for x in df.content.values] 
        
        # calculate how many times the words appears and divide it by the total.
        # Transpose the dataframe
        tf = df.tokens.apply(lambda x: pd.Series(x).value_counts()/len(x)).T
        tf = tf.set_axis(['tf'], axis=1, inplace=False)
        
        # Define the words column as index to concatenate it with idf
        tf.index.name = 'feature_name'

        # Remove duplicated
        tf = tf.loc[~tf.index.duplicated(keep='first')]

        return tf
        
    def get_text_url(self, url):

        page = urlopen(url)
        html = page.read().decode("utf-8", errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        # Only keep letters, numbers and blanks
        text = re.sub(r'[^A-Za-z0-9 ]+', '', text)

        return text
