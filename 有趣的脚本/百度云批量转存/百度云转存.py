#! /usr/bin/env python3
import requests

from base64 import b64encode
from json import loads
from re import compile as re_compile
from time import time
from typing import Optional, Union
from urllib.parse import urlencode, unquote
from uuid import uuid4


__version__ = (0, 0, 3)
__author__ = 'ChenyangGao <https://github.com/ChenyangGao>'


# TODO: 请把 Cookie 写到下面
HEADERS = '''
Cookie: 
'''


try:
    def startfile(path, _func=__import__('os').startfile):
        '打开文件或者文件夹 (适用于 Windows)'
        _func(path)
except AttributeError:
    _PLATFROM_SYSTEM = __import__('platform').system()
    if _PLATFROM_SYSTEM == 'Linux':
        def startfile(path, _func=__import__('subprocess').Popen):
            '打开文件或者文件夹 (适用于 Linux)'
            _func(['xdg-open', path])
    elif _PLATFROM_SYSTEM == 'Darwin':
        def startfile(path, _func=__import__('subprocess').Popen):
            '打开文件或者文件夹 (适用于 MacOSX)'
            _func(['open', path])
    else:
        def startfile(path, _func=lambda x: x):
            '说是要打开文件或者文件夹，其实什么都不做'
            # TODO: 实际上倒是可以用浏览器打开这个文件夹
            _func(path)
    del _PLATFROM_SYSTEM


def text_to_dict(
    text: str, item_sep: str='\n', kv_sep: str='='
) -> dict:
    return dict(item.split(kv_sep, 1) # type: ignore
                for item in text.split(item_sep) if item)


class TransferError(Exception):
    pass


class Errno(TransferError):
    pass


