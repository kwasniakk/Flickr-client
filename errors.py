class IncorrectFormat(Exception):
    __module__ = 'builtins'
    def __init__(self, db_file, message = "Please specify a correct database format (.db)"):
        self.db_file = db_file
        self.message = message
    
    def __str__(self):
        return self.message


class ConnectionFailure(Exception):
    __module__ = 'builtins'
    def __init__(self, status, message = "Cannot get an answer from Flickr API. Cannot proceed"):
        self.status = status
        self.message = message
    
    def __str__(self):
        return self.message