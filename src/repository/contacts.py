from typing import List
from datetime import datetime, date, timedelta
import re

from sqlalchemy.orm import Session

from sqlalchemy import or_, extract
from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate, ContactBirthday


def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact: ContactUpdate) -> Contact:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise ValueError("Contact not found")
    for field, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int) -> Contact:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise ValueError("Contact not found")
    db.delete(db_contact)
    db.commit()
    return db_contact


def search_contacts(db: Session, query: str) -> List[Contact]:
    if not query:
        return []
    return db.query(Contact).filter(or_(
        Contact.first_name.ilike(f"%{query}%"),
        Contact.last_name.ilike(f"%{query}%"),
        Contact.email.ilike(f"%{query}%"),
    )).all()


def get_contacts_with_birthdays(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(extract('month', Contact.birthday) == today.month,
                                      extract('day', Contact.birthday) >= today.day,
                                      extract('day', Contact.birthday) <= next_week.day).all()
    return contacts
