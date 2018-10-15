from pyfakefs import fake_filesystem_unittest


class TestDjangoDeployment(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
