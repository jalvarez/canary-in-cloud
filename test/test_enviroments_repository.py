import unittest
from dynamodb_test import DynamoDbTestCase
import src

class EnviromentsRepositoryTests(DynamoDbTestCase):
    def setUp(self):
        super(EnviromentsRepositoryTests, self).setUp()
        enviroments_table = self.dynamodb.Table('function_enviroment')
        self.repository = src.EnviromentsRepository(enviroments_table)

    def test_get_enviroment_by_function(self):
        enviroment = self.repository.get_enviroment_by_function( \
                                                      'CanaryInCloudScan_TEST')
        self.assertIsNotNone(enviroment)
        self.assertEqual(enviroment, 'TEST')
