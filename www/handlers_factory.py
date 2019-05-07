import logging; logging.basicConfig(level=logging.info)
import sys
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web
import orm
from handlers_common import cookie2user,COOKIE_NAME
#日志拦截
async def logger_factory(app, handler):
    async def logger(request):
        logging.info('Request:%s %s' % (request.method, request.path))
        return await (handler(request))
    return logger
#request 数据格式转换
async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json:%s' % str(request.__data__))
        elif request.content_type.startswith('application/x-www-form-urlencoded'):
            request.__data__ = await request.post()
            logging.info('request from:%s' % str(request.__data__))
        return await handler(request)
    return parse_data
#权限校验
async def auth_factory(app, handler):
    async def auth(request):
        logging.info('check user:%s %s' % (request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = await cookie2user(cookie_str)
            if user:
                logging.info('set current user:%s' % user.email)
                request.__user__ = user
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPNotFound()
        return await handler(request)
    return auth
#request 返回数据处理
async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and r >= 100 and r < 600:
            pass
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                pass
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response

                

