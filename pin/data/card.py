class Card(object):
    """
    Helper object for development of tests. Provides mock method for sending message

    """

    def __init__(self, pin, expected_result):
        self._pin = pin
        self._expected = expected_result

    @property
    def pin(self):
        """ Pin is used to represent if card requires verification or not """
        return self._pin

    @pin.setter
    def pin(self, pin):
        """ Sets pin """
        self._pin = pin

    @property
    def expected(self):
        """ Expected value is used as mocked response from card """
        return self._expected

    @expected.setter
    def expected(self, expected_result):
        """ Sets expected value """
        self._expected = expected_result

    def send(self, hex_data_string):
        """ Mocking of sending message to card"""
        return self.expected