class DuPanTransfer:
    '百度网盘文件转存'

    def __init__(self, headers: Union[dict, str] = HEADERS):
        if isinstance(headers, str):
            try:
                headers = text_to_dict(
                    headers, kv_sep=': ')
            except ValueError as exc:
                raise ValueError('请求头格式错误，正确形如\nkey1: value1\nkey2: value2\n...') from exc

        session = self.session = requests.session()
        if 'Cookie' not in headers or 'BAIDUID=' not in headers['Cookie']:
            if input('检测到未登录，是否采取扫码登录？ (Y)/N ').strip().upper() in ('', 'Y'):
                headers.pop('Cookie', None)
                self.login_by_qrcode()
                cookiejar = session.cookies
        else:
            session.headers.update(headers)
            cookiejar = requests.cookies.cookiejar_from_dict(
                text_to_dict(
                    session.headers['Cookie'],
                    item_sep='; ', 
                    kv_sep='=', 
                )
            )

        self.logid = b64encode(cookiejar['BAIDUID'].encode('ascii')).decode()

    def login_by_qrcode(self):
        '用 app 扫描二维码登录'
        ss = self.session

        gid = str(uuid4()).upper()

        msg_getqrcode = self._fetch_json(
            'GET', 
            'https://passport.baidu.com/v2/api/getqrcode', 
            params={
                'lp': 'pc',
                'qrloginfrom': 'pc',
                'gid': gid,
                'apiver': 'v3',
                'tpl': 'netdisk',
            }
        )

        imgurl = 'https://' + msg_getqrcode['imgurl']
        channel_id = msg_getqrcode['sign']

        img = self._fetch('GET', imgurl)
        open('qrimg.png', 'wb').write(img)
        startfile('qrimg.png')

        def query_login_status():
            with ss.get(
                'https://passport.baidu.com/channel/unicast', 
                params={
                    'channel_id': channel_id, 
                    'tpl': 'netdisk',
                    'gid': gid, 
                    'apiver': 'v3',
                    }
            ) as resp:
                resp.raise_for_status()
                return resp.json()

        while True:
            print('请扫码或点击登录！')
            msg = query_login_status()
            if msg['errno'] == 0:
                channel_v = msg['channel_v']
                if type(channel_v) is str:
                    channel_v = loads(channel_v)
                if channel_v['status'] == 0:
                    print('成功扫码登录')
                    break
                elif channel_v['status'] == 1:
                    print('扫码成功')
                elif channel_v['status'] == 2:
                    raise Exception('取消扫码登录')
            elif msg['errno'] == 1:
                pass
            else:
                raise Exception(msg)

        with ss.get(
            'https://passport.baidu.com/v3/login/main/qrbdusslogin?bduss='+channel_v['v']
        ) as resp:
            resp.raise_for_status()

    def _fetch(self, *args, **kwargs):
        with self.session.request(*args, **kwargs) as resp:
            resp.raise_for_status()
        return resp.content

    def _fetch_json(self, *args, **kwargs):
        with self.session.request(*args, **kwargs) as resp:
            resp.raise_for_status()
            msg = resp.json()
        if msg['errno'] != 0:
            raise Errno(msg)
        return msg

    def verify(
        self, 
        url_or_shorturl: str, 
        code: str, 
        bdstoken: str = '', 
    ) -> dict:
        '提交验证码'
        cre1 = re_compile(r'https?://pan\.baidu\.com/s/1(?P<shorturl>[^?&#]+).*')
        cre2 = re_compile(r'https?://pan\.baidu\.com/share/init\?(?:.*?&)?surl=(?P<shorturl>[^&#]+).*')
        while True:
            match = cre1.fullmatch(url_or_shorturl)
            if match:
                shorturl = match['shorturl']
                break
            match = cre2.fullmatch(url_or_shorturl)
            if match:
                shorturl = match['shorturl']
                break
            shorturl = url_or_shorturl
            break

        session = self.session
        msg = self._fetch_json(
            'POST', 
            'https://pan.baidu.com/share/verify', 
            params={
                'surl': shorturl,
                't': int(time() * 1000), 
                'channel': 'chunlei', 
                'web': 1, 
                'app_id': 250528,
                'clienttype': 0, 
                'bdstoken': bdstoken, 
                'logid': self.logid,
                'clienttype': 0, 
            }, 
            data={'pwd': code}, 
            headers={'Referer': 'https://pan.baidu.com/share/init?surl=' + shorturl}
        )

        session.cookies.set('BDCLND', msg['randsk'], domain='')
        return msg

    @staticmethod
    def _extract_data(
        html_content: bytes,
        _cre=re_compile(br'locals\.mset\((.*?)\);'),
    ) -> dict:
        '提取下载相关数据'
        match = _cre.search(html_content)
        # 不能匹配：可能是页面下载失败、被服务器限制访问等原因
        if match is None:
            raise TransferError('没有提取到页面相关数据，可能是没有登录、链接失效、分享被取消等原因')
        return loads(match[1])

    def transfer(
        self,
        link: str, 
        code: Optional[str] = None,
        save_folder: str = '/', 
        ensure_save_folder: bool = False, 
    ) -> dict:
        '''转存文件到百度网盘

        :param link: 分享链接
        :param code: 验证码，可选
        :param save_folder: 存储到这个文件夹，默认是 /，也就是网盘根目录
        :param ensure_save_folder: 如果为 True，则保证在转存前 `save_folder` 是存在的

        :return: 转存接口返回到 JSON 信息
        '''
        # 当 link 是 http 协议时，会重定向到 https 的对应页面
        if ensure_save_folder:
            self.create_folder(save_folder)
        if link.startswith('http://'):
            link = 'https' + link[4:]
        session = self.session
        html_content = self._fetch('GET', link)
        data = self._extract_data(html_content)
        # 如果出现验证框，说明需要输入 code
        if b'"verify-form"' in html_content:
            if code is None:
                raise TransferError('需要密码')
            self.verify(link, code, data['bdstoken'])
            html_content = self._fetch('GET', link)
            data = self._extract_data(html_content)

        file_list = data['file_list']
        # 没有找到文件列表，这可能意味着分享链接失效了
        if file_list is None:
            raise TransferError('没有找到下载文件，可能是链接失效、分享被取消等原因')
        fsidlist = [f['fs_id'] for f in file_list]
        with session.post(
            'https://pan.baidu.com/share/transfer', 
            params={
                'shareid': data['shareid'], 
                'from': data['share_uk'], 
                'sekey': unquote(session.cookies.get('BDCLND', '', domain='')), 
                'ondup': 'newcopy', 
                'async': 1, 
                'channel': 'chunlei', 
                'web': 1, 
                'app_id': 250528, 
                'bdstoken': data['bdstoken'], 
                'logid': self.logid, 
                'clienttype': 0, 
            }, 
            data=urlencode({'fsidlist': fsidlist, 'path': save_folder}), 
            headers={
                'Referer': link, 
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
            },
        ) as resp:
            resp.raise_for_status()
            msg = resp.json()
        if msg['errno'] != 0:
            raise Errno(msg)
        return msg

    def create_folder(self, path):
        '创建文件夹，形如 /a/b/c/... 这样的多级文件夹，可以一次性创建，类似 mkdir -p'
        html_content = self._fetch('GET', 'https://pan.baidu.com/disk/home')
        data = self._extract_data(html_content)
        return self._fetch_json(
            'POST', 
            'https://pan.baidu.com/api/create', 
            params={''
                'a': 'commit', 
                'channel': 'chunlei', 
                'web': 1, 
                'app_id': 250528, 
                'logid': self.logid, 
                'bdstoken': data['bdstoken'], 
                'clienttype': 0, 
            }, 
            data=urlencode({
                'path': path, 
                'isdir': 1, 
                'block_list': [], 
            }), 
            headers={
                'Referer': 'https://pan.baidu.com/disk/home?', 
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
            }, 
        )


