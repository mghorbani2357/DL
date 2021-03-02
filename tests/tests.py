from unittest import TestCase


class TestDownload(TestCase):
    def setUp(self):
        with open('file', 'wb') as file:
            file.write('')
