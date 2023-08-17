import os
from dotenv import load_dotenv
import pandas as pd
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.tools import PythonAstREPLTool
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.chat_models import ChatOpenAI
from src.types import TableMapping
from src.vars import NUM_ROWS_TO_RETURN
from src.prompt import DATA_SCIENTIST_PROMPT_STR, SPEC_WRITER_PROMPT_STR, ENGINEER_PROMPT_STR

load_dotenv()

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), 'data')
SYNTHETIC_DATA_DIR_PATH = os.path.join(DATA_DIR_PATH, 'synthetic')

TRANSFORM_MODEL = ChatOpenAI(
    model_name='gpt-4',
    temperature=0,
)

NATURAL_LANGUAGE_MODEL = ChatOpenAI(
    model_name='gpt-4',
    temperature=0.1,
)

def get_dataframes():
    source = pd.read_csv(os.path.join(SYNTHETIC_DATA_DIR_PATH, 'legal_entries_a.csv'))
    template = pd.read_csv(os.path.join(SYNTHETIC_DATA_DIR_PATH, 'legal_template.csv'))
    return source, template

def get_data_str_from_df_for_prompt(df, num_rows_to_return=NUM_ROWS_TO_RETURN):
    return f'<df>\n{df.head(num_rows_to_return).to_markdown()}\n</df>'

def get_table_mapping(source_df, template_df) -> TableMapping:
    table_mapping_parser = PydanticOutputParser(pydantic_object=TableMapping)
    analyst_prompt = ChatPromptTemplate.from_template(
        template=DATA_SCIENTIST_PROMPT_STR, 
        partial_variables={'format_instructions': table_mapping_parser.get_format_instructions()},
    )

    mapping_chain = analyst_prompt | TRANSFORM_MODEL | table_mapping_parser
    return mapping_chain.invoke({"source_1_csv_str": get_data_str_from_df_for_prompt(source_df), "target_csv_str": get_data_str_from_df_for_prompt(template_df)})


def get_code_spec(table_mapping: TableMapping) -> str:
    writer_prompt = ChatPromptTemplate.from_template(SPEC_WRITER_PROMPT_STR)
    writer_chain = writer_prompt | NATURAL_LANGUAGE_MODEL | StrOutputParser()
    return writer_chain.invoke({"table_mapping": str(table_mapping)})


def get_mapping_code(spec_str: str) -> str:
    engineer_prompt = ChatPromptTemplate.from_template(ENGINEER_PROMPT_STR)
    engineer_chain = engineer_prompt | TRANSFORM_MODEL | StrOutputParser()
    return engineer_chain.invoke({"spec_str": spec_str})


def sanitize_python_output(text: str):
    _, after = text.split("```python")
    return after.split("```")[0]

def save_csv_file(df, filename):
    df.to_csv(os.path.join(DATA_DIR_PATH, 'output', filename) + '.csv')
