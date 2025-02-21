import asyncio
import json
import aiofiles
import websockets

print("\n[ -kaz- ]\n\n")

socket = None
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "accept-encoding": "gzip, deflate, br, zstd",
    "origin": "chr"+"om"+"e-ex"+"te"+"ns"+"ion:/"+"/em"+"cc"+"lco"+"ag"+"lgc"+"poo"+"gnf"+"ig"+"gm"+"hnh"+"gab"+"pp"+"km",
    "cache-control": "no-cache"
}

async def safe_run(coroutine):
    try:
        await coroutine
    except:
        pass

async def read_file_async(file_path):
    try:
        async with aiofiles.open(file_path, 'r') as f:
            return json.loads(await f.read())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

async def get_access_token():
    data = await read_file_async('token.json')
    return data.get('accessToken')

async def connect_websocket(access_token):
    global socket
    if socket:
        return

    version = "v0.2"
    url = "wss://s"+"ecur"+"e.ws"+".ten"+"eo"+".p"+"ro"
    ws_url = f"{url}/websocket?accessToken={access_token}&version={version}"

    while True:
        try:
            print("Connecting...")
            socket = await websockets.connect(ws_url, extra_headers=HEADERS)
            print("Connected.")
            asyncio.ensure_future(periodic_ping())
            async for message in socket:
                data = json.loads(message)
                print("Received message:", data)
        except:
            await asyncio.sleep(1)

async def periodic_ping():
    while True:
        try:
            if socket and socket.open:
                await socket.send(json.dumps({'type': 'PING'}))
            await asyncio.sleep(5)
        except:
            break

async def main():
    while True:
        try:
            access_token = await get_access_token()
            if access_token:
                print("Using stored access token.")
                await connect_websocket(access_token)
            else:
                print("No access token found. Please add a valid token in 'token.json'.")
                break
        except (KeyboardInterrupt, SystemExit):
            print("Stopped by user.")
            break
        except:
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(safe_run(main()))
    except (KeyboardInterrupt, SystemExit):
        print("Stopped.")
