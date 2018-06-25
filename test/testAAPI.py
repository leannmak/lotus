#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author: Leann Mak
# Email: leannmak@139.com
# (c) 2018
#
# This is the autotest cases for ansible api.
#
import unittest
from mock import patch, Mock
from ansible.executor.stats import AggregateStats
from ansible.executor.task_queue_manager import TaskQueueManager

from lotus.api import Ansible2API


class TestAAPI(unittest.TestCase):
    '''
        Unit test for Ansible API
    '''
    def setUp(self):
        ''' create ansible api object and mock attr '''
        self._hosts = ['127.0.0.1', '10.0.0.1']
        self._args = 'cat helloworld.txt'
        self._state = 0
        self._stat = {
            'unreachable': 0,
            'skipped': 0,
            'ok': 1,
            'changed': 1,
            'failures': 0
        }
        self._hostvars = {
            self._hosts[0]: {
                'out': {
                    u'changed': True,
                    u'end': u'2018-01-01 10:57:08.144560',
                    u'stdout': u'Hello World!',
                    u'cmd': self._args,
                    u'rc': 0,
                    u'start': u'2018-01-01 10:57:08.137068',
                    u'stderr': u'',
                    u'delta': u'0:00:00.007492',
                    'stdout_lines': [u'Hello World!'],
                    u'warnings': []
                }
            },
            self._hosts[1]: {
                'out': {
                    u'changed': True,
                    u'end': u'2018-01-01 10:57:08.144560',
                    u'stdout': u'Hello Leann!',
                    u'cmd': self._args,
                    u'rc': 0,
                    u'start': u'2018-01-01 10:57:08.137068',
                    u'stderr': u'',
                    u'delta': u'0:00:00.007492',
                    'stdout_lines': [u'Hello Leann!'],
                    u'warnings': []
                }
            }
        }
        TaskQueueManager.hostvars = self._hostvars
        self.aapi = Ansible2API(hosts=self._hosts)

    def tearDown(self):
        ''' clear auth state and del tmp mock attr '''
        self.aapi = None
        self.assertTrue(hasattr(TaskQueueManager, 'hostvars'))
        del TaskQueueManager.hostvars
        with self.assertRaises(AttributeError):
            TaskQueueManager.hostvars

    def test_ansible_run(self):
        ''' [API      ] ansible api test '''
        with patch.object(
                AggregateStats, 'summarize', Mock(return_value=self._stat)):
            with patch.object(
                    TaskQueueManager, 'run', Mock(return_value=self._state)):
                state, stats_sum, results = self.aapi.run(
                    module='shell', args=self._args)
                self.assertEqual(state, self._state)
                self.assertEqual(stats_sum[self._hosts[0]], self._stat)
                self.assertEqual(
                    results[self._hosts[1]],
                    self._hostvars[self._hosts[1]]['out'])
