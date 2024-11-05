from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/categories", tags=["category"])


# TODO: Clean up on final releases
# class CategoryResponse(BaseModel):
#     model_config = ConfigDict(frozen=True)
#     id: str
#     name: str
#
#
# class CategoryPagination(QueryParams):
#     next_token: Optional[str] = None
#
#
# @router.get("/")
# async def get_all_categories(
#     query: Annotated[CategoryPagination, Query()]
# ) -> PaginatedResponse[CategoryResponse, str]: ...


class CreateCategory(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str = Field(
        description="Category name",
        min_length=1,
    )


class CreateCategoryResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str


@router.post("/")
async def create_category(category: CreateCategory) -> CreateCategoryResponse: ...
