from bs4 import BeautifulSoup
from decouple import config
import requests
import sys
import traceback
from datetime import datetime
from datetime import timedelta
from datetime import timezone
SOCKBOOM_USER = config("SOCKBOOM_USER")
SOCKBOOM_PASSWD = config("SOCKBOOM_PASSWD")
SOCKBOOM_URL = config("SOCKBOOM_URL")
WEB_HOOK = config("WEB_HOOK")
SHA_TZ = timezone(
	timedelta(hours=8),
	name='Asia/Shanghai',
)

form_data = {
	"email": SOCKBOOM_USER,
	"passwd": SOCKBOOM_PASSWD
}
currentUser = ""
checkInMsg = ""
s = requests.Session()
def run(form_data):
	response = s.post("https://oapi.dingtalk.com/robot/send?access_token=f253c2209e3e65f0a0fe19751b744efd586cd02e89d8bbcd42708e410232695c", {
    "text": '测试'
  })
	print(response.text)
	print(response.status_code)
def main():
	run(form_data)
	print("main")
if __name__ == '__main__':
	try:
		sys.exit(main())
	except Exception as e:
		traceback.print_exc()