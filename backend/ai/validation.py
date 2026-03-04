from pydantic import BaseModel

def validate_graph_output(value: BaseModel) -> dict:
  return value.model_dump()
