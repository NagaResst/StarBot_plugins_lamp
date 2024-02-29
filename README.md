# StarBot-plugins-lamp
一个StarBot的路灯插件，服务于剪切片的dd们

## 安装本插件

进入 statbot/commands 目录后克隆代码

### 通过源码安装的 StarBot

```shell
cd statbot/commands
git clone https://github.com/NagaResst/StarBot_plugins_lamp.git
```

### 通过pip安装的 StarBot

```shell
# ubuntu 22.04
cd /usr/local/lib/python3.10/dist-packages/starbot/commands
git clone https://github.com/NagaResst/StarBot_plugins_lamp.git
```


### 启用插件
在 main.py 中加入以下配置

```
# 加载路灯模块
config.set("CUSTOM_COMMANDS_PACKAGE","starbot.commands.StarBot_plugins_lamp")
# 允许使用路灯的群号 逗号分割
config.set("ALLOW_GROUP_USE_SLAMP",[])
# 路灯记录保留的天数
config.get("NOTE_EXPIRE_TIME", 7)
```