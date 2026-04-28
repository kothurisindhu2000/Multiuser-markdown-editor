import asyncio
import json
import websockets

connected_users = set()
operations = {}  # CRDT-style storage: id -> operation


def build_document():
    sorted_ops = sorted(operations.values(), key=lambda op: op["timestamp"])
    return "\n".join(f'{op["user"]}: {op["text"]}' for op in sorted_ops) + ("\n" if sorted_ops else "")


async def send_document_to_all():
    document = build_document()

    for user in connected_users.copy():
        try:
            await user.send(document)
        except:
            connected_users.remove(user)


async def handle_client(websocket):
    connected_users.add(websocket)
    print("New user connected")

    await websocket.send(build_document())

    try:
        async for message in websocket:
            operation = json.loads(message)

            op_id = operation["id"]

            # CRDT-style merge: ignore duplicate operation IDs
            if op_id not in operations:
                operations[op_id] = operation
                print("Received:", operation)

            await send_document_to_all()

    except:
        print("User disconnected")

    finally:
        connected_users.remove(websocket)


async def main():
    print("Server started on ws://localhost:8765")
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()


asyncio.run(main())