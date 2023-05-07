from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm.session import Session

from src.database.db import get_db
from src.schemas import ContactCreate, ContactUpdate, ContactResponse, ContactBirthday
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])




@router.get("/contacts")
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = repository_contacts.get_contact(db=db, contact_id=contact_id)
    if not db_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return repository_contacts.update_contact(db=db, contact_id=contact_id, contact=contact)

@router.post("/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return repository_contacts.create_contact(db=db, contact=contact)

@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = repository_contacts.get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = repository_contacts.get_contact(db=db, contact_id=contact_id)
    if not db_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    repository_contacts.delete_contact(db=db, contact_id=contact_id)
    return db_contact




@router.post("/search", response_model=List[ContactResponse])
def search_contacts(query: str = Query(None, description="Search query"), db: Session = Depends(get_db)):
    if not query:
        return []
    contacts = repository_contacts.search_contacts(db, query)
    return contacts



@router.get("/contacts/birthdays")
def get_contacts_with_birthdays(db: Session = Depends(get_db)):
    contacts = repository_contacts.get_contacts_with_birthdays(db)
    return contacts

