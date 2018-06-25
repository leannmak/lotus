#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author: Leann Mak
# Email: leannmak@139.com
# (c) 2018
#
# This is the autotest cases for disconf api
#
import unittest
from mock import patch, Mock

from lotus.api import DisconfAPIException, DisconfAPI


class TestDAPI(unittest.TestCase):
    '''
        Unit test for Disconf API
    '''
    def setUp(self):
        ''' create disconf api object and set auth state true '''
        self.dapi = DisconfAPI(url='', user='', password='')
        self.dapi._DisconfAPI__auth = 'i@mcookie'

    def tearDown(self):
        ''' clear auth state and remove disconf api object '''
        self.dapi._DisconfAPI__auth = None
        self.dapi = None

    def test_app_list_api(self):
        ''' [API      ] disconf api test '''
        result = None
        # normal
        value = {
            'message': {},
            'sessionId': 'i@theSession',
            'success': 'true',
            'page': {
                'orderBy': None,
                'pageNo': None,
                'pageSize': None,
                'totalCount': 1,
                'result': [
                    {'id': 0, 'name': 'hey-disconf'},
                    {'id': 7, 'name': 'bye-disconf'}
                ],
                'order': None,
                'footResult': None
            }
        }
        apps = Mock(return_value=value)
        with patch.object(DisconfAPI, 'url_request', apps):
            result = self.dapi.app_list.get()
            self.assertEqual(len(result), 4)
            self.assertEqual(result['success'], 'true')
        # no api
        with self.assertRaises(DisconfAPIException) as cm:
            self.dapi.app_lists
        self.assertIn('No such Disconf API', cm.exception.message)
        # no method
        with self.assertRaises(DisconfAPIException) as cm:
            self.dapi.app_list.post()
        self.assertIn('No such API Method', cm.exception.message)
        # no login
        self.dapi._DisconfAPI__auth = None
        with self.assertRaises(DisconfAPIException) as cm:
            self.dapi.app_list.get()
        self.assertIn('Disconf-Web NOT Logged In', cm.exception.message)
