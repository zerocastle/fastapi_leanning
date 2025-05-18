from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import Request


# rest full 하게 통신을 하려면 form tag는 put , patch가 적용이 안된다 그렇기에 middleware에서
# custom method 를 해주는 방향으로 통신을한다.


class DummyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("### request info : ", request.url, request.method)
        print("### request type : ", type(request))
        response = await call_next(request)
        return response
