#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author: Leann Mak
# Email: leannmak@139.com
# (c) 2018
#
# This is the autotest cases for etcd api.
#
import unittest
from mock import patch, Mock

from lotus.api import EtcdAPIException, EtcdAPI, Client


class TestEAPI(unittest.TestCase):
    '''
        Unit test for Etcd API
    '''
    class MockClient(object):
        ''' class for mock'''
        def __getattr__(self, method):
            return lambda *args, **kwargs: kwargs

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch.multiple(
        Client,
        __new__=Mock(return_value=MockClient()))
    def test_etcd_api(self):
        ''' [API      ] etcd api test '''
        eapi = EtcdAPI(host='', port=0, cert='', ca_cert='')
        # connect
        eapi.connect()
        self.assertTrue(eapi._EtcdAPI__connected)
        # normal
        params = dict(key='key-test', value='value-test')
        self.assertEqual(eapi.write(**params), params)
        self.assertEqual(eapi.write(), eapi._EtcdAPI__client.write())
        # no api
        with self.assertRaises(EtcdAPIException) as cm:
            eapi.remove()
        self.assertIn('No Such Etcd API', cm.exception.message)
        # disconnect
        eapi._EtcdAPI__connected = False
        with self.assertRaises(EtcdAPIException) as cm:
            eapi.write(**params)
        self.assertIn('Etcd NOT Connected', cm.exception.message)
        eapi = None
