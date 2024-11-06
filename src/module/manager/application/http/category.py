from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from src.app import application
from src.module.manager.domain.command.create_category import CreateCategory

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


class CreateCategoryRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str = Field(
        description="Category name",
        min_length=1,
    )


class CreateCategoryResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str


@router.post("")
async def create_category(category: CreateCategoryRequest) -> CreateCategoryResponse:
    app = application()
    bus = app.command_bus

    command = CreateCategory(category_name=category.name)
    response = await bus.exec(command)

    return CreateCategoryResponse(id=response.category_id)
