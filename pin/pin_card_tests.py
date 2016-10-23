import sys
import unittest

from unittest import TextTestRunner

from data.card import Card
from data.message import Message


class PinCardTests(unittest.TestCase):
    """
    Contains test cases for testing of PIN code command message

    For development purpose Card object has 'expected' attribute, which is always returned from card.send() method

    Few things where not clear enough in specification
    1. 'LC Field' in Command Message: it is not clear if LC value is length of data field in bytes or in characters.
     It was assumed it is number or characters. It is also not documented what is the desired behaviour in case when
     'LC Field' value does not correspond to 'Data Field'
    2. It is not clearly stated what kind of data 'Data Field' stores and in what format. It was assumed it is PIN
      stored as is.
    3. It is not clear what length has 'Data Field` in response message. Since it's always empty it was assumed it's 0
    4. It is not clear what Command Message should be send in order to receive number of further allowed retires.
     It was assumed that sending message with P2=00 will return number of further allowed tries 63CX for cards with
     verification enabled, and returns 9000 for cards where verification is not required.
    """

    def test_negatives_fuzzy_messages(self):
        """
        Negative path testing / Fuzzy Testing.

        Tests sending random hex string as the message.
        Tests sending special characters as the message.
        Tests sending empty message.

        Expected result: Documentation does not specify how card should react.
        It was assumed that 'Incorrect P1' should be returned
        """
        # expected result for series of checks
        expected_result = '6A86'
        pin = '1111'

        # card instance created with PIN and card reply as expected result
        card = Card(pin, expected_result)

        # prepare test messages
        messages = {
            1: Message(p1='BC', p2='3F', lc='A0', data='FF00'),
            2: Message(p1='%%', p2='()', lc='^^', data='{}'),
            3: Message(p1='', p2='', lc='', data=''),
        }

        for msg_id, msg in messages.items():
            response = card.send(msg.to_hex_string())
            self.assertEqual(response, expected_result, "Testing {} message {}".format(msg_id, msg))

    def test_incorrect_p1_p2(self):
        """
        Incorrect P1 and P2 testing.

        Tests sending message with incorrect P1.
        Tests sending message with incorrect P1

        Expected result: response message contains 6A86
        """
        # expected result for series of checks
        expected_result = '6A86'
        pin = '1111'

        # card instance created with PIN and card reply as expected result
        card = Card(pin, expected_result)

        # prepare test messages
        messages = {
            1: Message(p1='01', p2='00', lc='00', data='0000'),
            2: Message(p1='AA', p2='00', lc='00', data='0000'),
            3: Message(p1='G1', p2='00', lc='00', data='0000'),
            4: Message(p1='%%', p2='00', lc='00', data='0000'),
            5: Message(p1='00', p2='03', lc='00', data='0000'),
            6: Message(p1='00', p2='AA', lc='00', data='0000'),
            7: Message(p1='00', p2='G1', lc='00', data='0000'),
            8: Message(p1='00', p2='%%', lc='00', data='0000'),
        }

        for msg_id, msg in messages.items():
            response = card.send(msg.to_hex_string())
            self.assertEqual(response, expected_result, "Testing {} message {}".format(msg_id, msg))

    def test_incorrect_pin(self):
        """
        Incorrect PIN testing.

        Tests sending message with incorrect Global and Specific PIN. Three incorrect PIN tries per each PIN type
        until card sends 'blocked message'

        Expected result: response message contains 63C2, 63C1, 6983
        """
        # expected result for series of checks
        expected_result = ['63C2', '63C2', '6983']
        pin_global = '1234'
        pin_specific = '4321'

        # prepare global pin test messages
        messages = {
            1: Message(p1='00', p2='01', lc='4', data='1111'),
            2: Message(p1='00', p2='01', lc='4', data='1121'),
            3: Message(p1='00', p2='01', lc='4', data='1131'),
        }

        for msg_id, msg in messages.items():
            # card instance created with PIN and card reply as expected result
            card = Card(pin_global, expected_result[msg_id - 1])
            response = card.send(msg.to_hex_string())
            self.assertEqual(response, expected_result[msg_id - 1], "Testing {} message {}".format(msg_id, msg))

        # prepare specific pin test messages
        messages = {
            1: Message(p1='00', p2='02', lc='4', data='4444'),
            2: Message(p1='00', p2='02', lc='4', data='3333'),
            3: Message(p1='00', p2='02', lc='4', data='2222'),
        }

        for msg_id, msg in messages.items():
            # card instance created with PIN and card reply as expected result
            card = Card(pin_specific, expected_result[msg_id - 1])
            response = card.send(msg.to_hex_string())
            self.assertEqual(response, expected_result[msg_id - 1], "Testing {} message {}".format(msg_id, msg))

    def test_correct_pin(self):
        """
        Correct PIN testing.

        Tests sending message with correct Global and Specific PINs.

        Expected result: response message contains 9000
        """
        # expected result for series of checks
        expected_result = '9000'
        pin = '1234'

        # card instance created with PIN and card reply as expected result
        card = Card(pin, expected_result)

        # prepare test messages
        messages = {
            1: Message(p1='00', p2='01', lc='04', data='1234'),
            2: Message(p1='00', p2='02', lc='04', data='1234'),
        }

        for msg_id, msg in messages.items():
            response = card.send(msg.to_hex_string())
            self.assertEqual(response, expected_result, "Testing {} message {}".format(msg_id, msg))

    def test_verification_not_required(self):
        """
        Card verification mechanism testing - card with verification disabled.

        Tests sending message to request information if verification is required.

        Expected result: response message contains 9000
        """
        # expected result for series of checks
        expected_result = '9000'
        no_pin = ''

        # card instance created without PIN and card reply as expected result
        card = Card(no_pin, expected_result)

        # prepare test messages
        messages = {
            1: Message(p1='00', p2='00', lc='00', data=''),
        }

        for msg_id, msg in messages.items():
            response = card.send(msg.to_hex_string())
            self.assertEqual(response, expected_result, "Testing {} message {}".format(msg_id, msg))

    def test_verification_required(self):
        """
        Card verification mechanism testing - card with verification enabled.

        Tests sending message to request information about further allowed retries.
        First sending request about allowed retires, then sending authorization request with incorrect PIN

        Expected result: response message contains number of allowed retries 63CX
        """
        # expected result for series of checks
        expected_result = ['63C3', '63C2', '63C2']
        pin = '9876'

        # prepare test messages
        messages = {
            1: Message(p1='00', p2='01', lc='00', data=''),
            2: Message(p1='00', p2='01', lc='04', data='9999'),
            3: Message(p1='00', p2='01', lc='00', data='')
        }

        for msg_id, msg in messages.items():
            # card instance created without PIN and card reply as expected result
            card = Card(pin, expected_result)
            response = card.send(msg.to_hex_string())
            self.assertEqual(response, expected_result, "Testing {} message {}".format(msg_id, msg))

    def test_no_information(self):
        """
        Incorrect lc and data fields in message testing.

        Tests sending message with incorrect length of data field, meaning LC Field does not correspond data field.
        Messages for Global and Specific PINs

        Expected result: response message contains 6300
        """
        # expected result for series of checks
        expected_result = '6300'
        pin = '1234'

        # card instance created with PIN and card reply as expected result
        card = Card(pin, expected_result)

        # prepare test messages
        messages = {
            1: Message(p1='00', p2='01', lc='04', data=''),
            2: Message(p1='00', p2='01', lc='05', data='1234'),
            3: Message(p1='00', p2='01', lc='03', data='1234'),
            4: Message(p1='00', p2='01', lc='', data=''),
            5: Message(p1='00', p2='02', lc='04', data=''),
            6: Message(p1='00', p2='02', lc='05', data='1234'),
            7: Message(p1='00', p2='02', lc='03', data='1234'),
            4: Message(p1='00', p2='02', lc='', data=''),
        }

        for msg_id, msg in messages.items():
            response = card.send(msg.to_hex_string())
            self.assertEqual(response, expected_result, "Testing {} message {}".format(msg_id, msg))


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(PinCardTests)
    test_result = TextTestRunner().run(test_suite)
    # exit with return code equal to number of failures
    sys.exit(len(test_result.failures))
