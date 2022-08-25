from . import get_examples
from ..zhimi import miio_service

import logging
_LOGGER = logging.getLogger(__name__)


MODEL_SPECS = {
    # 'default': {'iid': (5,1), 'execute_iid': (5, 5), 'volume_iid': (2, 1)},

    # 已验证：lx01=小爱迷你音箱，lx5a=小爱音箱Play，lx04=小爱触屏音箱，x08c=红米小爱音箱
    # 未测试：l04m，l04n，l05c，l06a，lx05，lx06，s12，x08a
    'lx04,l04m,x08a': {'execute_iid': (5, 4)},
    'l04n,l05c': {'iid': (5, 3), 'execute_iid': (5, 4)},
    'x08c': {'iid': (3, 1), 'execute_iid': (3, 5), 'volume_iid': (4, 1)},

    # TODO: '123': {'iid': (5,3), 'execute_iid': (5, 4)}, # 未知型号，直接执行文本参数只有一个，应该不能工作，需要调整代码，但可能市面上不存在这个型号，先忽略
    # TODO：'v1,v3': # 不支持 MIoT TTS，需要引入 MiNA Service 支持，我手上没有相关设备，如果有人需要可以提出
}


def get_model_spec(model):
    if model:
        model = model.split('.')[-1]
        for k in MODEL_SPECS:
            if model in k:
                return MODEL_SPECS[k]
    return {}


class miaimsg:

    def __init__(self, hass, conf):
        self.hass = hass
        self.did = conf.get('did')
        if self.did and not isinstance(self.did, str):
            self.did = str(self.did)
        self.did2 = None
        self.name = conf.get('name')
        self.spec = get_model_spec(conf.get('model'))

    async def async_send(self, message, data):

        if not self.did:
            devs = await miio_service.device_list(self.name)
            if not devs:
                raise Exception('找不到设备：' + self.name)
            self.did = devs[0]['did']
            self.spec = get_model_spec(devs[0]['model'])

        if message.startswith('!') or message.startswith('！'):
            if len(message) == 1:
                return f"当前设备：{self.did2 or self.did}"
            devs = await miio_service.device_list(message[1:])
            if not devs:
                raise Exception('找不到设备：' + message[1:])
            self.did2 = devs[0]['did']
            return f"已切换到：{self.did2}"

        if message.startswith('?') or message.startswith('？'):
            if len(message) == 1:
                return get_examples(self.hass, 'miai')
            from miservice import miio_command
            return await miio_command(miio_service, self.did2 or self.did, message[1:])

        if message.startswith('音量'):
            pos = message.find('%')
            if pos == -1:
                volume = message[2:]
                message = None
            else:
                volume = message[2:pos]
                message = message[pos+1:].strip()
            volume_iid = self.spec.get('volume_iid', (2, 1))
            try:
                volume = int(volume)
                code = await miio_service.miot_set_prop(self.did, volume_iid, volume)
                if not message:
                    if code != 0:
                        return f"设置音量出错：{code}"
                    else:
                        raise Exception
            except:
                return f"当前音量：{await miio_service.miot_get_prop(self.did, volume_iid)}"

        if message.startswith('查询') or message.startswith('执行') or message.startswith('静默'):
            iid = self.spec.get('execute_iid', (5, 5))
            echo = 0 if message.startswith('静默') else 1
            args = [message[2:].strip(), echo]
        else:
            iid = self.spec.get('iid', (5, 1))
            args = [message]

        if not message:
            return "空谈误国，实干兴邦！"

        code = await miio_service.miot_action(self.did, iid, args)
        action = '执行' if len(args) == 2 else '播报'
        return action + ('成功' if code == 0 else '错误：' + str(code))
