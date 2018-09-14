import unittest
from app.models import User


class UserModelCase(unittest.TestCase):

    def test_password_hashing(self):
        user = User('cat', 'test', 'test', 'test@test.com')
        self.assertFalse(user.check_password('dog'))
        self.assertTrue(user.check_password('cat'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
