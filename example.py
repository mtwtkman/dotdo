from wsgiref.simple_server import make_server
from pyramid.request import Request
from pyramid.response import Response
from pyramid.config import Configurator


def hi(request: Request) -> Response:
    return Response(f'hi, {request.matchdict["x"]}')


def server_factory(global_conf: Configurator, host, port):
    def run(app):
        s = make_server(host, int(port), app)
        s.serve_forever()
    return run


def main(global_config: Configurator, **settings):
    with Configurator(settings=settings) as config:
        config.include('dotdo')
        config.add_dotdo_route('hi', '/hoge-fuga/{x}')
        config.add_view(hi, route_name='hi')
    return config.make_wsgi_app()