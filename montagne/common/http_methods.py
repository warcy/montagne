import json
import inspect
from montagne.common import hub
from montagne.common.log import getLogger
from eventlet.green.urllib import request, error

LOG = getLogger(__name__)

_DEFAULT_TIME_OUT = 2


def encode(obj, charset='utf-8'):
    return json.dumps(obj).encode(charset)


def decode(byte, charset='utf-8'):
    return json.loads(byte.decode(charset))


def get(url, headers=None, decode='utf-8'):
    return _base_method(url, headers=headers, decode=decode)


def post(url, data, headers=None, decode='utf-8'):
    assert isinstance(data, bytes)
    return _base_method(url, data=data, method='POST',
                        headers=headers, decode=decode)


def put(url, data, headers=None, decode='utf-8'):
    assert isinstance(data, bytes)
    return _base_method(url, data=data, method='PUT',
                        headers=headers, decode=decode)


def delete(url, data, headers=None, decode='utf-8'):
    assert isinstance(data, bytes)
    return _base_method(url, data=data, method='DELETE',
                        headers=headers, decode=decode)


def _base_method(url, data=None, headers=None,
                 origin_req_host=None, unverifiable=False,
                 method=None, decode='utf-8'):
    def _caller(stack_number):
        try:
            info = inspect.stack()[stack_number]
            caller_func = info[3]
            caller_inst = info[0].f_locals.get('self')
            if caller_inst:
                return str(caller_inst) + ' ' + caller_func
            else:
                return str(caller_func)
        except:
            return str('can not find caller')

    if headers is None:
        headers = {}

    req = request.Request(
        url=url, data=data, headers=headers,
        origin_req_host=origin_req_host, unverifiable=unverifiable,
        method=method)

    rval = None
    try:
        with hub.Timeout(_DEFAULT_TIME_OUT, True):
            response = request.urlopen(req)
            message = response.read()
            msg_dec = message.decode(decode)
            rval = json.loads(msg_dec)
            LOG.debug('receive')
    except hub.Timeout:
        LOG.error({'method': _caller(2),
                   'caller': _caller(3),
                   'url': url,
                   'timeout': str(_DEFAULT_TIME_OUT)})
    except error.HTTPError as e:
        LOG.error({'method': _caller(2),
                   'caller': _caller(3),
                   'url': url,
                   'error': {
                       'code': e.code,
                       'msg': e.msg}})
    except:
        LOG.error({'method': _caller(2),
                   'caller': _caller(3),
                   'url': url,
                   'error': 'uncovered error'})
    return rval

