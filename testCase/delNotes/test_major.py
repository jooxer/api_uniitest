import unittest
from businessCommon.data_clear import clear_notes
from businessCommon.data_create import create_notes
from common.checkOutput import CheckPro
from businessCommon.httpReMethod import BusinessRequests
from common.caseLogs import info, step, error, class_case_log
from common.yamlRead import YamlRead


@class_case_log
class DelNotesMajor(unittest.TestCase):
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
    get_notes_url = host + f'/v3/notesvr/user/{userId1}/home/startindex/0/rows/50/notes'

    def setUp(self) -> None:
        clear_notes(self.userId1, self.sid1)

    def testCase01_major(self):
        """删除便签 主流程"""
        step('【step】前置构建便签数据')
        note_id = create_notes(self.userId1, self.sid1, 1)[0]
        step('【step】删除便签')
        body = {"noteId": note_id[0]}
        res = self.br.post(self.del_url, json = body, user_id = self.userId1, sid = self.sid1)
        response = res.json()
        self.assertEqual(200, res.status_code, msg = '状态码校验失败')
        get_res = self.br.get(self.get_notes_url, user_id = self.userId1, sid = self.sid1)
        get_response = get_res.json()
        self.assertNotIn(note_id[0], get_response['webNotes'], msg = '便签删除失败')
        expected = {
            'responseTime': int
        }
        CheckPro().check_output(expected = expected, actual = response)


