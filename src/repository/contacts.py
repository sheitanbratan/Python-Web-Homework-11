from typing import Type
from datetime import datetime, date, timedelta

from sqlalchemy import and_, extract
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, UpdateContact


async def get_contacts(skip: int, limit: int, db: Session) -> list[Type[Contact]]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Type[Contact] | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(
        name=body.name,
        surname=body.surname,
        email=body.email,
        phone=body.phone,
        birthday=body.birthday,
        additional_info=body.additional_info
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: UpdateContact, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_by_name(contact_name: str, db: Session) -> list[Type[Contact]]:
    return db.query(Contact).filter(Contact.name == contact_name).all()


async def search_by_surname(contact_surname: str, db: Session) -> list[Type[Contact]]:
    return db.query(Contact).filter(Contact.surname == contact_surname).all()


async def search_by_email(contact_email: str, db: Session) -> list[Type[Contact]]:
    return db.query(Contact).filter(Contact.email == contact_email).all()


async def upcoming_birthdays(db: Session) -> list[Type[Contact]]:
    today = datetime.today()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).filter(and_(extract('day', Contact.birthday) >= today.day,
                                             extract('day', Contact.birthday) <= next_week.day,
                                             extract('month', Contact.birthday) == today.month)).all()
    return contacts





