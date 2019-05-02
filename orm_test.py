import asyncio
import orm
from models import User, Blog, Comment
import nest_asyncio
nest_asyncio.apply()
async def test(loop):
    await orm.create_pool(loop=loop,user='root', password='776007', db='awesome')
    #u = User(name='Test3', email='test@example.com2', #passwd='1234567890', image='about:blank')
    #await  u.save()
    await  User().findNumber('id', 'name=Test')
    print(id)
loop=asyncio.get_event_loop()
loop.run_until_complete(test(loop))
#loop.close()