import logging
import time
import os
from queue import Queue

import paho.mqtt.client as mqtt_client


FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
_logger = logging.getLogger()
log_level = logging.DEBUG if os.environ.get('DEBUG') in ['1', 'true', 'True'] else logging.WARNING
_logger.setLevel(log_level)


IOT_ENDPOINT_URL = 'http://localhost:4566'

NUM_MESSAGES = 10
TOPIC_NAME = '/test-topic'

recv_queue = Queue()


def get_endpoint():
    import boto3
    endpoint = boto3.client('iot', endpoint_url=IOT_ENDPOINT_URL).describe_endpoint()
    host, port = endpoint['endpointAddress'].split(':')
    return host, int(port)


def create_subscriber():
    def _on_connect(client, *args):
        client.subscribe(TOPIC_NAME, qos=0)

    def on_message(client, userdata, message: mqtt_client.MQTTMessage):
        recv_queue.put(message)

    mqtt = mqtt_client.Client("mqtt_subscriber")
    mqtt.enable_logger(_logger)
    mqtt.on_connect = _on_connect
    mqtt.on_message = on_message
    mqtt.loop_start()
    mqtt._thread.name = 'mqtt_thread_subscriber'  # noqa
    return mqtt


def create_publisher():
    mqtt_publisher = mqtt_client.Client("mqtt_publisher")
    mqtt_publisher.enable_logger(_logger)
    mqtt_publisher.loop_start()
    mqtt_publisher._thread.name = f'mqtt_thread_publisher'  # noqa
    return mqtt_publisher


def publish_messages(endpoint_host: str, endpoint_port: int):
    publisher = create_publisher()
    publisher.connect(host=endpoint_host, port=endpoint_port)
    # sleep 2 to let broker connack
    time.sleep(2)
    for i in range(NUM_MESSAGES):
        publisher.publish(
            topic=TOPIC_NAME,
            payload=f"TEST MESSAGE {i}",
            qos=0
        )
    print(f"{NUM_MESSAGES} messages published")
    publisher.disconnect()
    publisher.loop_stop()
    return publisher


def main():
    endpoint_host, endpoint_port = get_endpoint()
    _logger.debug("Trying to connect to MQTT endpoint %s:%s", endpoint_host, endpoint_port)
    mqtt_subscriber = create_subscriber()
    mqtt_subscriber.connect(host=endpoint_host, port=endpoint_port)
    time.sleep(2)  # sleep 2 to let broker connack and suback
    publish_messages(endpoint_host, endpoint_port)
    try:
        for i in range(NUM_MESSAGES):
            message: mqtt_client.MQTTMessage = recv_queue.get(block=True, timeout=3)
            print(f"{i}: {message.topic} => {message.payload}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        _logger.exception(e)
    finally:
        mqtt_subscriber.loop_stop()


if __name__ == '__main__':
    main()
