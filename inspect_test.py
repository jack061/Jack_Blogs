import inspect
def a(a, b=0, *c, d, e=1, **f):
    pass
def get_required_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        #判断参数为a=0类型的固定值参数并且没有默认值
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)
print(get_required_kw_args(a))
    
aa = inspect.signature(a)
print("inspect signature (fn):%s" % aa)
print("type of inspect signature (fn):%s" % type(aa))
bb = aa.parameters
print("inspect signature.parameter:%s " % bb)
print("typeof signature.parameter:%s" % type(bb))
for k, v in bb.items():
    print("mappingporxy.items is:%s and %s" % (k, v))
    print(type(k),':', type(v))
    kind = v.kind
    print("parameter kind is:%s" % kind)
    print(type(kind))
    default = v.default
    print("parameter default:%s" % default)
    print(type(default))

import hashlib
sha1_passwd = '%s:%s' % ('lbja2', '123')
passwd = hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest()
print(passwd)