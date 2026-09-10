from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from .cv_schema import CVCreate, CVOut
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .cv_model import CV
from auth.dependencies import get_current_user
from auth.auth_models import User
import pymupdf, pymupdf4llm

router = APIRouter(prefix ="/cv", tags=["cv"])


@router.post("/upload", response_model=CVOut)
async def upload_cv(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db) ):
   is_pdf_by_name = file.filename is not None and file.filename.endswith(".pdf")
   is_pdf_by_type = file.content_type == "application/pdf"

   if not (is_pdf_by_name or is_pdf_by_type):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed")
   
   contents = await file.read()
   doc = pymupdf.open(stream=contents, filetype="pdf")

   md_text = pymupdf4llm.to_markdown(doc)

   new_cv = CV(user_id=current_user.id,
    filename=file.filename,
    content=md_text)

   db.add(new_cv)
   await db.commit()
   await db.refresh(new_cv)
   return new_cv



@router.get("/", response_model=list[CVOut])
async def get_cvs (current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    stmt = select (CV).where(CV.user_id == current_user.id)
    result = await db.execute(stmt)
    cvs= result.scalars().all()

    return cvs

@router.get("/{cv_id}", response_model = CVOut)
async def get_one (cv_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    stmt = select(CV).where(CV.user_id == current_user.id, CV.id == cv_id)
    result = await db.execute(stmt)
    cv = result.scalar_one_or_none()

    if cv is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV not found")

    return cv


@router.delete("/{cv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv (cv_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    stmt = select(CV).where(CV.user_id == current_user.id, CV.id == cv_id)
    result = await db.execute(stmt)
    cv = result.scalar_one_or_none()

    if cv is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "CV not found")
    

    await db.delete(cv)
    await db.commit()



