import schemas.message
import util.rabbit.pusher

from fastapi import APIRouter, HTTPException
from core.config import config

message_router = APIRouter()


@message_router.post("/send", status_code=200)
def send_message(string: schemas.message.MessageCreate):
    try:
        if not string.message or not isinstance(string.message, str):
            raise HTTPException(status_code=400, detail="Invalid message format")

        util.rabbit.pusher.push_message_to_rabbit(string.message)

        return {"message": "Message sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @message_router.get("/receive", status_code=200)
# def receive_message():
#     try:
#         with util.rabbit.pusher.app.connection() as connection:
#             with connection.channel() as channel:
#                 method_frame, header_frame, body = channel.basic_get(queue=config.RABBITMQ_QUEUE)
#                 if method_frame:
#                     channel.basic_ack(delivery_tag=method_frame.delivery_tag)
#                     return {"message": body.decode()}
#                 else:
#                     return {"message": "No message in queue"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @message_router.get("/receive_all", status_code=200)
# def receive_all_messages():
#     try:
#         messages = []
#         with util.rabbit.pusher.app.connection() as connection:
#             with connection.channel() as channel:
#                 while True:
#                     method_frame, header_frame, body = channel.basic_get(queue=config.RABBITMQ_QUEUE)
#                     if method_frame:
#                         messages.append(body.decode())
#                         channel.basic_ack(delivery_tag=method_frame.delivery_tag)
#                     else:
#                         break
#         return {"messages": messages}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))