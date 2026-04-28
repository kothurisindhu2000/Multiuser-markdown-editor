import asyncio
import json
import os
import time
import uuid
import websockets

DOCUMENT_FILE = "document.md"
QUEUE_FILE = "queue.json"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def save_document(content):
    with open(DOCUMENT_FILE, "w", encoding="utf-8") as file:
        file.write(content)


def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []

    with open(QUEUE_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except:
            return []


def save_queue(queue):
    with open(QUEUE_FILE, "w", encoding="utf-8") as file:
        json.dump(queue, file, indent=2)


def create_operation(username, text):
    return {
        "id": str(uuid.uuid4()),
        "user": username,
        "text": text,
        "timestamp": time.time()
    }


async def send_offline_queue(websocket):
    queue = load_queue()

    if not queue:
        return

    print(f"Sending {len(queue)} offline saved changes...")

    for operation in queue:
        await websocket.send(json.dumps(operation))

    save_queue([])


async def send_message(websocket, username):
    while True:
        message = await asyncio.to_thread(input)

        operation = create_operation(username, message)

        try:
            await websocket.send(json.dumps(operation))
        except:
            queue = load_queue()
            queue.append(operation)
            save_queue(queue)
            print("Offline: saved change to queue.json")


async def receive_message(websocket):
    while True:
        try:
            document = await websocket.recv()

            save_document(document)

            clear_screen()
            print("=== Shared Markdown Document ===\n")
            print(document)
            print("\nType below:\n")

        except:
            break


async def main():
    username = input("Enter your name: ")

    try:
        async with websockets.connect("ws://localhost:8765") as websocket:
            clear_screen()
            print(f"Connected as {username}\n")

            await send_offline_queue(websocket)

            await asyncio.gather(
                send_message(websocket, username),
                receive_message(websocket)
            )

    except:
        print("Server is offline.")
        print("Start server.py first, then run main.py again.")


asyncio.run(main())