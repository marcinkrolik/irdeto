class Message(object):
    """
    Message object encapsulates information about Command Message to send to card
    """

    def __init__(self, **kwargs):
        self._cla = kwargs.get("cla", "A4")
        self._ins = kwargs.get("ins", "20")
        self._p1 = kwargs.get("p1", "00")
        self._p2 = kwargs.get("p2", "00")
        self._lc = kwargs.get("lc", "00")
        self._data = kwargs.get("data", "0000")

    def __str__(self):
        return self.to_hex_string()

    @property
    def cla(self):
        """ CLA part of message """
        return self._cla

    @cla.setter
    def cla(self, cla):
        """ Sets CLS parameter """
        self._cla = cla

    @property
    def ins(self):
        """ INS part of message """
        return self._ins

    @ins.setter
    def ins(self, ins):
        """ Sets INS parameter """
        self._ins = ins

    @property
    def p1(self):
        """ P1 part of message """
        return self._p1

    @p1.setter
    def p1(self, p1):
        """ Sets P1 parameter """
        self._p1 = p1

    @property
    def p2(self):
        """ P2 describes verification type to be done """
        return self._p2

    @p2.setter
    def p2(self, p2):
        """ Sets P2 parameter """
        self._p2 = p2

    @property
    def lc(self):
        """ Length of subsequent data field"""
        return self._lc

    @lc.setter
    def lc(self, lc):
        """ Sets length of data field """
        self._lc = lc

    @property
    def data(self):
        """ Verification data """
        return self._data

    @data.setter
    def data(self, data):
        """ Sets verification data """
        self._data = data

    def to_hex_string(self):
        """ Returns hex string representation of message"""
        return "{}{}{}{}{}{}".format(self.cla, self.ins, self.p1, self.p2, self.lc, self.data)
