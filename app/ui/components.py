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
        chat_history = gr.Chatbot(
            value=[],
            height=500,
            container=True,
            elem_classes="chat-container",
            label="Chat with AI",
            avatar_images=None,
        )
        json_generate_btn = gr.Button("Generate JSON")
    return chat_history, json_generate_btn

def create_json_column():
    with gr.Column():
        json_history = gr.Code(
            value=get_default_json(),
            language="json",
            interactive=True,
            lines=25,
            elem_classes="code-container",
            label="Configuration"
        )
        image_generate_btn = gr.Button("Generate Image")
    return json_history, image_generate_btn