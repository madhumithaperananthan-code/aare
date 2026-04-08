from pydantic import BaseModel


class AAREAction(BaseModel):
    action_type: str