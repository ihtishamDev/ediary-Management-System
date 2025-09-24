# from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
# from fastapi.responses import FileResponse
# from ..db import SessionLocal
# from ..models import Attachment, Entry
# from ..auth import get_current_user
# import os, uuid

# router = APIRouter()

# UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
# 'uploads'))
# os.makedirs(UPLOAD_DIR, exist_ok=True)
# @router.post('/upload')

# def upload(entry_id: int = Form(...), file: UploadFile = File(...),
# current_user=Depends(get_current_user)):
#     db = SessionLocal()
#     entry = db.query(Entry).filter(Entry.id == entry_id, Entry.owner_isd ==
# current_user.id).first()
#     if not entry:
#         db.close()
#         raise HTTPException(404, 'Entry not found or not owned')
#     ext = os.path.splitext(file.filename)[1]
#     stored_name = f"{uuid.uuid4().hex}{ext}"
#     path = os.path.join(UPLOAD_DIR, stored_name)
#     with open(path, 'wb') as f:
#         f.write(file.file.read())
#     att = Attachment(entry_id=entry.id, filename=file.filename,
# stored_name=stored_name, mime_type=file.content_type,
# size=os.path.getsize(path))
#     db.add(att); db.commit(); db.refresh(att)
#     out = {"id": att.id, "filename": att.filename}
#     db.close()
#     return out

# @router.get('/{attachment_id}')
# def get_attachment(attachment_id: int, current_user=Depends(get_current_user)):
#     db = SessionLocal()
#     att = db.query(Attachment).filter(Attachment.id == attachment_id).first()
#     if not att:
#         db.close()
#         raise HTTPException(404, 'not found')
#     # verify ownership via entry -> owner
#     entry = db.query(Entry).filter(Entry.id == att.entry_id).first()
#     if entry.owner_id != current_user.id:
#         db.close()
#         raise HTTPException(403, 'forbidden')
#     path = os.path.join(UPLOAD_DIR, att.stored_name)
#     db.close()
#     if not os.path.exists(path):
#         raise HTTPException(404, 'file not found on disk')
#     return FileResponse(path, filename=att.filename, media_type=att.mime_type)