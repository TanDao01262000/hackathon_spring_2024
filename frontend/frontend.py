import gradio as gr

from loguru import logger
from typing import Optional, List
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

load_dotenv()


class Message(BaseModel):
    role: str
    content: str


async def make_backend_request(messages: List[Message]) -> Optional[str]:
    query = messages[-1]
    url = f"https://hound-measured-colt.ngrok-free.app/api?query={query['content']}"
    logger.debug(f"Backend Query: {url}")
    response = requests.get(url)
    return response.json()


async def completion(input, history):
    history.append({"role": "user", "content": input})
    response = await make_backend_request(history)
    # logger.info(response)
    history.append({"role": "assistant", "content": response})
    messages = [
        (history[i]["content"], history[i + 1]["content"])
        for i in range(0, len(history) - 1, 2)
    ]
    return "", messages, history


with gr.Blocks() as demo:
    logger.info("Starting hackathon demo...")
    chatbot = gr.Chatbot(label="Tan, Quyen, and Nhu Hackathon")
    history = gr.State([])
    with gr.Row():
        txt = gr.Textbox(
            show_label=False, placeholder="Enter a question and press enter"
        ).style(container=False)
    txt.submit(completion, [txt, history], [txt, chatbot, history])

demo.launch(server_port=8081)
