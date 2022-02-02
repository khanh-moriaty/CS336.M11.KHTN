class Model:
    
    def __init__(self, df_corpus):
        raise NotImplementedError()

    def query(self, df_query):
        raise NotImplementedError()

    def __call__(self, df_query):
        return self.query(df_query)