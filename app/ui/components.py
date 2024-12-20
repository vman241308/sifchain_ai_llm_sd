import gradio as gr
from app.utils.json_handler import get_default_json

def create_chat_column():
    #  return gr.Chatbot(
    #     value=[],
    #     height=500,
    #     container=True,
    #     elem_classes="chat-container",
    #     label="Chat with AI",
    #     avatar_images=None
    # )
    with gr.Column():
        chat = gr.Chatbot(
            value=[],
            height=500,
            container=True,
            elem_classes="chat-container",
            label="Chat with AI",
            avatar_images=None,
        )
        regenerate_btn = gr.Button("Regenerate")
    return chat, regenerate_btn

def create_json_column():
    return gr.Code(
        value=get_default_json(),
        language="json",
        interactive=True,
        lines=25,
        elem_classes="code-container",
        label="Configuration"
    ) 