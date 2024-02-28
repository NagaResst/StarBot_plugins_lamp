from graia.ariadne import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Source, At
from graia.ariadne.message.parser.twilight import Twilight, FullMatch, UnionMatch, ResultValue, ElementMatch, WildcardMatch
from graia.ariadne.model import Member, Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from loguru import logger

from ...utils import config

logger.info(f"加载路灯命令模块")
prefix = config.get("COMMAND_PREFIX")
_allow_group_list = config.get("ALLOW_GROUP_USE_SLAMP")

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight(
            ElementMatch(At, optional=True),
            FullMatch(prefix),
            UnionMatch("路灯", "slamp"),
            "message" @ WildcardMatch()
        )],
    )
)
async def slamp_record(app: Ariadne, source: Source, sender: Group, member: Member, message: MessageChain = ResultValue()):
    logger.info(f"群[{sender.id}] 触发命令 : 路灯  {message} {type(message.display)} ")

    if _allow_group_list is False or len(_allow_group_list) == 0:
        logger.warning(f"由于配置为空的问题，允许所有的群使用路灯功能")
    elif sender.id not in _allow_group_list:
        return

    operation = message.display.split(" ")[0]

    if operation == "记录" or operation == "w":
        # TODO: 写入数据到redis 以note_slamp_{date} 为key  sender.id和message为值
        message = message.display.split(" ")[1]
        await app.send_message(sender, MessageChain(f"已经调用写入数据功能,获取到数据{message}"), quote=source)
    elif operation == "查看" or operation == "r":
        # TODO: 按照note_{date}读取redis数据 转换之后再进行输出
        await app.send_message(sender, MessageChain(f"已经调用读取数据功能"), quote=source)
