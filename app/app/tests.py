from django.test import SimpleTestCase

class CalcTests(SimpleTestCase):
    """Test calculations."""

    def test_addition(self):
        """Test that 5 + 6 equals 11."""
        res = 5 + 6
        self.assertEqual(res, 11)
