from application.services.naive_bayes.naive_bayes_filter import NaiveBayesFilter

class CommentariesFilterService:
    def __init__(self):
        self.filter = NaiveBayesFilter()
        self.filter.load_model('naive_bayes_model.pkl', 'vectorizer.pkl')
    
    def censor_commentary(self, commentary):
        return self.filter.censor(commentary)
