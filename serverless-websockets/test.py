import json
import boto3
import asyncio
import websockets
from six.moves.queue import Queue
from localstack.config import TEST_APIGATEWAYV2_URL


def test_websocket_api():
    client = boto3.client('apigatewayv2', endpoint_url=TEST_APIGATEWAYV2_URL)
    queue = Queue()
    msg = {'action': 'test-action'}

    async def start_client(uri):
        async with websockets.connect(uri) as websocket:
            print('Sending message to websocket')
            await websocket.send(json.dumps(msg))
            result = await websocket.recv()
            print('Received message from websocket: %s' % result)
            queue.put(json.loads(result))

    apis = client.get_apis()['Items']
    api = [a for a in apis if 'localstack-websockets' in a['Name']][0]

    url = api['ApiEndpoint']
    asyncio.get_event_loop().run_until_complete(start_client(url))
    result = queue.get(timeout=3)

    assert result == msg


def main():
    test_websocket_api()


if __name__ == '__main__':
    main()
