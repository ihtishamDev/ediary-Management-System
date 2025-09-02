from fastapi import APIRouter, Depends, HTTPException
from ..db import SessionLocal
from ..models import Entry
from ..schemas import EntryCreate, EntryOut
from ..auth import get_current_user

router = APIRouter()

@router.post('', response_model=EntryOut)
def create_entry(payload: EntryCreate, current_user =
Depends(get_current_user)):
    db = SessionLocal()
    e = Entry(owner_id=current_user.id, title=payload.title,
content=payload.content)
    db.add(e); db.commit(); db.refresh(e)
    out = EntryOut.from_orm(e)
    db.close()
    return out

@router.get('')
def list_entries(current_user = Depends(get_current_user)):
    db = SessionLocal()
    items = db.query(Entry).filter(Entry.owner_id ==
    current_user.id).order_by(Entry.created_at.desc()).all()
    db.close()
    return [EntryOut.from_orm(i) for i in items]

@router.get('/{entry_id}', response_model=EntryOut)
def get_entry(entry_id: int, current_user = Depends(get_current_user)):
    db = SessionLocal()
    e = db.query(Entry).filter(Entry.id == entry_id, Entry.owner_id ==
current_user.id).first()
    db.close()
    if not e:
        raise HTTPException(404, 'Not found')
    return EntryOut.from_orm(e)
@router.patch('/{entry_id}', response_model=EntryOut)
def update_entry(entry_id: int, payload: EntryCreate, current_user =
Depends(get_current_user)):
    db = SessionLocal()
    e = db.query(Entry).filter(Entry.id == entry_id, Entry.owner_id ==
current_user.id).first()
    if not e:
        db.close()
        raise HTTPException(404, 'Not found')
    e.title = payload.title
    e.content = payload.content
    db.add(e); db.commit(); db.refresh(e)
    out = EntryOut.from_orm(e)
    db.close()
    return out
@router.delete('/{entry_id}')
def delete_entry(entry_id: int, current_user = Depends(get_current_user)):
    db = SessionLocal()
    e = db.query(Entry).filter(Entry.id == entry_id, Entry.owner_id ==
current_user.id).first()
    if not e:
        db.close()
        raise HTTPException(404, 'Not found')
    db.delete(e); db.commit(); db.close()
    return {"msg": "deleted"}
