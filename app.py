import gradio as gr
from src.core import (
    get_table_mapping,
    transform_source,
    process_csv_text,
    generate_mapping_code,
)

MAX_ROWS = 10

import pandas as pd


def generate_step_markdown(step_number: int, subtitle: str, description: str = None):
    return gr.Markdown(f"# Step {step_number}\n\n ### {subtitle}\n{description}")


example_df = pd.read_csv("./src/data/synthetic/legal_entries_a.csv")


def load_example_template(template_df, example_df):
    return template_df.update(example_df)


# TODO: use tempfile
def export_csv(df, filename):
    df.to_csv(filename, index=False)
    return gr.File.update(value=filename, visible=True)


# TODO: use tempfile
def export_text(content, filename):
    with open(filename, "w") as f:
        f.write(content)
    return gr.File.update(value=filename, visible=True)


with gr.Blocks() as demo:
    gr.Markdown(
        "# LLM Data Mapper\n\nThis tool will help you map a source CSV to a template CSV, and then generate python code to transform the source CSV into the template CSV. You can edit all of the values, re-run the processes, and download files along the way."
    )
    # STEP 1
    generate_step_markdown(
        1,
        "Upload a Template CSV and a Source CSV.",
        "The schema will be extracted from the template file and the source file will be transformed to match the schema.",
    )
    with gr.Row():
        with gr.Column():
            upload_template_btn = gr.UploadButton(
                label="Upload Template File",
                file_types=[".csv"],
                file_count="single",
                variant="primary",
            )
            load_template_btn = gr.Button(
                value="Load Example Template File",
                variant="secondary",
            )
            template_df = gr.Dataframe(max_rows=MAX_ROWS, interactive=False)
            upload_template_btn.upload(
                fn=process_csv_text, inputs=upload_template_btn, outputs=template_df
            )
            load_template_btn.click(
                lambda _: pd.read_csv("./src/data/actual/template.csv"),
                upload_template_btn,
                template_df,
            )
        with gr.Column():
            upload_source_button = gr.UploadButton(
                label="Upload Source File",
                file_types=[".csv"],
                file_count="single",
                variant="primary",
            )
            load_source_button = gr.Button(
                value="Load Example Source File",
                variant="secondary",
            )
            source_df = gr.Dataframe(max_rows=MAX_ROWS, interactive=False)
            upload_source_button.upload(
                fn=process_csv_text, inputs=upload_source_button, outputs=source_df
            )
            load_source_button.click(
                lambda _: pd.read_csv("./src/data/actual/table_A.csv"),
                upload_source_button,
                source_df,
            )

    # STEP 2
    generate_step_markdown(
        2,
        "Generate mapping from Source to Template.",
        "Once generated, you can edit the values directly in the table below and they will be incorporated into the mapping logic.",
    )
    with gr.Row():
        generate_mapping_btn = gr.Button(value="Generate Mapping", variant="primary")
    with gr.Row():
        table_mapping_df = gr.DataFrame(max_rows=MAX_ROWS, interactive=True)
        generate_mapping_btn.click(
            fn=get_table_mapping,
            inputs=[source_df, template_df],
            outputs=[table_mapping_df],
        )

    with gr.Row():
        save_mapping_btn = gr.Button(value="Save Mapping", variant="secondary")
    with gr.Row():
        csv = gr.File(interactive=False, visible=False)
        save_mapping_btn.click(
            lambda df: export_csv(df, "source_template_mapping.csv"),
            table_mapping_df,
            csv,
        )
        mapping_file = gr.File(label="Downloaded File", visible=False)
        mapping_file.change(lambda x: x, mapping_file, table_mapping_df)

    # STEP 3
    generate_step_markdown(
        3,
        "Generate python code to transform Source to Template, using the generated mapping.",
        "Once generated, you can edit the code directly in the code block below and it will be incorporated into the transformation logic. And this is re-runnable! Update the mapping logic above to try it out.",
    )
    with gr.Row():
        generate_code_btn = gr.Button(
            value="Generate Code from Mapping", variant="primary"
        )
    with gr.Row():
        code_block = gr.Code(language="python")
        generate_code_btn.click(
            fn=generate_mapping_code, inputs=[table_mapping_df], outputs=[code_block]
        )

    with gr.Row():
        save_code_btn = gr.Button(value="Save Code", variant="secondary")
    with gr.Row():
        text = gr.File(interactive=False, visible=False)
        save_code_btn.click(
            lambda txt: export_text(txt, "transformation_code.py"), code_block, text
        )
        code_file = gr.File(label="Downloaded File", visible=False)
        code_file.change(lambda x: x, code_file, code_block)

    # STEP 4
    generate_step_markdown(
        4,
        "Transform the Source CSV into the Template CSV using the generated code.",
        "And this is re-runnable! Update the logic above to try it out.",
    )
    with gr.Row():
        transform_btn = gr.Button(value="Transform Source", variant="primary")
    with gr.Row():
        source_df_transformed = gr.Dataframe(
            label="Source (transformed)", max_rows=MAX_ROWS
        )
        transform_btn.click(
            transform_source,
            inputs=[source_df, code_block],
            outputs=[source_df_transformed],
        )

    with gr.Row():
        save_transformed_source_btn = gr.Button(
            value="Save Transformed Source", variant="secondary"
        )
    with gr.Row():
        csv = gr.File(interactive=False, visible=False)
        save_transformed_source_btn.click(
            lambda df: export_csv(df, "transformed_source.csv"),
            source_df_transformed,
            csv,
        )
        transform_file = gr.File(label="Downloaded File", visible=False)
        transform_file.change(lambda x: x, transform_file, source_df_transformed)

demo.launch()
