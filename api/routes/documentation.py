import data.documentation as data
import data.applications as app_data

from fastapi import APIRouter, Depends, HTTPException, Path, status
from models import User, Documentation, DocumentationReturn, Message
from dependencies import current_user_is_active

from constants import OWNER_KEY

router = APIRouter(
    prefix="/documentation",
    tags=["documentation"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{documentation}", response_model=DocumentationReturn)
async def read_documentation_by_id(
    documentation: int = Path(..., description="Documentation ID")
):
    doc = data.get_documentation_by_id(documentation)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return doc


@router.get("/app/{application}", response_model=DocumentationReturn)
async def read_documentation_by_app_id(
    application: int = Path(..., description="Application ID")
):
    doc = data.get_documentation_by_app_id(application)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return doc


@router.post("/{application}", response_model=DocumentationReturn)
async def add_update_documentation(
    doc: Documentation,
    current_user: User = Depends(current_user_is_active),
    application: int = Path(..., description="Application ID"),
):
    if doc.documentation:
        app = app_data.get_application_by_id(application)
        if app[OWNER_KEY]["id"] == current_user["id"]:
            data.add_documentation(
                application,
                doc.external,
                doc.documentation,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Not allowed"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required fields"
        )
    return_doc = data.get_documentation_by_app_id(application)
    if not return_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found, failed to add",
        )
    return return_doc


@router.delete("/{documentation}", response_model=Message)
async def delete_documentation(
    documentation: int = Path(..., description="Documentation ID"),
    current_user: User = Depends(current_user_is_active),
):
    app_id = data.get_documentation_by_id(documentation)[APPLICATION_KEY]
    app = app_data.get_application_by_id(app_id)
    if app[OWNER_KEY]["id"] == current_user["id"]:
        data.remove_documentation(documentation)
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Not allowed"
        )
    if data.get_documentation_by_id(documentation):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Failed to delete"
        )
    return {"msg": "deleted"}