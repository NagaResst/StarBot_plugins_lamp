# StarBot-plugins-lamp
一个StarBot的路灯插件，服务于剪切片的dd们

## 安装插件
下载代码解压或者使用git克隆代码 到main.py 所在的文件夹中  
如果文件夹名称带 -main 请手动删除，确保文件夹名称为 StarBot_plugins_lamp

## 启用插件
```
# 加载路灯模块
config.set("CUSTOM_COMMANDS_PACKAGE","StarBot_plugins_lamp")
# 允许使用路灯的群号 逗号分割
config.set("ALLOW_GROUP_USE_SLAMP",[])
# 路灯记录保留的天数
config.get("NOTE_EXPIRE_TIME", 7)
```