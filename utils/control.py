# import requests

# # 树莓派的IP地址和端口
# raspberry_pi_ip = 'http://192.168.137.23:5000'

# # 控制继电器的函数
# def control_relay(state):
#     url = f"{raspberry_pi_ip}/control"
#     data = {'state': state}
#     response = requests.post(url, data=data)
#     print(response.status_code)
#     if response.status_code == 200:
#         print(f"继电器已成功切换到: {state}")
#     else:
#         print("控制继电器时发生错误")

# # 示例使用
# control_relay('on')
# input()
# control_relay('off')

import paramiko
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.137.23', username='aiart', password='123456789')
 
stdin, stdout, stderr = ssh.exec_command('python ~/ICCI/code/pin_control.py 1 on')
print(stdout.read())
print(stderr.read())

ssh.close()

