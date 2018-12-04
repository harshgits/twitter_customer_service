# class that uses GCP to analyze sentiment in text

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account
from pathlib import Path
import re
from pprint import pprint

class GCPSentiment:
    
    def __init__(self, credentialspath):
        # authenticate
        self.client = language.LanguageServiceClient(credentials = \
            service_account.Credentials.from_service_account_file(
                credentialspath
                )
            )
        
    # sentiment for full document
    def get_sentiment(self, text, language_str = "en"):
        document = types.Document(
            content = text,
            type = enums.Document.Type.PLAIN_TEXT,
            language = language_str
            )

        sentiment = self.client.analyze_sentiment(
            document = document).document_sentiment
    
        score, magnitude = sentiment.score, sentiment.magnitude
        return {"score": score, "magnitude": magnitude}
    
    # sentiments for sentences in a list
    def get_sentence_sentiments(self, sentences, language_str = "en"):

        def standardize_sentence(s):
            
            # remove punctuation
            s = re.sub(r'[^a-zA-Z0-9\s]', '', s)
            
            # strip off end spaces
            s = s.strip()
            
            # standardize whitespace
            s = re.sub(r'\s+', ' ', s)
            
            # lower case
            s = s.lower()
            
            # if sentence is whitespace, replace with neutral word "And"
            if len(s) < 5 or re.match(r"\s+", s):
                s = "Rather" + s
            
            # use "|" to indicate end of sentence
            s = s + " |"
            
            return s
        
        # joining sentences into para
        def sens_to_para(sentences):

            # standardize the sentences
            sentences = list(map(
                standardize_sentence, sentences
                ))

            # make paragraph
            para = "\n".join(sentences)
            return para
        
        para = sens_to_para(sentences)
        
        # turning para into Document obj
        document = types.Document(
            content = para,
            type = enums.Document.Type.PLAIN_TEXT,
            language = language_str
            )
        
        # getting sentence_sentiment objects
        senten_sentis = self.client.analyze_sentiment(
            document = document).sentences
        
        # extracting numerical scores
        scores = [ss.sentiment.score for ss in senten_sentis]
        return scores