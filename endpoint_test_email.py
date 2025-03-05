import unittest
from parameterized import parameterized
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from io import StringIO
import sys
datetime_format = '%Y-%m-%d %H:%M:%S'
date_format = '%Y-%m-%d'

receiver_list = ['wl_cui@haotingche.net']

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

def send_email(content, receiver, file=None):
    sender = 'warning@haotingche.net'
    subject = "回归测试"
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
    msg['From'] = '回归测试-车道健康检测'
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
    # 重定向标准输出以捕获测试结果
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
#    runner = unittest.TextTestRunner()
#    result = runner.run(unittest.makeSuite(APITest))

    runner = unittest.TextTestRunner()
    # 使用 TestLoader 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(APITest)
    result = runner.run(suite)
    sys.stdout = old_stdout

    # 获取测试结果输出
    test_output = mystdout.getvalue()
    print(test_output)

    # 邮件配置信息，请根据实际情况修改
    send_email(test_output, receiver_list)
    # 发送邮件
    #send_email(subject, test_output, sender_email, sender_password, receiver_email)
