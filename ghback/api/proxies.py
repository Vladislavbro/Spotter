import requests
from random import choice
from random_user_agent.user_agent import UserAgent
from time import sleep


user_agent_rotator = UserAgent()

proxies = [
    'http://CrCWgH3r:bb3KGpCE@91.230.38.109:64220',
    'http://CrCWgH3r:bb3KGpCE@45.85.66.206:50933',
    'http://CrCWgH3r:bb3KGpCE@194.55.105.13:47634',
    'http://CrCWgH3r:bb3KGpCE@45.140.64.241:46385',
    'http://CrCWgH3r:bb3KGpCE@45.154.160.110:61956',
    'http://CrCWgH3r:bb3KGpCE@45.154.163.79:49156',
    'http://CrCWgH3r:bb3KGpCE@91.236.121.164:47682',
    'http://CrCWgH3r:bb3KGpCE@45.152.117.122:63971',
    'http://CrCWgH3r:bb3KGpCE@77.83.80.63:53622',
    'http://CrCWgH3r:bb3KGpCE@194.156.93.162:63025',
    'http://CrCWgH3r:bb3KGpCE@45.10.108.222:47210',
    'http://CrCWgH3r:bb3KGpCE@45.142.254.151:59861',
    'http://CrCWgH3r:bb3KGpCE@45.144.37.181:49839',
    'http://CrCWgH3r:bb3KGpCE@212.193.164.24:46273',
    'http://CrCWgH3r:bb3KGpCE@195.209.145.2:57269',
    'http://CrCWgH3r:bb3KGpCE@195.208.21.18:50040',
    'http://CrCWgH3r:bb3KGpCE@212.193.171.171:47732',
    'http://CrCWgH3r:bb3KGpCE@212.193.168.135:50421',
    'http://CrCWgH3r:bb3KGpCE@195.209.188.116:46413',
    'http://CrCWgH3r:bb3KGpCE@195.209.135.55:53533',
    'http://CrCWgH3r:bb3KGpCE@195.208.84.102:46432',
    'http://CrCWgH3r:bb3KGpCE@212.193.167.162:51246',
    'http://CrCWgH3r:bb3KGpCE@212.193.102.119:52577',
    'http://CrCWgH3r:bb3KGpCE@212.193.162.212:48864',
    'http://CrCWgH3r:bb3KGpCE@212.192.228.195:62665',
    'http://CrCWgH3r:bb3KGpCE@212.192.192.235:51607',
    'http://CrCWgH3r:bb3KGpCE@212.192.168.210:45786',
    'http://CrCWgH3r:bb3KGpCE@195.208.56.149:59609',
    'http://CrCWgH3r:bb3KGpCE@195.208.110.210:64662',
    'http://CrCWgH3r:bb3KGpCE@195.208.117.194:53780',
    'http://CrCWgH3r:bb3KGpCE@195.208.20.87:50544',
    'http://CrCWgH3r:bb3KGpCE@195.19.219.150:49585',
    'http://CrCWgH3r:bb3KGpCE@212.192.58.76:49214',
    'http://CrCWgH3r:bb3KGpCE@212.192.59.89:61151',
    'http://CrCWgH3r:bb3KGpCE@212.193.186.222:46301',
    'http://CrCWgH3r:bb3KGpCE@212.193.187.144:47355',
    'http://CrCWgH3r:bb3KGpCE@212.193.188.155:62075',
    'http://CrCWgH3r:bb3KGpCE@212.193.189.44:58696',
    'http://CrCWgH3r:bb3KGpCE@212.193.190.137:52004',
    'http://CrCWgH3r:bb3KGpCE@212.193.191.199:56319',
    'http://CrCWgH3r:bb3KGpCE@212.193.185.134:45901',
    'http://CrCWgH3r:bb3KGpCE@193.232.89.127:55065',
    'http://CrCWgH3r:bb3KGpCE@194.190.211.31:59906',
    'http://CrCWgH3r:bb3KGpCE@5.8.51.45:62666',
    'http://CrCWgH3r:bb3KGpCE@31.184.243.108:51805',
    'http://CrCWgH3r:bb3KGpCE@109.196.165.103:46090',
    'http://CrCWgH3r:bb3KGpCE@109.94.211.191:50361',
    'http://CrCWgH3r:bb3KGpCE@194.32.239.170:59713',
    'http://CrCWgH3r:bb3KGpCE@194.32.238.125:52494',
]


def check_proxies():
    for proxy in proxies:
        headers = {
            'User-Agent': user_agent_rotator.get_random_user_agent()
        }
        proxy = choice(proxies)
        url = 'https://ipinfo.io'
        response = requests.get(url, headers=headers, proxies={
            'http': proxy,
            'https': proxy,
        })
        print(proxy, response.status_code)
        sleep(1)


if __name__ == '__main__':
    check_proxies()

# 'http://CrCWgH3r:bb3KGpCE@84.54.28.154:56818',
# 'http://CrCWgH3r:bb3KGpCE@84.252.71.19:51548',
# 'http://CrCWgH3r:bb3KGpCE@91.188.212.142:59265',
# 'http://CrCWgH3r:bb3KGpCE@91.188.213.10:55056',
# 'http://CrCWgH3r:bb3KGpCE@91.188.215.244:58537',
# 'http://CrCWgH3r:bb3KGpCE@176.53.173.228:51946',
# 'http://CrCWgH3r:bb3KGpCE@176.53.175.160:58819',
# 'http://CrCWgH3r:bb3KGpCE@194.156.117.241:61238',
# 'http://CrCWgH3r:bb3KGpCE@194.156.118.131:47198',
# 'http://CrCWgH3r:bb3KGpCE@194.156.119.99:62839',
# 'http://CrCWgH3r:bb3KGpCE@5.8.54.125:53012',
# 'http://CrCWgH3r:bb3KGpCE@5.8.9.34:64952',
# 'http://CrCWgH3r:bb3KGpCE@95.215.0.144:50902',
# 'http://CrCWgH3r:bb3KGpCE@5.8.10.176:46533',
# 'http://CrCWgH3r:bb3KGpCE@31.184.192.52:63995',
# 'http://CrCWgH3r:bb3KGpCE@31.184.197.182:54637',
# 'http://CrCWgH3r:bb3KGpCE@31.184.194.53:47883',
# 'http://CrCWgH3r:bb3KGpCE@78.142.239.103:50257',
# 'http://CrCWgH3r:bb3KGpCE@77.83.81.2:57803',
# 'http://CrCWgH3r:bb3KGpCE@77.83.72.58:59985',
# 'http://CrCWgH3r:bb3KGpCE@85.208.84.98:61851',
# 'http://CrCWgH3r:bb3KGpCE@194.156.122.62:45864',
# 'http://CrCWgH3r:bb3KGpCE@213.226.113.200:62598',
# 'http://CrCWgH3r:bb3KGpCE@81.16.142.149:64697',
# 'http://CrCWgH3r:bb3KGpCE@213.166.80.198:49691',
# 'http://CrCWgH3r:bb3KGpCE@91.188.245.171:49667',
