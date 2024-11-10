import requests
from common.yamlRead import YamlRead

envConfig = YamlRead().env_config()
dataConfig = YamlRead().data_config()
host = envConfig['host']
get_group_url = host + '/v3/notesvr/get/notegroup'
del_group_url = host + '/notesvr/delete/notegroup'

del_notes_url = host + '/v3/notesvr/delete'
cleanrecyclebin_url = host + '/v3/notesvr/cleanrecyclebin'


def clear_groups(userId, sid):
    """
    基于用户进行分组清理
    :param userId: str
    :param sid: str
    :return: None
    """

    headers = {
        'Cookie': f'wps_sid={sid}',
        'X-user-key': f'{userId}'
    }

    # 查询当前用户分组信息
    body = {
        "excludeInValid": False
    }
    res = requests.post(url = get_group_url, headers = headers, json = body)
    d_group = []
    for group in res.json()['noteGroups']:
        if group['valid'] == 1:
            d_group.append(group['groupId'])

    for group_id in d_group:
        requests.post(url = del_group_url, headers = headers, json = {'groupId': group_id})


def clear_notes(userId, sid):
    """
    基于用户删除便签
    :param userId: str
    :param sid: str
    :return: None
    """
    get_homepage_notes_url = host + f"/v3/notesvr/user/{userId}/home/startindex/0/rows/50/notes"
    get_recyclebin_url = host + f'/v3/notesvr/user/{userId}/invalid/startindex/0/rows/50/notes'
    get_headers = {
        'Cookie': f'wps_sid={sid}',
    }

    del_headers = {
        'Cookie': f'wps_sid={sid}',
        'X-user-key': f'{userId}'
    }
    # 获取所有便签并软删除
    res = requests.get(url = get_homepage_notes_url, headers = get_headers)
    d_notes = []
    for note in res.json()['webNotes']:
        d_notes.append(note['noteId'])
    for note_id in d_notes:
        requests.post(url = del_notes_url, headers = del_headers, json = {'noteId': note_id})

    # 获取回收站下便签并删除
    while True:
        res = requests.get(url = get_recyclebin_url, headers = get_headers)
        if res.json()['webNotes'] == []:
            break
        del_notes = []
        for note in res.json()['webNotes']:
            del_notes.append(note['noteId'])
        requests.post(url = cleanrecyclebin_url, headers = del_headers, json = {'noteIds': del_notes})


def clear_recycle_notes(user_id, sid, note_ids):
    del_headers = {
        'Cookie': f'wps_sid={sid}',
        'X-user-key': f'{user_id}'
    }
    requests.post(url = cleanrecyclebin_url, headers = del_headers, json = {'noteIds': note_ids})


if __name__ == '__main__':
    clear_notes('459349776', 'V02SS3bAi_Tyd2Jka6BPbfRLnDcM4bw00aa04f6d001b611f10', )
