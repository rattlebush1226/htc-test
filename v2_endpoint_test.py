import unittest
from parameterized import parameterized
import requests

class APITest(unittest.TestCase):
    base_url = 'https://api.4-xiang.com'
    # 假设这里是你的token值，你可以根据实际情况修改
    token = '28C5326284AF5B433850761B17A593C0'  

    @parameterized.expand([
        ('case1', {'parkUid': 'P20231205161512wLou', 'gateUid':'G20231205161512Q1pG' }),
        ('case2', {'parkUid': 'P20231205161512wLou', 'gateUid':'G20231205161512Q1pG' }),
        ('case3', {'parkUid': 'P20231205161512wLou', 'gateUid':'G20231205161512Q1pG' })
    ])
    def test_api_with_params(self, name, params):
        endpoint = '/mobile/parking/gate_enter'
        url = self.base_url + endpoint
        # 定义请求头，添加token
        headers = {
            'X-Auth-Token': self.token  # 根据实际情况调整token的格式
        }
        try:
            # 在请求中传入headers参数
            response = requests.get(url, params=params, headers=headers)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            # 处理复杂嵌套结构
            if 'data' in data and isinstance(data['data'], dict):
                data_data = data['data']
                self.assertIn('parkUid', data_data)
                # self.assertEqual(nested_data['gateId'], 'expected_sub_value')
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except ValueError:
            print("Response is not valid JSON")

if __name__ == '__main__':
    unittest.main()
