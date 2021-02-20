# ZhiMsg
HomeAssistant Component for Message Platform

通用消息平台，目前支持钉钉群、小爱同学。依赖 [ZhiMi](https://github.com/Yonsm/ZhiMi)。

1. 三种使用方式：

- 调用服务，如：`zhimsh.miai`，例如我的 [automations](https://github.com/Yonsm/.homeassistant/blob/master/automations/air.yaml) 中大量使用。
- 如果配置了 `name`，会在 Home Assistant 前端界面生成一个 `input_text` 组件，可以在此输入文本。
- 可以上接 ZhiBot/dingbot 中联动，在钉钉群里配置代理机器人，并通过 @机器人 来使用。

2. 平台类型

# [dingmsg](custom_components/zhibot/dingmsg.py)

向钉钉群机器人发送消息。

# [miaimsg](custom_components/zhibot/miaimsg.py)

小爱同学 TTS 播报/执行插件。支持的命令样例如下：

```
您好，我是小爱同学
查询天气
执行关灯
静默关灯
音量40
音量70%大声说您好
```

如果是在钉钉群里输入上述命令，可以输入 `?` 和 `??` 查看帮助：

```
Get Props: ?<siid[-piid]>[,...]
           ?1,1-2,1-3,1-4,2-1,2-2,3
Set Props: ?<siid[-piid]=[#]value>[,...]
           ?2=#60,2-2=#false,3=test
Do Action: ?<siid[-piid]> <arg1> [...] 
           ?5 您好
           ?5-4 天气 #1

Call MIoT: ?<cmd=prop/get|/prop/set|action> <params>
           ?action {"did":"267090026","siid":5,"aiid":1,"in":["您好"]}

Call MiIO: ?/<uri> <data>
           ?/home/device_list {"getVirtualModel":false,"getHuamiDevices":1}

Devs List: ?list [name=full|name_keyword] [getVirtualModel=false|true] [getHuamiDevices=0|1]
           ?list 灯 true 0

MiIO Spec: ?spec [model_keyword|type_urn]
           ?spec
           ?spec speaker
           ?spec xiaomi.wifispeaker.lx04
           ?spec urn:miot-spec-v2:device:speaker:0000A015:xiaomi-lx04:1
```
