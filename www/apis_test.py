from apis import APIError, APIValueError
import logging
class A:
    def __call__(self, *args):
        try:
            if a == 0:
                raise APIValueError()
            a = 10 / 0
            return a
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)
a = A()
a()
