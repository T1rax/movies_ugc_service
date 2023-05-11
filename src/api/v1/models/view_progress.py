from pydantic import BaseModel, StrictInt


class SaveViewProgressInput(BaseModel):
    viewed_frame: StrictInt
