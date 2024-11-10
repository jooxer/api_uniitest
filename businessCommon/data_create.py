import requests
import time
from common.yamlRead import YamlRead

envConfig = YamlRead().env_config()
dataConfig = YamlRead().data_config()
host = envConfig['host']
notebody_url = host + dataConfig['createNoteInfo']['path']
note_url = host + dataConfig['createNoteContent']['path']
group_url = host + dataConfig['createGroup']['path']
del_notes_url = host + dataConfig['deleteNote']['path']


def create_group(user_id, sid):
    """"""
    group_id = str(int(time.time() * 1000)) + '_group_id'
    group_name = str(int(time.time() * 1000)) + '_group_name'
    headers = {
        'Cookie': f'wps_sid={sid}',
        'X-user-key': f'{user_id}'
    }
    body = {
        "groupName": group_name,
        "groupId": group_id
    }
    requests.post(url = group_url, headers = headers, json = body)
    return group_id


def create_notes(user_id, sid, num, re_time=None, group_id=None):
    """
    新建便签数据
    :param group_id:
    :param re_time: str
    :param user_id: str
    :param sid: str
    :param num: 新建便签数量
    :return: lst
    """

    # 处理当前获取的时间转化为就近整点的时间戳
    # 获取当前时间的小时数和分钟数
    current_hour, current_minute = time.localtime(re_time)[3], time.localtime(re_time)[4]
    # 如果分钟数大于等于 0 小于 30，向下取整到当前小时；如果分钟数大于等于 30，向上取整到下一个小时
    if current_minute < 30:
        target_hour = current_hour
    else:
        target_hour = current_hour + 1 if current_hour < 23 else 0
    # 计算目标时间戳（整小时）
    target_timestamp = time.mktime((time.localtime(re_time)[0], time.localtime(re_time)[1],
                                    time.localtime(re_time)[2], target_hour, 0, 0,
                                    time.localtime(re_time)[6], time.localtime(re_time)[7],
                                    time.localtime(re_time)[8]))

    lst = []
    t_lst = []
    s_lst = []
    for i in range(num):
        noteid = str(int(time.time() * 1000)) + '_noteid'
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-user-key': f'{user_id}'
        }

        # 上传便签主体
        if re_time:  # 上传日历便签主体
            body = {"noteId": noteid,
                    "remindTime": int(target_timestamp * 1000),
                    "remindType": 0,
                    "star": 0}
        elif group_id:
            body = {"noteId": noteid,
                    "groupId": group_id}

        else:  # 上传首页便签主体
            body = {"noteId": noteid}
        res = requests.post(url = notebody_url, headers = headers, json = body)
        # 上传便签内容
        body = {
            "title": str(int(time.time())) + '_title',
            "summary": str(int(time.time())) + '_summary',
            "body": str(int(time.time())) + '_body',
            "localContentVersion": 1,
            "noteId": noteid,
            "bodyType": 0
        }
        requests.post(url = note_url, headers = headers, json = body)
        lst.append(noteid)
        t_lst.append(body['title'])
        s_lst.append(body['summary'])
    return lst, t_lst, s_lst


def create_recycle_note(user_id, sid, note_id):
    """
    基于用户删除便签
    :param userId: str
    :param sid: str
    :return: None
    """
    del_headers = {
        'Cookie': f'wps_sid={sid}',
        'X-user-key': f'{user_id}'
    }
    requests.post(url = del_notes_url, headers = del_headers, json = {'noteId': note_id})


if __name__ == '__main__':
    # group = create_group('459349776', 'V02SS3bAi_Tyd2Jka6BPbfRLnDcM4bw00aa04f6d001b611f10')
    note_id, title  = create_notes('459349776', 'V02SS3bAi_Tyd2Jka6BPbfRLnDcM4bw00aa04f6d001b611f10', 1)[0], create_notes('459349776', 'V02SS3bAi_Tyd2Jka6BPbfRLnDcM4bw00aa04f6d001b611f10', 1)[1]
    tup = create_notes('459349776', 'V02SS3bAi_Tyd2Jka6BPbfRLnDcM4bw00aa04f6d001b611f10', 1)
    note_id1 = tup[0]
    title1 = tup[1]
    print(note_id)
    print(title)
    print(note_id1)
    print(title1)
    # print(create_notes('459349776', 'V02SS3bAi_Tyd2Jka6BPbfRLnDcM4bw00aa04f6d001b611f10', 1))
    # print(t_lst)