"""切噜语（ちぇる語, Language Cheru）转换
定义:
    W_cheru = '切' ^ `CHERU_SET`+
    切噜词均以'切'开头，可用字符集为`CHERU_SET`
    L_cheru = {W_cheru ∪ `\\W`}*
    切噜语由切噜词与标点符号连接而成
"""

import re
from nonebot import on_command
from itertools import zip_longest
import nonebot
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Adapter
from services.db_context import init, disconnect

__zx_plugin_name__ = "切噜语"
__plugin_usage__ = """
usage：
    [切噜一下] 转换为切噜语
    [切噜～♪切啰巴切拉切蹦切蹦] 切噜语翻译
""".strip()
__plugin_des__ = "切噜"
__plugin_cmd__ = ["切噜一下"]
__plugin_version__ = 0.1
__plugin_author__ = " "
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["切噜一下", "cherugo"],
}

CHERU_SET = '切卟叮咧哔唎啪啰啵嘭噜噼巴拉蹦铃'
CHERU_DIC = {c: i for i, c in enumerate(CHERU_SET)}
ENCODING = 'gb18030'
rex_split = re.compile(r'\b', re.U)
rex_word = re.compile(r'^\w+$', re.U)
rex_cheru_word: re.Pattern = re.compile(rf'切[{CHERU_SET}]+', re.U)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def word2cheru(w: str) -> str:
    c = ['切']
    for b in w.encode(ENCODING):
        c.append(CHERU_SET[b & 0xf])
        c.append(CHERU_SET[(b >> 4) & 0xf])
    return ''.join(c)


def cheru2word(c: str) -> str:
    if not c[0] == '切' or len(c) < 2:
        return c
    b = []
    for b1, b2 in grouper(c[1:], 2, '切'):
        x = CHERU_DIC.get(b2, 0)
        x = x << 4 | CHERU_DIC.get(b1, 0)
        b.append(x)
    return bytes(b).decode(ENCODING, 'replace')

def str2cheru(s: str) -> str:
    c = []
    for w in rex_split.split(str(s)):
        if rex_word.search(w):
            w = word2cheru(w)
        c.append(w)
    return ''.join(c)



def cheru2str(c: str) -> str:
    return rex_cheru_word.sub(lambda w: cheru2word(w.group()), str(c))

cherugo = on_command("cherugo", aliases={"切噜一下"}, priority=5, block=True)

cheru = on_command("cheru", aliases={"切噜～♪"}, priority=5, block=True)

@cherugo.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    s = arg.extract_plain_text().strip().split()
    if len(s) > 500:
        await cherugo.send(  '切、切噜太长切不动勒切噜噜...', at_sender=True)
        return
    msg =  '切噜～♪' + str2cheru(s)
    await cherugo.send( re.sub("['\]\[]","",msg) , at_sender=True)

@cheru.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    s = arg.extract_plain_text().strip().split()
    if len(s) > 1501:
        await cherugo.send(  '切、切噜太长切不动勒切噜噜...', at_sender=True)
        return
    msg = '的切噜噜是：\n' + cheru2str(s)
    await cherugo.send( re.sub("['\]\[]","",msg), at_sender=True)