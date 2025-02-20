import unittest
from parameterized import parameterized
import requests

class APITest(unittest.TestCase):
    base_url = 'http://cloud.4-xiang.com'

    @parameterized.expand([
        ('case1', {'gateId': 216}),
        ('case1', {'gateId': 218}),
        ('case1', {'gateId': 219}),
        ('case3', {'gateId': 220})
    ])
    def test_api_with_params(self, name, params):
        endpoint = '/api/vi/online_pay/lookup_with_gate'
        url = self.base_url + endpoint
        try:
            response = requests.get(url, params=params)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            # 处理复杂嵌套结构
            if 'lookupFeeUnit' in data and isinstance(data['lookupFeeUnit'], dict):
                lookupFeeUnit_data = data['lookupFeeUnit']
                self.assertIn('totalFee', lookupFeeUnit_data)
                #self.assertEqual(nested_data['gateId'], 'expected_sub_value')
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except ValueError:
            print("Response is not valid JSON")

if __name__ == '__main__':
    unittest.main()
