from pydantic import BaseModel

class Article(BaseModel):
    id: int
    title_area: str
    price_area: str
    information_area: str
    tag_area: str
    merit_area: str
    full_url: str
    article_number: str

    class Config:
        orm_mode = True