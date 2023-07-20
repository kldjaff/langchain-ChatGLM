from flask import Flask
from flask_sockets import Sockets
import datetime
import argparse
import json
import time
import asyncio
from gevent import monkey; monkey.patch_all()
import gevent
import os
# import shutil
# from typing import List, Optional
# import urllib

# import nltk
from chains.local_doc_qa import LocalDocQA
from configs.model_config import (VS_ROOT_PATH, UPLOAD_ROOT_PATH, EMBEDDING_DEVICE,
                                  EMBEDDING_MODEL, NLTK_DATA_PATH,
                                  VECTOR_SEARCH_TOP_K, LLM_HISTORY_LEN, OPEN_CROSS_DOMAIN)
# import models.shared as shared
# from models.loader.args import parser
# from models.loader import LoaderCheckPoint

app = Flask(__name__)
sockets = Sockets(app)

from flask_cors import *
CORS(app, supports_credentials=True)

# @sockets.route('/local_doc_qa/stream-chat/{knowledge_base_id}')
# async def stream_chat(websocket, knowledge_base_id: str):
#     await websocket.accept()
#     turn = 1
#     while True:
#         input_json = await websocket.receive_json()
#         question, history, knowledge_base_id = input_json[""], input_json["history"], input_json["knowledge_base_id"]
#         vs_path = os.path.join(VS_ROOT_PATH, knowledge_base_id)

#         if not os.path.exists(vs_path):
#             await websocket.send_json({"error": f"Knowledge base {knowledge_base_id} not found"})
#             await websocket.close()
#             return

#         await websocket.send_json({"question": question, "turn": turn, "flag": "start"})

#         last_print_len = 0
#         # for resp, history in local_doc_qa.get_knowledge_based_answer(
#         #         query=question, vs_path=vs_path, chat_history=history, streaming=True
#         # ):
#         #     await websocket.send_text(resp["result"][last_print_len:])
#         #     last_print_len = len(resp["result"])

#         # source_documents = [
#         #     f"""出处 [{inum + 1}] {os.path.split(doc.metadata['source'])[-1]}：\n\n{doc.page_content}\n\n"""
#         #     f"""相关度：{doc.metadata['score']}\n\n"""
#         #     for inum, doc in enumerate(resp["source_documents"])
#         # ]

#         source_documents = []

#         await websocket.send_text(
#             json.dumps(
#                 {
#                     "question": question,
#                     "turn": turn,
#                     "flag": "end",
#                     "sources_documents": source_documents,
#                 },
#                 ensure_ascii=False,
#             )
#         )
#         turn += 1

@sockets.route('/echo')
def echo_socket(websocket):
    turn = 1
    while not websocket.closed:
        input_json = json.loads(websocket.receive())
        print(input_json)
        question, history, knowledge_base_id = input_json[""], input_json["history"], input_json["knowledge_base_id"]

        print(f"knowledge_base_id = {knowledge_base_id}")
        gevent.spawn(websocket.send,json.dumps({"question": question, "turn": turn, "flag": "start"}))

        source_documents = [f"{turn}"]

        gevent.spawn(websocket.send,json.dumps(
                {
                    "question": question,
                    "turn": turn,
                    "flag": "end",
                    "sources_documents": source_documents,
                },
                ensure_ascii=False,
            ))

        turn += 1
        

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    
    try:
        # global local_doc_qa

        # llm_model_ins = shared.loaderLLM()
        # llm_model_ins.set_history_len(LLM_HISTORY_LEN)

        # local_doc_qa = LocalDocQA()
        # local_doc_qa.init_cfg(
        #     llm_model=llm_model_ins,
        #     embedding_model=EMBEDDING_MODEL,
        #     embedding_device=EMBEDDING_DEVICE,
        #     top_k=VECTOR_SEARCH_TOP_K,
        # )
        server = pywsgi.WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler)
        print('server start')
        server.serve_forever()
    except Exception as e:
        print(f"e:{e}")
