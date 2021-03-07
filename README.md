# [https://github.com/Yonsm/ZhiMsg](https://github.com/Yonsm/ZhiMsg)

Uniform Message Platform for HomeAssistant

HomeAssisstant 通用消息平台，功能类似 HomeAssisstant 内建的 `notify`，但支持了不同的渠道，并且多了文本输入框。目前支持钉钉群、小爱同学。

## 1. 安装准备

-   **依赖**：[ZhiMi](https://github.com/Yonsm/ZhiMi)，请一并准备好，把 `zhimi` 放入 `custom_components`。

-   **安装**：把 `zhimsg` 放入 `custom_components`；也支持在 [HACS](https://hacs.xyz/) 中添加自定义库的方式安装。

## 2. 配置方法

参见 [我的 Home Assistant 配置](https://github.com/Yonsm/.homeassistant) 中 [configuration.yaml](https://github.com/Yonsm/.homeassistant/blob/main/configuration.yaml)

```
zhimi:
    username: !secret zhimi_username
    password: !secret zhimi_password

zhimsg:
  - platform: ding
    name: 钉钉信使
    token: !secret dingbot_token
    secret: !secret dingbot_secret
  - platform: miai
    name: 客厅音箱
    did: 380205692
    model: x08c
  - platform: miai
    name: 过道音箱
    did: 89463074
    model: lx01
  - platform: miai
    name: 儿童房音箱
    did: 267090026
    model: lx04
```

其中 `did` 和 `model` 可以不配置，此时要求 `name` 必须和`米家`/`小爱音箱` App 里面的名称一致。为了更快的运行速度，建议配置 `did` 和 `model`。

_如何获取小爱同学的 `did` 和 `model`？_ 参见 [MiService](https://github.com/Yonsm/MiService)

## 3. 使用方式：三种姿势

-   **调用服务**：如：`zhimsg.ding`，例如我的 [automations](https://github.com/Yonsm/.homeassistant/blob/master/automations/door.yaml) 中，入户门长时间开启会给钉钉群持续推送消息。如果一个平台有多个渠道，如上面有多个 `miai`，则会有多个服务名称生成。此时，可以单独调用特定渠道 `zhmsg.ke_ting_yin_xiang`；也可以调用 `zhimsg.miai`，使该平台下的所有渠道一起发出消息播报。

-   **文本输入框**：如果配置了 `name`，会在 Home Assistant 前端界面生成一个 `input_text` 组件，可以在此输入文本。

-   **对接钉钉群**：可以上接 [ZhiBot](https://github.com/Yonsm/ZhiBot)/[dingbot](https://github.com/Yonsm/ZhiBot/blob/main/custom_components/zhibot/dingbot.py) 中联动，在钉钉群里配置代理机器人，并通过 @机器人 来使用。_`为什么没有接微信`？因为微信不开放，需要伪造账号登录，暂时懒得搞了。_

## 4. 平台类型

_提示：如果只用了单个消息平台，可以把未使用的平台文件删除，如只用了小爱同学 TTS，可以删除掉 `dingmsg.py`。_

### 钉钉群消息 [dingmsg](https://github.com/Yonsm/ZhiMsg/blob/main/custom_components/zhimsg/dingmsg.py)

向钉钉群机器人发送消息。

### 小爱同学语音播报/执行 [miaimsg](https://github.com/Yonsm/ZhiMsg/blob/main/custom_components/zhimsg/miaimsg.py)

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
           ?action {"did":"267090026","siid":5,"aiid":1,"in":["Hello"]}

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

## 5. 参考

-   [ZhiMi](https://github.com/Yonsm/ZhiMi)
-   [ZhiBot](https://github.com/Yonsm/ZhiBot)
-   [MiService](https://github.com/Yonsm/MiService)
-   [Yonsm.NET](https://yonsm.github.io)
-   [Hassbian.com](https://bbs.hassbian.com/thread-12320-1-1.html)
-   [Yonsm's .homeassistant](https://github.com/Yonsm/.homeassistant)