import unittest
from businessCommon.data_clear import clear_groups
from businessCommon.data_create import create_notes
from common.caseLogs import info, error, step, class_case_log
from businessCommon.httpReMethod import BusinessRequests
from common.yamlRead import YamlRead



@class_case_log
class GetHomeNotesInput(unittest.TestCase):
    # 环境变量
    envConfig = YamlRead().env_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    br = BusinessRequests()
    host = envConfig['host']

    def setUp(self) -> None:  # 初始化构建数据、前置清理脏数据
        clear_groups(self.userId1, self.sid1)

    def testCase01_must_key_userId_None(self):
        """查询首页便签, 必填项user_id为空"""
        step('【step】前置构建首页便签数据')
        create_notes(self.userId1, self.sid1, 1)
        self.userId1 = None
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项校验失败')

    def testCase02_must_key_userId_str(self):
        """查询首页便签, 必填项user_id为字符串"""
        step('【step】前置构建首页便签数据')
        create_notes(self.userId1, self.sid1, 1)
        path = f'/v3/notesvr/user/str({self.userId1})/home/startindex/0/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项校验失败')

    def testCase03_must_key_userId_long(self):
        """查询首页便签, 必填项user_id长度过长"""
        step('【step】前置构建首页便签数据')
        create_notes(self.userId1, self.sid1, 1)
        self.userId1 = 999999999999999999
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(412, res.status_code, msg = '必填项校验失败')

    def testCase04_must_key_startindex_None(self):
        """查询首页便签, 必填项startindex为空"""
        step('【step】前置构建首页便签数据')
        create_notes(self.userId1, self.sid1, 1)
        start_index = None
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/{start_index}/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项校验失败')

    def testCase05_must_key_startindex_str(self):
        """查询首页便签, 必填项startindex为字符串"""
        step('【step】前置构建首页便签数据')
        create_notes(self.userId1, self.sid1, 1)
        start_index = 0
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/str({start_index})/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项校验失败')

    def testCase06_must_key_startindex_long(self):
        """查询首页便签, 必填项startindex长度过长"""
        step('【step】前置构建首页便签数据')
        create_notes(self.userId1, self.sid1, 1)
        start_index = 99999999999999
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/{start_index}/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项校验失败')

    def testCase07_must_key_rows_None(self):
        """查询首页便签, 必填项rows为空"""
        step('【step】前置构建首页便签数据')
        create_notes(self.userId1, self.sid1, 1)
        rows = None
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/{rows}/notes'
        url = self.host + path
        step('【step】获取首页便签')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项校验失败')

    def testCase08_must_key_rows_str(self):
        """查询首页便签, 必填项rows为字符串"""
        step('【step】前置构建首页便签数据')
        create_notes(self.userId1, self.sid1, 1)
        rows = 0
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/str({rows})/notes'
        url = self.host + path
        step('【step】获取首页便签')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项校验失败')

    def testCase09_must_key_rows_long(self):
        """查询首页便签, 必填项rows长度过长"""
        step('【step】前置构建首页便签数据')
        create_notes(self.userId1, self.sid1, 1)
        rows = 999999999999999999
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/{rows}/notes'
        url = self.host + path
        step('【step】获取首页便签')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项校验失败')