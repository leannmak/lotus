#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author: Leann Mak
# Email: leannmak@139.com
# (c) 2018
#
# This is the autotest cases for minio api.
#
import unittest
from mock import patch, Mock

from lotus.api import MinioAPIException, MinioAPI, Minio


class TestEAPI(unittest.TestCase):
    '''
        Unit test for Minio API in ADAPTER
    '''
    class MockMinio(object):
        ''' class for mock'''
        def __getattr__(self, method):
            return lambda *args, **kwargs: kwargs

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch.multiple(
        Minio,
        __new__=Mock(return_value=MockMinio()))
    def test_minio_api(self):
        ''' [API      ] minio api test '''
        mapi = MinioAPI(
            endpoint='127.0.0.1:9000', access_key='access-key-test',
            secret_key='secret-key-test')
        # connect
        mapi.connect()
        self.assertTrue(mapi._MinioAPI__connected)
        # normal
        params = dict(bucket_name='bucket-test', prefix='prefix-test/', recursive=True)
        self.assertEqual(mapi.list_objects(**params), params)
        self.assertEqual(mapi.list_objects(), mapi._MinioAPI__client.list_objects())
        # no api
        with self.assertRaises(MinioAPIException) as cm:
            mapi.remove()
        self.assertIn('No Such Minio API', cm.exception.message)
        # disconnect
        mapi.disconnect()
        with self.assertRaises(MinioAPIException) as cm:
            mapi.list_objects(**params)
        self.assertIn('Minio NOT Connected', cm.exception.message)
        mapi = None
