import unittest


class CheckPro(unittest.TestCase):
    def check_output(self, expected, actual):
        """
        接口返回体（dict字典结构）通用校验方法
        :param expected: 期望值的协议，协议需要对齐接口文档中的数据结构。
        ① 接口文档所描述的key 需要对齐到数据结构体中；
        ② 如果进行动态值校验即校验数据类型， 只需把期望值key的值描述成类型；（'order_id': int）
        ③ 如果进行精确值的校验，把值明确写在数据结构上即可。（'order_id': 123）
        :param actual:返回体（json需转义为dict）
        :return:
        """
        self.assertEqual(len(expected.keys()), len(actual.keys()),
                         msg = f'{actual.keys()} object keys len inconsistent!')   # 校验字段长度，是否存在多余字段
        for key, value in expected.items():
            self.assertIn(key, actual.keys(), msg = f'{key} not in actual')        # 校验字段是否存在
            if isinstance(value, type):                                            # 校验字段的数据类型(字段为动态值)
                self.assertEqual(value, type(actual[key]), msg = f'{key} type inconsistent!')
            elif isinstance(value, dict):                                          # 字段为字典结构时
                self.check_output(value, actual[key])
            elif isinstance(value, list):                                          # 字段为列表结构时
                self.assertEqual(len(value), len(actual[key]),
                                 msg = f'{actual.keys()} object items len inconsistent!')
                for lst_i in range(len(value)):
                    if isinstance(value[lst_i], type):
                        self.assertEqual(value[lst_i], actual[key][lst_i],
                                         msg = f'{value[lst_i]} type inconsistent!')
                    elif isinstance(value[lst_i], dict):
                        self.check_output(value[lst_i], actual[key][lst_i])
                    else:
                        self.assertEqual(value[lst_i], actual[key][lst_i],
                                         msg = f'{value[lst_i]} value inconsistent!')
            else:
                self.assertEqual(value, actual[key], msg = f'{key} value inconsistent!')    # 校验字段的精确值
