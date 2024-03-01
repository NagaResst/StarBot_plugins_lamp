from graia.ariadne import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Source, At
from graia.ariadne.message.parser.twilight import Twilight, FullMatch, UnionMatch, ResultValue, ElementMatch, WildcardMatch
from graia.ariadne.model import Member, Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from loguru import logger

from starbot.utils import config
from starbot.utils import redis
import datetime


logger.info(f"加载路灯命令模块")
prefix = config.get("COMMAND_PREFIX")
_allow_group_list = config.get("ALLOW_GROUP_USE_SLAMP")
try:
    expire_day = config.get("NOTE_EXPIRE_TIME")
    expire_time = expire_day*24*60*60
except:
    expire_time = 604800

today = datetime.date.today()

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
    logger.info(f"群[{sender.id}] 触发命令 : 路灯  {message} ")
    #
    if _allow_group_list is False or len(_allow_group_list) == 0:
        logger.warning(f"由于配置为空的问题，允许所有的群使用路灯功能")
    elif sender.id not in _allow_group_list:
        return

    operation = message.display.split(" ")[0]

    if operation == "记录" or operation == "w":
        # 去掉操作行为的tag
        message = message.display[2:]
        # 移除开头的空格
        while True:
            if message[0] == " ":
                message = message[1:]
            else:
                break
        # 组织保存数据用的键值对
        storage_key = f"StarBot:note:slamp:{sender.id}:{today}"
        storage_value = {"sender": str(member.id), "time": datetime.datetime.now().strftime('%H:%m'), "message": message}
        # 数据落盘
        await redis.rpush(storage_key, str(storage_value))
        await redis.expire(storage_key, expire_time)
        await app.send_message(sender, MessageChain(f"推送姬已经帮您记下了呢~♡"), quote=source)

    elif operation == "查看" or operation == "r":
        # TODO: 按照note_{date}读取redis数据 转换之后再进行输出
        if len(message.display) > 3:
            date = message.display.split(" ")[1]
            storage_key = f'StarBot:note:slamp:{sender.id}:{today.strftime("%Y")}-{date}'
            logger.info(f'读取群{sender.id}的路灯记录 日期为：{today.strftime("%Y")}-{date}')
            send_message = f"为您找到了{date}的路灯记录了呐 \n"
        else:
            storage_key = f"StarBot:note:slamp:{sender.id}:{today}"
            logger.info(f"读取群{sender.id}的路灯记录 日期为：{today}")
            send_message = f"为您找到了今天的路灯记录了呐 \n"

        readed_value = await redis.lrange(storage_key, 0, -1)

        if len(readed_value) != 0:
            for i in readed_value:
                record = eval(i)
                logger.info(record)
                send_message = send_message + f"{record['time']} \t {record['sender']} \t {record['message']} \n"
            await app.send_message(sender, MessageChain(f"{send_message}"), quote=source)
        else:
            await app.send_message(sender, MessageChain(f"很抱歉呢，没有查询到有人插入喔~"), quote=source)


