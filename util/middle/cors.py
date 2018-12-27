from django.utils.deprecation import MiddlewareMixin


class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # 添加响应头

        # 允许你的域名来获取我的数据
        response['Access-Control-Allow-Origin'] = 'http://localhost:8080'  # cookie跨域这里不能为'*'

        # # 允许你携带Content-Type请求头
        response[
            'Access-Control-Allow-Headers'] = """Content-Type,,Accept-Encoding,Access-Control-Request-Headers,Access-Control-Request-Method,Connection,Host,Origin,User-Agent,Content-Disposition"""
        # # 允许你发送DELETE,PUT
        response['Access-Control-Allow-Methods'] = "GET,POST"

        # 允许使用cookie，使用后，就跟平常没有跨域一样使用。而vue-cookie只是应用在需要我们在在客户端手动操纵cookie的时候
        response['Access-Control-Allow-Credentials'] = 'true'

        return response
