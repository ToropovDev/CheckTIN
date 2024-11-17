from pydantic import BaseModel


class OfdDAta(BaseModel):
    mode: str = "quick"
    page: str = ""
    query: int
    pageSize: int = 10
    sortField: str = "NAME_EX"
    sort: str = "ASC"


class OfdSubject(BaseModel):
    class Config:
        extra = "ignore"

    ogrn: int
    inn: int
    regioncode: int
    dtregistry: str
    is_active: bool
    nptype: str
    name_ex: str
