from datetime import datetime, timedelta

from sqlalchemy import select, and_, cast, DATE, func, Date
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    statmnt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(statmnt)
    return contacts.scalars().all()


async def search_contacts(query, db: AsyncSession, user: User):
    statmnt = select(Contact).filter_by(user=user).filter((Contact.firstname.ilike(query))
                                     | (Contact.surname.ilike(query))
                                     | (Contact.email.ilike(query)))
    results = await db.execute(statmnt)
    return results.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    statmnt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(statmnt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession, user: User):
    statmnt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(statmnt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.firstname = body.firstname
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.details = body.details
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    statmnt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(statmnt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact



async def get_upcoming_birthdays(db: AsyncSession, user: User):
    today = datetime.now().date()
    week_from_today = today + timedelta(days=7)
    statmnt = select(Contact).filter_by(user=user).filter(
        and_(
            cast(Contact.birthday, Date) >= today,
            cast(Contact.birthday, Date) <= week_from_today
        )
    )
    contacts = await db.execute(statmnt)
    return contacts.scalars().all()