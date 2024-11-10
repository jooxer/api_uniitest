import unittest
from businessCommon.data_clear import clear_notes
from businessCommon.data_create import create_notes, create_group, create_recycle_note
from businessCommon.httpReMethod import BusinessRequests
from common.caseLogs import info, step, error, class_case_log
from common.yamlRead import YamlRead
import time


@class_case_log
class DelNotesHandle(unittest.TestCase):
    # 环境变量
    envConfig = YamlRead().env_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    userId2 = envConfig['userId2']
    sid2 = envConfig['sid2']
    br = BusinessRequests()
    host = envConfig['host']

    # 接口数据变量
    dataConfig = YamlRead().data_config()
    del_path = dataConfig['deleteNote']['path']
    del_url = host + del_path

    def setUp(self) -> None:
        clear_notes(self.userId1, self.sid1)
        clear_notes(self.userId2, self.sid2)

    def testCase01_del_homeNotes(self):
        """删除便签 删除首页便签"""
        step('【step】前置构建首页便签数据')
        note_id = create_notes(self.userId1, self.sid1, 1)[0]
        step('【step】删除便签')
        body = {"noteId": note_id[0]}
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        step('【step】校验便签删除情况')
        recycle_url = self.host + f'/v3/notesvr/user/{self.userId1}/invalid/startindex/0/rows/50/notes'
        recycle_res = self.br.get(recycle_url, user_id = self.userId1, sid = self.sid1)
        response = recycle_res.json()
        lst = []
        for i in response['webNotes']:
            lst.append(i['noteId'])
        self.assertIn(note_id[0], lst, msg = f'{note_id[0]}首页便签删除失败')
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')

    def testCase02_del_calendarNotes(self):
        """删除便签 删除日历便签"""
        step('【step】前置构建日历便签数据')
        re_time = int(time.time())
        note_id = create_notes(self.userId1, self.sid1, 1, re_time = re_time)[0]
        step('【step】删除便签')
        body = {"noteId": note_id[0]}
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        step('【step】校验便签删除情况')
        recycle_url = self.host + f'/v3/notesvr/user/{self.userId1}/invalid/startindex/0/rows/50/notes'
        recycle_res = self.br.get(recycle_url, user_id = self.userId1, sid = self.sid1)
        response = recycle_res.json()
        lst = []
        for i in response['webNotes']:
            lst.append(i['noteId'])
        self.assertIn(note_id[0], lst, msg = f'{note_id[0]}日历便签便签删除失败')
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')

    def testCase03_del_groupNotes(self):
        """删除便签 删除分组便签"""
        step('【step】前置构建分组便签数据')
        group_id = create_group(self.userId1, self.sid1)[0]
        note_id = create_notes(self.userId1, self.sid1, 1, group_id = group_id)
        step('【step】删除便签')
        body = {"noteId": note_id[0]}
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        step('【step】校验便签删除情况')
        recycle_url = self.host + f'/v3/notesvr/user/{self.userId1}/invalid/startindex/0/rows/50/notes'
        recycle_res = self.br.get(recycle_url, user_id = self.userId1, sid = self.sid1)
        response = recycle_res.json()
        lst = []
        for i in response['webNotes']:
            lst.append(i['noteId'])
        self.assertIn(note_id[0], lst, msg = f'{note_id[0]}分组便签便签删除失败')
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')

    def testCase04_del_recycleNotes(self):
        """删除便签 删除回收站便签"""
        step('【step】前置构建回收站便签数据')
        note_id = create_notes(self.userId1, self.sid1, 1)[0][0]
        create_recycle_note(self.userId1, self.sid1, note_id)
        step('【step】删除便签')
        body = {"noteId": note_id}
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        step('【step】校验便签删除情况')
        recycle_url = self.host + f'/v3/notesvr/user/{self.userId1}/invalid/startindex/0/rows/50/notes'
        recycle_res = self.br.get(recycle_url, user_id = self.userId1, sid = self.sid1)
        response = recycle_res.json()
        lst = []
        for i in response['webNotes']:
            lst.append(i['noteId'])
        self.assertIn(note_id, lst, msg = f'{note_id}回收站便签便签删除失败')
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')

    def testCase05_del_repeat(self):
        """删除便签 重复删除便签"""
        step('【step】前置构建首页便签数据')
        note_id = create_notes(self.userId1, self.sid1, 1)[0]
        step('【step】删除便签')
        body = {"noteId": note_id[0]}
        self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        step('【step】再次删除便签')
        body = {"noteId": note_id[0]}
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')

    def testCase09_check_ultra_vires(self):
        """删除其他用户便签，校验越权"""
        step('【step】前置构建便签数据1条')
        note_id = create_notes(self.userId2, self.sid2, 1)[0]
        step('【step】删除便签')
        body = {"noteId": note_id[0]}
        self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        step('【step】校验越权')
        get_notes_url = self.host + f'/v3/notesvr/user/{self.userId2}/home/startindex/0/rows/50/notes'
        res = self.br.get(get_notes_url, user_id = self.userId2, sid = self.sid2)
        self.assertEqual(note_id[0], res.json()['webNotes'][0]['noteId'], msg = '存在越权')