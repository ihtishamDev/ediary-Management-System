from fastapi import APIRouter, Depends, HTTPException
from ..db import SessionLocal
from ..models import Entry,Category
from ..schemas import EntryCreate, EntryOut,categorySchema,categoryOut
from ..auth import get_current_user
from zoneinfo import ZoneInfo
from datetime import datetime
import pytz

router = APIRouter()

# ---------------- post & get Category ----------------

@router.post("/categoryName")
def category_create(payload: categorySchema , current_user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        pk_tz = pytz.timezone("Asia/Karachi")
        now_pkr = datetime.now(pk_tz)

        existing = (
            db.query(Category).filter(
                Category.owner_id == current_user.id , Category.category == payload.category ).first()
        )
        if existing:
            raise HTTPException(status_code=400 , detail="Category already exist")
        
        e = Category(
            owner_id=current_user.id,
            category=payload.category,
            status=payload.status or "active",
            created_at=now_pkr,
            updated_at=now_pkr,
        )
        db.add(e)
        db.commit()
        db.refresh(e)
        return e
        # return EntryOut.from_orm(e)
    finally:
        db.close()
    
@router.get("/getCategory")
def category_get( current_user = Depends(get_current_user)):
    db = SessionLocal()

    cat = (
        db.query(Category).filter(Category.owner_id == current_user.id).order_by(Category.created_at.desc()).all()
    )
    for c in cat:
        print("Category:", c.id, c.category, c.status, c.created_at)
    db.close()
    if not cat:
        raise HTTPException(404, "Not found")
    
    return [categoryOut.from_orm(i) for i in cat]

@router.put("/category/{category_id}")
def category_update(category_id: int, payload: categorySchema, current_user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        pk_tz = pytz.timezone("Asia/Karachi")
        now_pkr = datetime.now(pk_tz)

        cate = db.query(Category).filter(
            Category.id == category_id,
            Category.owner_id == current_user.id
        ).first()

        if not cate:
            raise HTTPException(status_code=404, detail="Category not found")

        # Update fields
        cate.category = payload.category
        cate.status = payload.status or cate.status
        cate.updated_at = now_pkr

        db.commit()
        db.refresh(cate)

        return categoryOut.from_orm(cate)
    finally:
        db.close()

@router.delete("/deletecategory/{category_id}")
def delete_category(category_id: int , current_user=Depends(get_current_user)):
    db = SessionLocal()
    e = (
        db.query(Category)
        .filter(Category.id == category_id, Category.owner_id == current_user.id)
        .first()
    )
    if not e:
        db.close()
        raise HTTPException(404, "Not found")
    db.delete(e)
    db.commit()
    db.close()
    return {"msg": "deleted"}


# @router.post("/categories")
# def add_category(category_name: str, current_user=Depends(get_current_user)):
    """
    Add a new category for the user.
    Since categories are stored in entries, we just insert a placeholder entry.
    """
    db = SessionLocal()
    try:
        pk_tz = pytz.timezone("Asia/Karachi")
        now_pkr = datetime.now(pk_tz)

        # Check if category already exists
        existing = (
            db.query(Entry)
            .filter(Entry.owner_id == current_user.id, Entry.category == category_name)
            .first()
        )
        if existing:
            db.close()
            raise HTTPException(status_code=400, detail="Category already exists")

        # Create a placeholder entry (category only)
        e = Entry(
            owner_id=current_user.id,
            title=f" {category_name}",
            category=category_name,
            content="",
            status="active",
            created_at=now_pkr,
            updated_at=now_pkr,
        )
        db.add(e)
        db.commit()
        db.refresh(e)
        return {"msg": f"Category '{category_name}' added successfully"}
    finally:
        db.close()



# ---------------- Create Entry ----------------
@router.post("/EntryData", response_model=EntryOut)
def create_entry(payload: EntryCreate, current_user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        pk_tz = pytz.timezone("Asia/Karachi")
        now_pkr = datetime.now(pk_tz)
        e = Entry(
            owner_id=current_user.id,
            title=payload.title,
            category=payload.category,
            content=payload.content,
            # status=payload.status or "active",
            created_at=now_pkr,
            updated_at=now_pkr,
        )
        db.add(e)
        db.commit()
        db.refresh(e)
        return EntryOut.from_orm(e)
    finally:
        db.close()

# ------ List Entries -----
@router.get("")
def list_entries(current_user=Depends(get_current_user)):

    db = SessionLocal()
    items = (
        db.query(Entry)
        .filter(Entry.owner_id == current_user.id)
        .order_by(Entry.created_at.desc())
        .all()
    )
    db.close()
    return [EntryOut.from_orm(i) for i in items]

# ---------------- Get Entry by ID ----------------
# @router.get("/{entry_id}", response_model=EntryOut)
# def get_entry(entry_id: int, current_user=Depends(get_current_user)):
#     db = SessionLocal()
#     e = (
#         db.query(Entry)
#         .filter(Entry.id == entry_id, Entry.owner_id == current_user.id)
#         .first()
#     )
#     db.close()
#     if not e:
#         raise HTTPException(404, "Not found")
#     return EntryOut.from_orm(e)

# ---------------- Update Entry (title/content/category/status) ----------------
@router.patch("/{entry_id}", response_model=EntryOut)
def update_entry(entry_id: int, payload: EntryCreate, current_user=Depends(get_current_user)):
    db = SessionLocal()
    e = (
        db.query(Entry)
        .filter(Entry.id == entry_id, Entry.owner_id == current_user.id)
        .first()
    )
    if not e:
        db.close()
        raise HTTPException(404, "Not found")

    # Only update fields if provided
    if payload.title is not None:
        e.title = payload.title
    if payload.content is not None:
        e.content = payload.content
    if payload.category is not None:
        e.category = payload.category
    # if payload.status is not None:   # 👈 update status too
    #     e.status = payload.status

    e.updated_at = datetime.now(ZoneInfo("Asia/Karachi"))

    db.add(e)
    db.commit()
    db.refresh(e)
    out = EntryOut.from_orm(e)
    db.close()
    return out

# ---------------- Toggle Status Endpoint ----------------
@router.patch("/{entry_id}/status", response_model=EntryOut)
def toggle_status(entry_id: int, current_user=Depends(get_current_user)):
    """Toggle active/inactive status"""
    db = SessionLocal()
    e = (
        db.query(Entry)
        .filter(Entry.id == entry_id, Entry.owner_id == current_user.id)
        .first()
    )
    if not e:
        db.close()
        raise HTTPException(404, "Not found")

    e.status = "inactive" if e.status == "active" else "active"
    e.updated_at = datetime.now(ZoneInfo("Asia/Karachi"))

    db.add(e)
    db.commit()
    db.refresh(e)
    out = EntryOut.from_orm(e)
    db.close()
    return out

# ---------------- Delete Category ----------------
@router.delete("/categories/{cat}")
def delete_category(cat: str, user=Depends(get_current_user)):
    db = SessionLocal()
    db.query(Entry).filter(
        Entry.owner_id == user.id, Entry.category == cat
    ).delete()
    db.commit()
    return {"detail": "Category deleted"}

# ---------------- Delete Entry ----------------
@router.delete("/{entry_id}")
def delete_entry(entry_id: int, current_user=Depends(get_current_user)):
    db = SessionLocal()
    e = (
        db.query(Entry)
        .filter(Entry.id == entry_id, Entry.owner_id == current_user.id)
        .first()
    )
    if not e:
        db.close()
        raise HTTPException(404, "Not found")
    db.delete(e)
    db.commit()
    db.close()
    return {"msg": "deleted"}

