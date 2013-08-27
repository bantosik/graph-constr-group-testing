class PathTester(object):
    def __init__(self, faulty_set):
        self.faulty_set = faulty_set
        self.positive_queries = 0
        self.negative_queries = 0
    
    def test_path(self, path):
        result = any((x in self.faulty_set) for x in path)
        if result:
            self.positive_queries = self.positive_queries + 1
        else:
            self.negative_queries = self.negative_queries + 1
        return result 
    
    def get_all_queries(self):
        return self.positive_queries + self.negative_queries
    
    def get_negative_queries(self):
        return self.negative_queries
    
    def get_positive_queries(self):
        return self.positive_queries
    
        
            