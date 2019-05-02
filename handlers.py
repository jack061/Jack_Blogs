'''from coroweb import add_routes, add_static, get, post
from aiohttp import web
import asyncio, os, json, time
@get('/')
def index(a=0, **kw):
    return web.Response(body=b'<h1>Awesome55555%s</h1>' % bytes(str(kw), 'utf8'), content_type='text/html') '''
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from www.coroweb2 import get, post

from models import User, Comment, Blog, next_id
from aiohttp import web
@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }
@get('/blog/{id}')
async def lbj(**kw):
    st=str(kw['id'])
    return web.Response(body=b'<h1>Awesome55555%s</h1>' % bytes(st, 'utf8'), content_type='text/html')
@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict(users=users)