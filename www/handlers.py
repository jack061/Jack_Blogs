
__author__ = 'Michael Liao'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
import markdown2
from models import User, Comment, Blog, next_id
from aiohttp import web
from apis import APIValueError, APIResourceNotFoundError, APIPermissionError, Page
from handlers_common import get_page_index,COOKIE_NAME,check_admin,user2cookie
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

#注册    
@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users =await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIValueError('register:failed', 'Email is existed')
    uid = next_id()
    sha1passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    #设置响应cookie
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '********'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r
#登陆    
@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'invalid email')
    if not passwd:
        raise APIValueError('passwd', 'invalid passwd')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'not exists')
    user = users[0]
    #check passwd
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if sha1.hexdigest() != user.passwd:
        raise APIValueError('passwd', 'invalid passwd')
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), expires=86400, httponly=True)
    user.passwd='***********'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r
#日志分页列表
@get('/api/blogs')
async def api_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = await Blog.findAll(orderby='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)
#日志json数据
@get('/blog_json/{id}')
async def blog_json(id):
    blog_entity = await Blog.find(id)
    #blog = json.dumps(blog_entity, ensure_ascii=False).encode('utf-8')
    return blog_entity    
#日志创建   
@post('/api/blogs/create')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty')      
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog
#日志编辑    
@post('/api/blogs/edit/{id}')
async def api_edit_blog(id,request, *, name, summary, content):
    #check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty')
    blog = await Blog.find(id)
    blog.name = name
    blog.summary = summary
    blog.content =content
    await blog.update()
    return blog


                