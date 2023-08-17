import gradio as gr
import pandas as pd
from src.types import TableMapping
from src.core import get_dataframes, get_table_mapping, save_csv_file, sanitize_python_output

source_df, template_df = get_dataframes()


with gr.Blocks() as demo:
    with gr.Column():
        gr.Markdown("## To begin, upload a Template CSV and a Source CSV file.")
        with gr.Row():
            gr.inputs.File(label="Template", type="file", file_count='single')
            gr.inputs.File(label="Source", type="file", file_count='single')

    with gr.Column():
        gr.Markdown("## Mapping from Source to Template")
        with gr.Row():
            table_mapping: TableMapping = get_table_mapping(source_df, template_df)
            table_mapping_df = pd.DataFrame(table_mapping.dict()['table_mappings'])
            gr.DataFrame(value=table_mapping_df)
            save_mapping_btn = gr.Button(value="Save Mapping", variant="secondary")
            save_mapping_btn.click(fn=lambda : save_csv_file(table_mapping_df, 'table_mapping'))

    with gr.Row():
        generate_code_btn = gr.Button(value="Generate Code from Mapping", variant="primary")
        # generate_code_btn.click(fn=generate_code, outputs=test)

    # with gr.Column():
    #     gr.Markdown("## Here is the code that will be used to transform the source file into the template schema:")
    #     gr.Code(language="python", value=sanitize_python_output(transform_code))

    # with gr.Row():
    #     gr.Button(value="Transform Source", variant="primary", trigger="transform_source")
    #     gr.Button(value="Save Code", variant="secondary", trigger="save_code")
    
    # with gr.Row():
    #     with gr.Column():
    #         gr.Dataframe(label='Target (template)', type='pandas', value=template_df)
    #     with gr.Column():
    #         gr.Dataframe(label='Source (transformed)', type='pandas', value=PythonAstREPLTool(locals={'source_df': table_1_df}).run(transform_code))

demo.launch()
