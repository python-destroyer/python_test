from aiohttp import web
import datetime
import pathlib

PORT = 8082
LOCAL_DIR = pathlib.Path(__file__).parent

async def send_file(request):

    data = await request.post()
    with open(str(LOCAL_DIR) + "/" + datetime.datetime.now().strftime("%Y-%m-%d") +'.csv', 'w') as f:
        f.write(data['file'])
        print("received")
    return web.Response(text='ok',content_type="text/html")

app = web.Application(client_max_size=1024**3)
app.router.add_post('/sendfile', send_file)

web.run_app(app,port=PORT)
