from . import get_examples
from ..zhimi import get_miiocom
from ..zhimi.micom.miiocmd import miio_cmd

import logging
_LOGGER = logging.getLogger(__name__)


MODEL_SPECS = {
    # 'default': {'siid': 5, 'aiid': 1, 'execute_siid': 5, 'execute_aiid': 5, 'volume_siid': 2, 'volume_piid': 1},
    'lx01': {},
    'lx5a': {},
    'lx04': {'execute_aiid': 4},
    'x08c': {'siid': 3, 'execute_siid': 3, 'volume_siid': 4},
}


class miaimsg:

    def __init__(self, hass, conf):
        self.hass = hass
        self.did = conf.get('did')
        if self.did and not isinstance(self.did, str):
            self.did = str(self.did)
        self.name = conf.get('name')
        self.spec = MODEL_SPECS[conf.get('model', 'lx01')]

    async def async_send(self, message, data):

        if not self.did:
            devs = await get_miiocom().device_list(self.name)
            for dev in devs:
                model = dev['model'].split('.')[-1]
                if model in MODEL_SPECS:
                    self.did = dev['did']
                    self.spec = MODEL_SPECS[model]
                    break
            if not self.did:
                raise Exception('已支持的音箱列表中找不到：' + self.name)

        if message.startswith('?') or message.startswith('？'):
            if message == '?' or message == '？':
                return get_examples(self.hass, 'miai')
            return await miio_cmd(get_miiocom(), self.did, message[1:])
    
        if message.startswith('音量'):
            pos = message.find('%')
            if pos == -1:
                volume = message[2:]
                message = None
            else:
                volume = message[2:pos]
                message = message[pos+1:].strip()
            siid = self.spec.get('volume_siid', 2)
            piid = self.spec.get('volume_piid', 1)
            try:
                volume = int(volume)
                code = await get_miiocom().miot_set_prop(self.did, siid, piid, volume)
                if not message:
                    if code != 0:
                        return f"设置音量出错：{code}"
                    else:
                        raise Exception
            except:
                return f"当前音量：{await get_miiocom().miot_get_prop(self.did, siid, piid)}"

        if message.startswith('查询') or message.startswith('执行') or message.startswith('静默'):
            siid = self.spec.get('execute_siid', 5)
            aiid = self.spec.get('execute_aiid', 5)
            echo = 0 if message.startswith('静默') else 1
            args = [message[2:].strip(), echo]
        else:
            siid = self.spec.get('siid', 5)
            aiid = self.spec.get('aiid', 1)
            args = [message]

        if not message:
            return "空谈误国，实干兴邦！"

        result = await get_miiocom().miot_action(self.did, siid, aiid, args)
        return (('执行' if len(args) == 2 else '播报') + '成功') if result.get('code') == 0 else result
