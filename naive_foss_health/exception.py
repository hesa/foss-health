
class NfhcException(Exception):

    def __init__(self, error_code, error_message=None):
        self._error_code = error_code
        if error_message is None:
            self._error_message = self._error_code.value[1]
        else:
            self._error_message = error_message

    def error_code(self):
        return self._error_code.value[0]

    def error_message(self):
        return self._error_message
