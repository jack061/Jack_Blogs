import logging, hashlib, base64, asyncio,time
from apis import APIValueError, APIResourceNotFoundError, APIPermissionError, Page
from config import configs
from models import User
COOKIE_NAME = 'awesession'
_COKKIE_KEY = configs.session.secret
#校验是否有admin权限
def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError
#校验页码，出错时设置为1        
def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p
#生成cookie(用户id-密码-过期时间-cookie_key)
def user2cookie(user, max_age):
    expires = str(int(time.time()) + max_age)
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COKKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)
#解密cookie
async def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COKKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '*' * 15
        return user2cookie
    except Exception as e:
        logging.exception(e)
        return None
#文本转换html,去除空行，替换特殊字符        
def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


