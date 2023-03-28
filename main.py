import requests
import sys
import traceback
from decouple import config
from bs4 import BeautifulSoup
SOCKBOOM_USER = config("SOCKBOOM_USER")
SOCKBOOM_PASSWD = config("SOCKBOOM_PASSWD")
SOCKBOOM_URL = config("SOCKBOOM_URL")
WEB_HOOK = config("WEB_HOOK")
form_data = {
    "email": "${{SOCKBOOM_USER}}",
    "passwd": "${{SOCKBOOM_PASSWD}}"
}
s = requests.Session()
def run(form_data):
	response = s.post("${{SOCKBOOM_URL}}/auth/login", data=form_data)
	print(response.text)
	print(response.status_code)
	if response.status_code == 200:
		resp = s.post("${{SOCKBOOM_URL}}/user/checkin")
		print(resp.json())
		if resp.status_code == 200:
			if "${{WEB_HOOK}}":
				msg_data = {
					"msgtype": "markdown",
					"markdown": {
					"content": response.json()['user'] + "，签到，<font color=\"warning\">"+ resp.json()['msg'] + "</font>"
					}
				}
				s.post("${{WEB_HOOK}}", json=msg_data)
				getUserInfo()
def getUserInfo():
	userinfo = s.get("${{SOCKBOOM_URL}}/user")
	if userinfo.status_code == 200:
		try:
			bs = BeautifulSoup(userinfo.text, 'html.parser')
			ul = bs.find_all("ul", "unstyled")[0]
			li = ul.find_all("li")
			info = ""
			for item in li:
				value = item.find_all("span", "pull-right")[0]
				label = value.previous_sibling
				info += label + value.string + "\n"
			print("当前时间：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\n" + info)
			msg_data = {
				"msgtype": "markdown",
				"markdown": {
				"content": "当前时间：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\n" + info
				}
			}
			s.post("${{WEB_HOOK}}", json=msg_data)
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