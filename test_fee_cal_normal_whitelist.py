import unittest
from parameterized import parameterized
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from io import StringIO
from datetime import datetime
import datetime

datetime_format = '%Y-%m-%d %H:%M:%S'
date_format = '%Y-%m-%d'
receiver_list = ['wl_cui@haotingche.net']

class APITest(unittest.TestCase):
    base_url = 'https://api.4-xiang.com'
    token = '28C5326284AF5B433850761B17A593C0'
    #京RTYUPK，2024.10.31日到期
    @parameterized.expand([
        ('case1', {'parkUid': 'P20231205161512wLou', 'licencePlate': '京RYPLK4'}, {'status_code': 200, 'expected_key': 'totalFee', 'totalFee': 0})
    ])
    def test_api_with_params(self, name, params, expected):
        prepare_date()
        endpoint = '/mobile/parking/lp'
        url = self.base_url + endpoint
        headers = {
            'X-Auth-Token': self.token  # 根据实际情况调整token的格式
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            print(response)
            self.assertEqual(response.status_code, expected['status_code'])
            data = response.json()
            print(data)
            if 'data' in data and isinstance(data['data'], dict):
                lookupFeeUnit_data = data['data']
                self.assertIn('totalFee', lookupFeeUnit_data)
                self.assertEqual(lookupFeeUnit_data['totalFee'], expected['totalFee'])
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except ValueError:
            print("Response is not valid JSON")

def prepare_date():
    #理想家园西北进口和出口
    data_array = [
        {"licencePlate":"京RYPLK4", "gateUid":"G20231205161512OkSE", "deltaMinutesAgo": 240}
        #{"licencePlate": "京RYPLK4", "gateUid": "G20231205161512Q1pG", "deltaMinutesAgo": 0}
    ]
    # 遍历列表中的字典
    for element in data_array:
        make_request_lazy_supplement(element['licencePlate'], element['gateUid'], element['deltaMinutesAgo'])

def make_request_lazy_supplement(licencePlate, gateUid, deltaMinutes):
    url = "https://api.4-xiang.com/mgmt/remote/lazy_supplement"
    headers = {
        "x-auth-token": "39f1b0d9-c524-4c0f-b124-b41527dfc134",
        "Content-Type": "application/json"
    }
    current_time = datetime.datetime.now()
    delta_ago = current_time - datetime.timedelta(minutes=deltaMinutes)
    # 将 2 个小时以前的时间转换为时间戳
    eventTime = int(delta_ago.timestamp())

    print(f"当前时间: {current_time}")
    print(f"得到时间戳: {eventTime}")
    # 定义字符串日期
    # 将字符串日期转换为datetime对象
    #date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # 将datetime对象转换为时间戳
    eventTime = eventTime*1000
    print(eventTime)
    data = {
        "reason": "远程人工补登",
        "color": "蓝色",
        "licencePlate": licencePlate,
        "time": eventTime,
        "gateUid": gateUid,
        "eventTime": eventTime
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None

def send_email(content, subject, receiver, file=None):
    sender = 'warning@haotingche.net'
    smtpserver = 'smtp.exmail.qq.com'
    username = 'warning@haotingche.net'
    password = 'H_tingche08'
    content = content

    if file:
        msg = MIMEMultipart()

        # 构建正文
        part_text = MIMEText(content)
        msg.attach(part_text)  # 把正文加到邮件体里面去

        # 构建邮件附件
        part_attach1 = MIMEApplication(open(file, 'rb').read())  # 打开附件
        part_attach1.add_header('Content-Disposition', 'attachment', filename=file.split("/")[-1])  # 为附件命名
        msg.attach(part_attach1)  # 添加附件
    else:
        msg = MIMEText(content, 'html', 'utf-8')

    msg['Subject'] = subject
    msg['From'] = subject
    try:
       # smtp = smtplib.SMTP_SSL('smtpdm.aliyun.com', 465)
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
    except smtplib.SMTPConnectError as e:
        print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('邮件发送失败, ', str(e))
    except Exception as e:
        print('邮件发送异常, ', str(e))


if __name__ == '__main__':
    testCaseName = "回归测试-正常临停计费检查"
# 创建一个 StringIO 对象来捕获测试结果
    test_output = StringIO()
    # 使用 TextTestRunner 并将 stream 参数设置为 test_output
    runner = unittest.TextTestRunner(stream=test_output)

    # 使用 TestLoader 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(APITest)
    result = runner.run(suite)

    # 获取测试结果输出
    test_output_text = test_output.getvalue()
    print(test_output_text)

     # 根据测试结果设置邮件标题
    if result.wasSuccessful():
        subject = testCaseName + " - 所有测试案例通过"
    else:
        subject = testCaseName + f"回归测试 - 测试失败，失败数量: {len(result.failures)}"
    # 邮件配置信息，请根据实际情况修改
    send_email(test_output_text, subject, receiver_list)
