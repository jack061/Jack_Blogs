# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

'''
async web application.
'''

import logging; logging.basicConfig(level=logging.INFO)
import sys
import asyncio, os, json, time
import orm
from datetime import datetime
from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from handlers_factory import logger_factory, data_factory, auth_factory, response_factory
from coroweb import add_routes, add_static
from config import configs
from handlers_filter import detetime_filter
from handlers_common import cookie2user, COOKIE_NAME
import nest_asyncio
nest_asyncio.apply()
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join( os.path.join(os.path.dirname(os.path.abspath('__file__')), r'www\templates'))
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env

async def init(loop):
    await orm.create_pool(loop=loop,**configs.db)
    app = web.Application(loop=loop, middlewares=[
        logger_factory,auth_factory, response_factory
    ])
    init_jinja2(app, filters=dict(datetime=detetime_filter))
    add_routes(app, 'handlers','handlers_common','handlers_template')
    add_static(app)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 1111)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()