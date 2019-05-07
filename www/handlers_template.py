from coroweb import get, post
from config import configs
from apis import APIValueError, APIResourceNotFoundError, APIPermissionError, Page
from models import User, Comment, Blog, next_id
from handlers_common import text2html,get_page_index
import markdown2
COOKIE_NAME = 'awession'
_COKKIE_KEY = configs.session.secret

#首页
@get('/')
async def index(request):
    blogs =await Blog.findAll()
    return {
        '__template__': 'blogs.html',
        'blogs':blogs
    }
#日志详情页
@get('/blog/{id}')
async def blog_details(id):
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id=?', [id], orderby='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog_details.html',
        'blog': blog,
        'comments': comments
    }
#注册
@get('/register')
async def register():
    return {
        '__template__':'register.html'
}
#登陆
@get('/signin')
async def signin():
    return {
        '__template__':'signin.html'
}
#后台管理列表模板
@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index':get_page_index(page)
}
#后台管理日志创建
@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action':'/api/blogs'
}
#后台管理日志编辑
@get('/manage/blogs/edit')
def manage_edit_blog(id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/edit/' + id
}

