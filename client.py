import asyncio
from concurrent.futures import ThreadPoolExecutor
from socketgame.client import Client


client = Client(host='localhost', port=65432)

name = input("Username: ")


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


async def ainput(prompt: str = "") -> str:
    with ThreadPoolExecutor(1, "AsyncInput") as executor:
        return await asyncio.get_event_loop().run_in_executor(
            executor, input, prompt)


@client.event(name='message')
async def on_message(con, data):
    if data['id'] == client.id:
        return
    print(data['message'])


@client.event(name='user_join')
async def on_user_join(con, data):
    if data['id'] == client.id:
        return
    print(colored(0, 255, 0, data['message']))


@client.event(name='user_leave')
async def on_user_leave(con, data):
    if data['id'] == client.id:
        return
    print(colored(255, 0, 0, data['message']))


@client.event(name='name_change')
async def on_name_change(con, data):
    if data['id'] == client.id:
        return
    print(colored(0, 0, 255, data['message']))


@client.task
async def send_messages():
    print(colored(255, 255, 255, 'Connected!'))
    client.send('setname', name)
    while True:
        to_send = await ainput("")
        client.send('message', to_send)
        await asyncio.sleep(0.5)


client.run()
