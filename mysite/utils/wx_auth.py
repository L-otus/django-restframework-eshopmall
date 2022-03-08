import requests
import json

AppSecret = '在开发者平台查看'
js_code = ''

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
}
url = 'https://api.weixin.qq.com/sns/jscode2session?'


# 微信认证
def auth_code2Session(js_code):
    appid='wx87d92966be73400d'
    secret= AppSecret
    grant_type: 'authorization_code'
    wurl=url+'appid='+appid+'&secret='+secret+'&js_code='+js_code+'&grant_type=authorization_code'
    res = requests.get(wurl)
    res.encoding = 'utf-8'
    r_list = res.text
    j_list = json.loads(r_list)
    #res = requests.get(url, headers=headers, params=params, verify=True)

    if 'errcode' in res:
        # 有错误码
        return {'erc': res['errcode'], 'msg': res['errmsg']}
        # 登录成功
    openid = res['openid']
    key = res['session_key']
    return {'openid':openid,'session_key':key}