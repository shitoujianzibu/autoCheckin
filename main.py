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
	response = s.post(SOCKBOOM_URL + "/auth/login", data=form_data)
	print(response.text)
	print(response.status_code)
	if response.status_code == 200:
		# 声明是全局变量
		global currentUser
		currentUser = response.json()['user']
		checkInRes = s.post(SOCKBOOM_URL + "/user/checkin")
		print(checkInRes.json())
		if checkInRes.status_code == 200:
			global checkInMsg
			checkInMsg = checkInRes.json()['msg']
			getUserInfo()
def getUserInfo():
	userinfo = s.get(SOCKBOOM_URL + "/user")
	if userinfo.status_code == 200:
		try:
			# 有微信机器人
			if WEB_HOOK:
				bs = BeautifulSoup(userinfo.text, 'html.parser')
				ul = bs.find_all("ul", "unstyled")[0]
				li = ul.find_all("li")
				info = ""
				for item in li:
					value = item.find_all("span", "pull-right")[0]
					label = value.previous_sibling
					info += label.strip() + ": " + value.string + "\n"
				utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
				beijing_now = utc_now.astimezone(SHA_TZ)
				print("当前时间：" + beijing_now.strftime('%Y-%m-%d %H:%M:%S') + "\n" + info)
				msg_data = {
					"msgtype": "markdown",
					"markdown": {
					"text": "当前用户: " + currentUser + "\n" 
						+ "当前时间: " + beijing_now.strftime('%Y-%m-%d %H:%M:%S') + "\n"
						+ "签到: <font color=\"warning\">" + checkInMsg + "</font>\n"
						+ info
					}
				}
				s.post(WEB_HOOK, json=msg_data)
		except Exception as e:
			print(e)
def main():
	run(form_data)
	print("main")
if __name__ == '__main__':
	try:
		sys.exit(main())
	except Exception as e:
		traceback.print_exc()