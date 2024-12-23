import gradio as gr
from app.ui.components import create_chat_column, create_json_column
from app.ui.styles import custom_css
from app.core.processor import process_input, process_json

def create_ui():
    with gr.Blocks(theme=gr.themes.Default(), css=custom_css) as interface:
        with gr.Row():
            chat_component, json_generate_btn = create_chat_column()
            json_component, image_generate_btn = create_json_column()

        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    label="Enter new text here",
                    placeholder="Type your message...",
                    lines=3
                )
                file_upload = gr.File(label="Upload File")
                submit_btn = gr.Button("Submit")


        submit_btn.click(
            fn=process_input,
            inputs=[input_text, file_upload],
            outputs=[chat_component]
        )

        json_generate_btn.click(
            fn=process_json,
            outputs=[json_component]
        )

    return interface 