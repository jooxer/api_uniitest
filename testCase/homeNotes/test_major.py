import unittest
from businessCommon.data_clear import clear_notes
from businessCommon.data_create import create_notes
from common.checkOutput import CheckPro
from businessCommon.httpReMethod import BusinessRequests
from common.caseLogs import info, step, error, class_case_log


@class_case_log
class GetHomeNotesMajor(unittest.TestCase):
    userId1 = '459349776'
    sid1 = 'V02SS3bAi_Tyd2Jka6BPbfRLnDcM4bw00aa04f6d001b611f10'
    br = BusinessRequests()

    def setUp(self) -> None:
        clear_notes(self.userId1, self.sid1)

    def testCase01_major(self):
        """获取首页便签列表 主流程"""
        step('【step】前置构建首页便签数据')
        tup = create_notes(self.userId1, self.sid1, 1)
        note_id = tup[0][0]
        title = tup[1][0]
        summary = tup[2][0]
        host = 'https://note-api.wps.cn'
        path = f'/v3/notesvr/user/{self.userId1}/home/startindex/0/rows/50/notes'
        url = host + path
        step('【step】获取首页便签')
        res = self.br.get(url, user_id = self.userId1, sid = self.sid1)
        response = res.json()
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')
        expected = {
            'responseTime': int,
            'webNotes': [{
                "noteId": note_id,
                "createTime": int,
                "star": int,
                "remindTime": 0,
                "remindType": 0,
                "infoVersion": 1,
                "infoUpdateTime": int,
                "groupId": None,
                "title": title,
                "summary": summary,
                "thumbnail": None,
                "contentVersion": 1,
                "contentUpdateTime": int
            }]
        }
        CheckPro().check_output(expected = expected, actual = response)


