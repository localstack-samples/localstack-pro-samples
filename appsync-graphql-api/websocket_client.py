import os
import sys
import boto3
import asyncio
import requests
import websockets

# initialize globals
os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
URL_APPSYNC = 'http://localhost:4566'


def subscribe_websocket(api_id):
    # get AppSync websocket URL
    appsync = boto3.client('appsync', endpoint_url=URL_APPSYNC)
    result = appsync.get_graphql_api(apiId=api_id)
    api_url = result['graphqlApi']['uris'].get('GRAPHQL')
    ws_url = result['graphqlApi']['uris'].get('REALTIME')

    async def start_client(uri, msg):
        async with websockets.connect(uri) as websocket:
            await websocket.send(msg)
            result = await websocket.recv()
            print('Received notification message from WebSocket: %s' % result)
            os._exit(0)

    # Fix to initialize Websocket (fixes a bug in Mac OS)
    requests.get(ws_url.replace('ws://', 'http://'))

    # start subscription client
    subscribe_message = 'subscription mySub {addedPost {id}}'
    event_loop = asyncio.get_event_loop()
    print('Connecting to WebSocket URL', ws_url)
    event_loop.create_task(start_client(ws_url, subscribe_message))
    event_loop.run_forever()


def main():
    try:
      subscribe_websocket(sys.argv[1])
    except websockets.exceptions.ConnectionClosedOK as e:
      print(f"WebSocket connection terminated")

if __name__ == '__main__':
    main()
