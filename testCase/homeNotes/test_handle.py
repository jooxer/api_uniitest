import unittest
import time
from businessCommon.data_clear import clear_groups, clear_recycle_notes, clear_notes
from businessCommon.data_create import create_notes, create_group, create_recycle_note
from common.caseLogs import info, error, step, class_case_log
from businessCommon.httpReMethod import BusinessRequests
from common.yamlRead import YamlRead


@class_case_log
class GetHomeNotesHandle(unittest.TestCase):
    # 环境变量
    envConfig = YamlRead().env_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    userId2 = envConfig['userId2']
    sid2 = envConfig['sid2']
    br = BusinessRequests()
    host = envConfig['host']

    def setUp(self) -> None:  # 初始化构建数据、前置清理脏数据
        clear_notes(self.userId1, self.sid1)
        clear_notes(self.userId2, self.sid2)

    def testCase01_check_calendarNotes(self):
        """查询日历便签是否在首页"""
        step('【step】前置构建日历便签数据')
        re_time = int(time.time())
        cal_notes = create_notes(self.userId1, self.sid1, 1, re_time = re_time)[0]
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签列表')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        response = res.json()
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')
        self.assertEqual([], response['webNotes'], msg = f'{cal_notes[0]}日历便签存在首页中')

    def testCase02_check_groupNotes(self):
        """查询分组便签是否在首页"""
        step('【step】前置构建分组便签数据')
        group_id = create_group(self.userId1, self.sid1)
        group_notes = create_notes(self.userId1, self.sid1, 1, group_id = group_id)[0]
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签列表')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        response = res.json()
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')
        self.assertEqual([], response['webNotes'], msg = f'{group_notes[0]}分组便签存在首页中')

    def testCase03_check_recycleNotes(self):
        """查询回收站便签是否在首页"""
        step('【step】前置构建回收站便签数据')
        recycle_note = create_notes(self.userId1, self.sid1, 1)[0]
        create_recycle_note(self.userId1, self.sid1, recycle_note)
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签列表')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        response = res.json()
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')
        self.assertEqual([], response['webNotes'], msg = f'{recycle_note}回收站便签存在首页中')

    def testCase04_check_delNotes(self):
        """查询彻底删除便签是否在首页"""
        step('【step】前置彻底删除便签数据')
        del_note = create_notes(self.userId1, self.sid1, 1)[0]
        create_recycle_note(self.userId1, self.sid1, del_note[0])
        clear_recycle_notes(self.userId1, self.sid1, del_note)
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签列表')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        response = res.json()
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')
        self.assertEqual([], response['webNotes'], msg = f'{del_note}删除便签存在首页中')

    def testCase05_limit_rows(self):
        """获取首页便签，限制获取条数"""
        step('【step】前置便签数据2条')
        create_notes(self.userId1, self.sid1, 2)
        rows = 1
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/{rows}/notes'
        url = self.host + path
        step('【step】获取首页便签列表')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        response = res.json()
        self.assertEqual(1, len(response['webNotes']), msg = '限制条数校验失败')

    def testCase06_limit_startindex(self):
        """获取首页便签，限制获取索引"""
        step('【step】前置构建便签数据2条')
        create_notes(self.userId1, self.sid1, 2)
        startindex = 1
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/{startindex}/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签列表')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        response = res.json()
        self.assertEqual(1, len(response['webNotes']), msg = '限制索引校验失败')

    def testCase07_check_notes_num(self):
        """获取首页便签，校验0条便签"""
        step('【step】不构建便签数据')
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签列表')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        response = res.json()
        self.assertEqual(0, len(response['webNotes']), msg = '校验0条便签失败')

    def testCase08_check_notes_num(self):
        """获取首页便签，校验2条便签"""
        step('【step】前置构建便签数据2条')
        create_notes(self.userId1, self.sid1, 2)
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签列表')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        response = res.json()
        self.assertEqual(2, len(response['webNotes']), msg = '校验1条便签失败')

    def testCase09_check_ultra_vires(self):
        """获取其他用户首页便签，校验越权"""
        step('【step】前置构建便签数据1条')
        create_notes(self.userId2, self.sid2, 1)
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/50/notes'
        url = self.host + path
        step('【step】获取首页便签列表')
        res = self.br.get(url, user_id = self.userId2, sid = self.sid2)
        self.assertEqual(412, res.status_code, msg = '存在越权')
