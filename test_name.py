import unittest
from scanner_handler import CheckQr


class ChildCheckQr(CheckQr):
    is_can_add_device = False

    def check_in_db(self, qr):
        return True

    @staticmethod
    def can_add_device(message: str):
        ChildCheckQr.is_can_add_device = True
        return message

    @staticmethod
    def send_error(error: str):
        ChildCheckQr.is_can_add_device = False
        return error


class ChildCheckQrNeg(ChildCheckQr):
    def check_in_db(self, qr):
        return None


class TestQr(unittest.TestCase):
    def setUp(self):
        self.checkQr1 = ChildCheckQr()
        self.checkQr2 = ChildCheckQr()
        self.checkQrNeg = ChildCheckQrNeg()
        self.available_colors = ['Red', 'Green', 'Fuzzy Wuzzy']

    def test_check_color_pos(self):
        self.assertEqual(self.checkQr1.check_len_color('111'), 'Red')
        self.assertEqual(self.checkQr1.check_len_color('red'), 'Red')
        self.assertEqual(self.checkQr1.check_len_color('green'), 'Green')
        self.assertEqual(self.checkQr1.check_len_color('11111'), 'Green')
        self.assertEqual(self.checkQr1.check_len_color('1111111'), 'Fuzzy Wuzzy')
        self.assertEqual(self.checkQr1.check_len_color('somestr'), 'Fuzzy Wuzzy')

    def test_check_color_neg(self):
        self.assertEqual(self.checkQr1.check_len_color('1'), 'Red')
        self.assertEqual(self.checkQr1.check_len_color('21'), 'Green')

    def test_check_in_db_pos(self):
        self.assertTrue(self.checkQr1.check_in_db("red"))
        self.assertTrue(self.checkQr1.check_in_db("green"))
        self.assertTrue(self.checkQr1.check_in_db("1111111"))
        self.assertTrue(self.checkQr1.check_in_db("no"))

    def test_check_in_db_neg(self):
        self.assertTrue(self.checkQrNeg.check_in_db("red"))

    def test_check_scanned_device_pos(self):
        self.checkQr1.check_scanned_device('red')
        self.assertIn(self.checkQr1.color, self.available_colors)

        self.checkQr1.check_scanned_device('green')
        self.assertIn(self.checkQr1.color, self.available_colors)

        self.checkQr1.check_scanned_device('1234567')
        self.assertIn(self.checkQr1.color, self.available_colors)

    def test_check_scanned_device_neg(self):
        self.checkQr1.check_scanned_device('re')
        self.assertIn(self.checkQr1.color, self.available_colors)

        self.checkQr1.check_scanned_device('gree')
        self.assertIn(self.checkQr1.color, self.available_colors)

        self.checkQrNeg.check_scanned_device('red')
        self.assertIn(self.checkQrNeg.color, self.available_colors)

    def test_can_add_device_pos(self):
        self.checkQr1.check_scanned_device('red')
        self.assertTrue(self.checkQr1.is_can_add_device)

        self.checkQr1.check_scanned_device('green')
        self.assertTrue(self.checkQr1.is_can_add_device)

        self.checkQr1.check_scanned_device('1234567')
        self.assertTrue(self.checkQr1.is_can_add_device)

    def test_can_add_device_neg(self):
        self.checkQr1.check_scanned_device('re')
        self.assertTrue(self.checkQr1.is_can_add_device)

        self.checkQrNeg.check_scanned_device('red')
        self.assertTrue(self.checkQrNeg.is_can_add_device)

    def test_send_error_pos(self):
        self.checkQr1.check_scanned_device('re')
        self.assertFalse(self.checkQr1.is_can_add_device)

        self.checkQrNeg.check_scanned_device('red')
        self.assertFalse(self.checkQrNeg.is_can_add_device)

    def test_send_error_neg(self):
        self.checkQr1.check_scanned_device('red')
        self.assertFalse(self.checkQr1.is_can_add_device)

        self.checkQr1.check_scanned_device('green')
        self.assertFalse(self.checkQr1.is_can_add_device)

        self.checkQr1.check_scanned_device('1234567')
        self.assertFalse(self.checkQr1.is_can_add_device)


if __name__ == "__main__":
    unittest.main()
