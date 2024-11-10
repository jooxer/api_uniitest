import unittest
from businessCommon.data_clear import clear_notes
from businessCommon.data_create import create_notes
from businessCommon.httpReMethod import BusinessRequests
from common.caseLogs import info, step, error, class_case_log
from common.yamlRead import YamlRead


@class_case_log
class DelNotesInput(unittest.TestCase):
    # 环境变量
    envConfig = YamlRead().env_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    br = BusinessRequests()
    host = envConfig['host']

    # 接口数据变量
    dataConfig = YamlRead().data_config()
    del_path = dataConfig['deleteNote']['path']
    del_url = host + del_path

    def setUp(self) -> None:
        clear_notes(self.userId1, self.sid1)

    def testCase01_must_key_noteId_lost(self):
        """删除便签 必填项noteId缺失"""
        step('【step】前置构建便签数据')
        note_id = create_notes(self.userId1, self.sid1, 1)[0]
        step('【step】删除noteId缺失的便签')
        body = {"noteId": note_id[0]}
        body.pop("noteId")
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项noteId缺失校验失败')

    def testCase02_must_key_noteId_None(self):
        """删除便签 必填项noteId为空"""
        step('【step】前置构建便签数据')
        note_id = create_notes(self.userId1, self.sid1, 1)[0]
        step('【step】删除noteId为空的便签')
        body = {"noteId": None}
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项noteId为空校验失败')

    def testCase03_must_key_noteId_long(self):
        """删除便签 必填项noteId值过长"""
        step('【step】前置构建便签数据')
        note_id = create_notes(self.userId1, self.sid1, 1)
        step('【step】删除noteId为空的便签')
        body = {"noteId": "99999999999999999999999999999999999999999999999999"}
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项noteId值过长校验失败')

    def testCase04_must_key_noteId_special(self):
        """删除便签 必填项noteId为特殊字符"""
        step('【step】前置构建便签数据')
        note_id = create_notes(self.userId1, self.sid1, 1)
        step('【step】删除noteId为空的便签')
        body = {"noteId": "？@#￥%……"}
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(500, res.status_code, msg = '必填项noteId特殊字符校验失败')

    def testCase05_must_key_noteId_upper_lower(self):
        """删除便签 必填项noteId为大小写"""
        step('【step】前置构建便签数据')
        step('【step】删除noteId为空的便签')
        body = {"noteId": "AAAAAaaaa"}
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(200, res.status_code, msg = '必填项noteId大小写校验失败')