if __name__ == '__main__':
    # [] TODO: 支持对网盘文件的增删改查
    # [] TODO: 更丰富的失败原因反馈
    # [] TODO: 如果转存大量文件发生失败，尝试分成几份后再尝试进行转存
    # [] TODO: 如果转存的目标目录不存在，先创建目录，再转存
    from argparse import ArgumentParser, RawTextHelpFormatter

    def extract_share_links(
        path, 
        _cre=re_compile('([0-9a-zA-Z]{4})[\t ]*$'),
    ):
        link_list = []
        prev_is_link = False
        with open(path) as f:
            for row in f:
                if not row.strip():
                    continue
                if 'http' in row:
                    link_info = {}
                    link_info['link'] = row[row.index('http'):].rstrip()
                    link_list.append(link_info)
                    prev_is_link = True
                    continue
                if prev_is_link:
                    match_pwd = _cre.search(row)
                    if match_pwd is not None:
                        link_info['code'] = match_pwd[1]
                prev_is_link = False
        return link_list

    ap = ArgumentParser(
        description='百度网盘文件批量转存 （如果检测到没有登录信息，会提示扫码登录）', 
        formatter_class=RawTextHelpFormatter,
    )
    ap.add_argument('-p', '--path', default=None, 
                    help='必选，存有下载链接的文本文件路径\n'
                         '1. 文本里面链接和密码不要在同一行\n'
                         '2. 文本里面可以有多余的文字，目前支持一定程度的模糊匹配\n'
                         '3. 链接所在的那一行，链接后面除了空格外不要有多余文字\n')
    ap.add_argument('-s', '--save_folder', default='/', 
                    help='可选，在百度网盘中的存储路径，默认存储在根目录')
    ap.add_argument('-c', '--cookies', default=None, 
                    help='可选，设置 Cookie')
    ap.add_argument('-e', '--errors', default='raise', 
                    choices=('raise', 'ignore'),
                    help='可选，遇到错误的处理方式：\n'
                         '    raise: 报错然后停止程序，默认；\n'
                         '    ignore: 忽略而后进行下一个')
    ap.add_argument('-H', '--header', help='可选，请求头')

    args = ap.parse_args()
    if args.path is None:
        ap.parse_args(['-h'])

    if args.header is not None:
        HEADERS = HEADERS + '\n' + args.header
    if args.cookies is not None:
        HEADERS = HEADERS + '\nCookie: ' + args.cookies

    share_links = extract_share_links(args.path)

    errors = args.errors
    pt = DuPanTransfer(headers=HEADERS)
    for share_link in share_links:
        try:
            msg = pt.transfer(**share_link, save_folder=args.save_folder)
            print('[成功]', share_link, ':', msg)
        except Exception as exc:
            if errors == 'ignore':
                print('[失败]', share_link, ':', repr(exc))
            raise