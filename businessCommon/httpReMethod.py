import requests
from common.caseLogs import info, error


class BusinessRequests:
    @staticmethod
    def post(url, json=None, headers=None, sid=None, user_id=None, **kwargs):
        # 如果 headers 为空，则设置默认的 headers
        if headers:
            pass
        else:
            headers = {
                "Cookie": f'wps_sid={sid}',
                'X-user-key': f'{user_id}'
            }
        info(f'send url: {url}')
        info(f'send headers: {headers}')
        info(f'send body: {json}')
        try:
            # 发送 POST 请求
            res = requests.post(url, headers = headers, json = json, timeout = 10, **kwargs)
        except TimeoutError:
            # 如果超时，打印错误信息并抛出 TimeoutError
            error('http requests Timeout!')
            raise TimeoutError
        # 打印接收的状态码和响应体
        info(f'recv code: {res.status_code}')
        info(f'recv body: {res.text}')
        return res

    @staticmethod
    def get(url, headers=None, sid=None, user_id=None, **kwargs):

        # 如果 headers 为空，则设置默认的 headers
        if headers:
            pass
        else:
            headers = {
                "Cookie": f'wps_sid={sid}',
                'X-user-key': f'{user_id}'
            }
        info(f'send url: {url}')
        info(f'send headers: {headers}')
        try:
            # 发送 GET 请求
            res = requests.get(url, headers = headers, timeout = 10, **kwargs)
        except TimeoutError:
            # 如果超时，打印错误信息并抛出 TimeoutError
            error('http requests Timeout!')
            raise TimeoutError
        # 打印接收的状态码和响应体
        info(f'recv code: {res.status_code}')
        info(f'recv body: {res.text}')
        return res

    @staticmethod
    def patch(url, json=None, headers=None, sid=None, user_id=None, **kwargs):
        # 如果 headers 为空，则设置默认的 headers
        if headers:
            pass
        else:
            headers = {
                "Cookie": f'wps_sid={sid}',
                'X-user-key': f'{user_id}'
            }
        info(f'send url: {url}')
        info(f'send headers: {headers}')
        info(f'send body: {json}')
        try:
            # 发送 PATCH 请求
            res = requests.patch(url, headers = headers, json = json, timeout = 10, **kwargs)
        except TimeoutError:
            # 如果超时，打印错误信息并抛出 TimeoutError
            error('http requests Timeout!')
            raise TimeoutError
        # 打印接收的状态码和响应体
        info(f'recv code: {res.status_code}')
        info(f'recv body: {res.text}')
        return res
