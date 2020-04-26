import time
import logging
import asyncio
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_0

IOT_ENDPOINT_URL = 'http://localhost:4589'

NUM_MESSAGES = 10
TOPIC_NAME = '/test-topic'


@asyncio.coroutine
def subscriber():
    C = MQTTClient()
    yield from C.connect(get_endpoint())
    yield from C.subscribe([(TOPIC_NAME, QOS_0)])
    try:
        for i in range(NUM_MESSAGES):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            print("%d: %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
        yield from C.unsubscribe([TOPIC_NAME])
        yield from C.disconnect()
    except ClientException as ce:
        print("Client exception: %s" % ce)


@asyncio.coroutine
def publisher():
    C = MQTTClient()
    yield from C.connect(get_endpoint())
    for i in range(NUM_MESSAGES):
        tasks = [asyncio.ensure_future(C.publish(TOPIC_NAME, ('TEST MESSAGE %s' % i).encode('utf-8')))]
        yield from asyncio.wait(tasks)
    print('%s messages published' % NUM_MESSAGES)
    yield from C.disconnect()


def get_endpoint():
    import boto3
    endpoint = boto3.client('iot', endpoint_url=IOT_ENDPOINT_URL).describe_endpoint()
    return 'mqtt://%s' % endpoint['endpointAddress']


async def run_async():
    loop = asyncio.get_event_loop()
    sub = loop.create_task(subscriber())
    pub = loop.create_task(publisher())
    await pub
    await sub


@asyncio.coroutine
def run():
    yield from run_async()


def main():
    asyncio.get_event_loop().run_until_complete(run())


if __name__ == '__main__':
    main()
