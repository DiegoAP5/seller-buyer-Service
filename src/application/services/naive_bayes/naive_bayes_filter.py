import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

class NaiveBayesFilter:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()
    
    def train(self, clean_data, offensive_data):
        X = clean_data + offensive_data
        y = [0] * len(clean_data) + [1] * len(offensive_data)
        X_vec = self.vectorizer.fit_transform(X)
        self.model.fit(X_vec, y)
    
    def save_model(self, model_path, vectorizer_path):
        with open(model_path, 'wb') as model_file, open(vectorizer_path, 'wb') as vectorizer_file:
            pickle.dump(self.model, model_file)
            pickle.dump(self.vectorizer, vectorizer_file)
    
    def load_model(self, model_path, vectorizer_path):
        with open(model_path, 'rb') as model_file, open(vectorizer_path, 'rb') as vectorizer_file:
            self.model = pickle.load(model_file)
            self.vectorizer = pickle.load(vectorizer_file)
    
    def censor(self, text):
        words = text.split()
        censored_text = []
        for word in words:
            if self.is_offensive(word):
                censored_text.append('***')
            else:
                censored_text.append(word)
        return ' '.join(censored_text)
    
    def is_offensive(self, text):
        text_vec = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vec)
        return prediction[0] == 1

clean_comments = ["Esta muy bueno", "Esta con madres", "Compren", "Esa bien vergas", "Esta bien verga", "Me quedó al pedo"]
offensive_comments = ["Puto", "Pendejo", "Desgraciado", "Mampo", "Esta de la verga", "Pendejos", "Mampos", "Mampito", "ctm","CTM","chinga tu madre","verga","vergas"]

filter = NaiveBayesFilter()
filter.train(clean_comments, offensive_comments)
filter.save_model('naive_bayes_model.pkl', 'vectorizer.pkl')
