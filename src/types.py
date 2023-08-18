from pydantic import BaseModel, Field


class TableMappingEntry(BaseModel):
    """A single row in a table mapping. Describes how a single column in a source table maps to a single column in a target table, including any necessary transformations, and their explanations."""

    source_column_name: str = Field(
        ..., description="Name of the column in the source table."
    )
    target_column_name: str = Field(
        ...,
        description="Name of the column in the target table, to which the source column maps.",
    )
    value_transformations: str = Field(
        ...,
        description="Transformations needed make the source values match the target values. If unncecessary, write 'NO_TRANSFORM'.",
    )
    explanation: str = Field(
        ...,
        description="One-sentence explanation of this row (source-target mapping/transformation). Include any information that might be relevant to a software engineer building an ETL pipeline with this document.",
    )


class TableMapping(BaseModel):
    """A list of table mappings collectively describe how a source table should be transformed to match the schema of a target table."""

    table_mappings: list[TableMappingEntry] = Field(
        ..., description="A list of table mappings."
    )
