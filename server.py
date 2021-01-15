from socketgame.server import Server


server = Server(host='localhost', port=65432)


user_data = {}


@server.on_connection
async def on_connect(con):
    user_data[con.id] = {'name': f'Client#{con.id}'}
    server.send_to_all(
        'user_join',
        {
            'id': con.id,
            'message': f"{user_data[con.id]['name']} joined the chat!"
        }
    )
    print(f"Client {con.id} connected!")


@server.on_disconnect
async def on_disconnect(con):
    server.send_to_all(
        'user_leave',
        {
            'id': con.id,
            'message': f"{user_data[con.id]['name']} left the chat"
        }
    )
    del user_data[con.id]
    print(f"Client {con.id} disconnected.")


@server.on_ready
async def on_ready():
    print(f"Server ready at {server.host}:{server.port}")


@server.event(name='message')
async def on_message(con, message):
    name = user_data[con.id]['name']
    server.send_to_all(
        'message', {
            'id': con.id,
            'message': f"{name}: {message}"
        }
    )


@server.event(name='setname')
async def on_setname(con, new_name):
    old_name = user_data[con.id]['name']
    user_data[con.id]['name'] = new_name
    server.send_to_all(
        'name_change',
        {
            'id': con.id,
            'message': (
                f"{old_name} "
                f"changed names to {new_name}"
            )
        }
    )


server.run()
