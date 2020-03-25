import re
from typing import Sequence, Tuple

from pyramid.config import Configurator


def to_dotdo(pattern: str, allowed_delimiter: Sequence[str]=('-', '_')) -> str:
    """URL path converter

    This function converts original URL pattern to struts 1 like URL pattern. But I don't know how struts 1 URL pattern is.
    This function works like below. (This is my irresponsible guess.)

    >>> assert to_dotdo('/') == '/'
    >>> assert to_dotdo('/hoge_fuga') == '/HogeFuga.do'
    >>> assert to_dotdo('/hoge__fuga') == '/HogeFuga.do'
    >>> assert to_dotdo('/hoge-fuga') == '/HogeFuga.do'
    >>> assert to_dotdo('/hoge-fuga_piyo') == '/HogeFugaPiyo.do'
    >>> assert to_dotdo('/hoge') == '/Hoge.do'
    >>> assert to_dotdo('/hoge/{id}') == '/Hoge.do/{id}'
    >>> assert to_dotdo('/hoge/fuga') == '/hoge/Fuga.do'
    >>> assert to_dotdo('/hoge/fuga/{id}') == '/hoge/Fuga.do/{id}'
    >>> assert to_dotdo('/hoge/{id}/fuga/') == '/hoge/{id}/Fuga.do/'

    This conversion rule is just "I treat the end of URL pattern resource name as ActionServlet". Simple.
    """
    splitted = pattern.split('/')
    filtered = [(i, x) for i, x in enumerate(splitted) if x and '{' not in x]
    if not filtered:
        return pattern

    index, tail = filtered[-1]

    delimiters = ''.join(allowed_delimiter)
    DELIMITER_PATTERN = re.compile(fr'[{delimiters}]+')
    converted = ''.join(x.capitalize() for x in re.split(DELIMITER_PATTERN ,tail))
    return '/'.join(x if i != index else f'{converted}.do' for i, x in enumerate(splitted))


def struts_one_like(config: Configurator, route_name: str, pattern: str, *add_route_args, **add_route_kwargs):
    config.add_route(route_name, to_dotdo(pattern), *add_route_args, **add_route_kwargs)


def includeme(config: Configurator):
    config.add_directive('add_dotdo_route', struts_one_like)