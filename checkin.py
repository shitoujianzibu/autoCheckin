import requests
import os
import sys
import traceback

SOCKBOOM_URL = os.environ["SOCKBOOM_URL"]
SOCKBOOM_USER = os.environ["SOCKBOOM_USER"]
SOCKBOOM_PASSWD = os.environ["SOCKBOOM_PASSWD"]

form_data = {
"email": SOCKBOOM_USER,
"passwd": SOCKBOOM_PASSWD
}
def run(form_data):
    s = requests.Session()
    response = s.post(SOCKBOOM_URL + "/auth/login", data=form_data)
    print(response.text)
    print(response.status_code)
    if response.status_code == 200:
    resp = s.post(SOCKBOOM_URL + "/user/checkin")
    print(resp.text)
def main():
    run(form_data)
    print("run1")
if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc()