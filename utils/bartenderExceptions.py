class BartenderException(Exception):
    '''
    Class to through an exception related to the bartender
    '''
    def __init__(self, message, error):
        super().__init__(message)
        self.error = error
        self.message = message
        print("Error: {} Message: {}".format(error, message))

    def getMessage(self) -> str:
        return self.message

    def getError(self) -> str:
        return self.error