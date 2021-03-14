import voluptuous as vol
from random import randint
from importlib import import_module
import homeassistant.helpers.config_validation as cv
from homeassistant.util import slugify
from homeassistant.util.yaml import load_yaml
from homeassistant.components.input_text import (InputText, CONF_MIN, CONF_MIN_VALUE, CONF_MAX, CONF_MAX_VALUE, CONF_INITIAL, MODE_TEXT, SERVICE_SET_VALUE, ATTR_VALUE)
from homeassistant.const import (CONF_ID, CONF_NAME, CONF_ICON, CONF_MODE)

import logging
_LOGGER = logging.getLogger(__name__)

DOMAIN = 'zhimsg'
SERVICES = {}

SERVICE_SCHEMA = vol.Schema({
    vol.Required('message'): cv.string,
})


def load_desc(hass):
    return load_yaml(hass.config.path(f'custom_components/{DOMAIN}/services.yaml'))


def get_example(desc, platform):
    return desc.get(platform, {}).get('fields', {}).get('message', {}).get('example', '您好')


def get_examples(hass, platform):
    return get_example(load_desc(hass), platform).replace('|', '\n')


async def async_setup(hass, config):
    global SERVICES
    entities = []
    Classes = {}
    desc = load_desc(hass)
    for conf in config.get(DOMAIN):
        service = conf['platform']
        platform = service.split('_')[0]
        Class = Classes.get(platform)
        if Class is None:
            module = import_module('.' + platform, __package__)
            Class = getattr(module, platform + 'msg')
            Classes[platform] = Class
            SERVICES[platform] = []
            hass.services.async_register(DOMAIN, platform, async_call, schema=SERVICE_SCHEMA)
            _LOGGER.debug("Platform Service as %s.%s", DOMAIN, platform)
        instance = Class(hass, conf)
        SERVICES[platform].append(instance)

        name = conf.get('name')
        if name:
            service = slugify(name)
            examples = get_example(desc, platform).split('|')
            initial_text = examples[randint(0, len(examples) - 1)]
            entities.append(create_input_entity(hass, name, service, initial_text))
        if service not in SERVICES:
            SERVICES[service] = instance
            _LOGGER.debug("Service as %s.%s", DOMAIN, service)
            hass.services.async_register(DOMAIN, service, async_call, schema=SERVICE_SCHEMA)

    if len(entities):
        await async_add_input_entities(hass, entities)
    return True


async def async_call(call):
    data = call.data
    message = data.get('message')
    await async_send(call.service, message, data)


async def async_send(service, message, data={}):
    instance = SERVICES[service]
    if isinstance(instance, list):
        result = None
        for inst in instance:
            ret = await inst.async_send(message, data)
            if ret:
                result = ret
        return result
    return await instance.async_send(message, data)


def create_input_entity(hass, name, service, initial_text):
    config = {
        CONF_ID: service,
        CONF_NAME: name,
        CONF_MIN: CONF_MIN_VALUE,
        CONF_MAX: CONF_MAX_VALUE,
        CONF_INITIAL: initial_text,
        CONF_ICON: 'mdi:account-tie-voice',
        CONF_MODE: MODE_TEXT
    }
    entity = InputText(config)
    entity.entity_id = f"input_text.{service}"
    #entity.editable = False
    return entity


async def async_input_changed(event):
    data = event.data
    old_state = data.get('old_state')
    new_state = data.get('new_state')
    _LOGGER.error('HAHA: %s!!!', new_state.entity_id)
    if old_state and new_state:
        message = new_state.state
        if message != old_state.state:
            entity_id = data['entity_id']
            service = entity_id[entity_id.find('.') + 1:]
            await async_send(service, message)


async def async_add_input_entities(hass, entities):
    from homeassistant.helpers.entity_component import EntityComponent
    component = hass.data.get('entity_components', {}).get('input_text')
    if component is None:
        component = EntityComponent(_LOGGER, 'input_text', hass)
        component.async_register_entity_service(SERVICE_SET_VALUE, {vol.Required(ATTR_VALUE): cv.string}, 'async_set_value')
    await component.async_add_entities(entities)
    hass.helpers.event.async_track_state_change_event([entity.entity_id for entity in entities], async_input_changed)
