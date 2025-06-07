from pydantic import BaseModel, ConfigDict, field_validator
from pydantic_settings import BaseSettings

# Input Model
class Deps(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)

  image_url: str
  user_input: str

# Output Model
class Summary(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)

  caption: str
  hashtags: str

# Configuration Model
class Settings(BaseSettings):
    LLM_MODEL: str = "gpt-4.1-mini" # TODO: o4-mini
    OPENAI_API_KEY: str

    model_config = ConfigDict(
        env_file=".env",
        extra="allow",
        arbitrary_types_allowed=True,
    )
