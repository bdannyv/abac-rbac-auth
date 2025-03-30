import uuid

import pytest
from features.authentication.api.v1.schemas import SignUpFormModel
from features.authentication.exc import EmailAlreadyExists, UnknownUserColumn
from features.authentication.repos.user import UserRepository
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def test_user_create_command(db_session: AsyncSession, user_create_form: SignUpFormModel):
    new_user_id = await UserRepository.create(session=db_session, user_data=user_create_form)
    assert new_user_id == user_create_form.id


async def test_create_user_with_existing_email(db_session: AsyncSession, user_create_form: SignUpFormModel):
    await UserRepository.create(session=db_session, user_data=user_create_form)
    with pytest.raises(EmailAlreadyExists):
        await UserRepository.create(session=db_session, user_data=user_create_form)


async def test_user_update_command(db_session: AsyncSession, user_record, user_create_form: SignUpFormModel):
    user_data = user_create_form.model_dump(exclude={"id"})
    for column, value in user_data.items():
        assert getattr(user_record, column) != value

    await UserRepository.update(id_=user_record.id, session=db_session, user_data=user_data)
    await db_session.commit()

    upd_user_record = await db_session.get(User, user_record.id)
    for column, value in user_data.items():
        assert getattr(upd_user_record, column) == value


async def test_unknown_user_update_command(db_session: AsyncSession, user_record, user_create_form: SignUpFormModel):
    user_data = user_create_form.model_dump(exclude={"id"})
    for column, value in user_data.items():
        assert getattr(user_record, column) != value

    new_id = await UserRepository.update(id_=user_create_form.id, session=db_session, user_data=user_data)
    await db_session.commit()

    assert new_id is None


async def test_user_update_command_unknown_column(
    db_session: AsyncSession, user_record, user_create_form: SignUpFormModel
):
    user_data = user_create_form.model_dump(exclude={"id"})
    for column, value in user_data.items():
        assert getattr(user_record, column) != value

    user_data.update({"random_col": "random_value"})
    with pytest.raises(UnknownUserColumn):
        await UserRepository.update(id_=user_create_form.id, session=db_session, user_data=user_data)


async def test_user_delete_command(db_session: AsyncSession, user_record: User):
    deleted_id = await UserRepository.delete(id_=user_record.id, session=db_session)
    await db_session.commit()

    deleted_user = await db_session.get(User, user_record.id)
    assert deleted_user is None
    assert deleted_id == user_record.id


async def test_unknown_user_delete_command(db_session: AsyncSession, user_record: User):
    deleted_id = await UserRepository.delete(uuid.uuid4(), db_session)
    await db_session.commit()

    assert deleted_id is None
    await db_session.refresh(user_record)


async def test_repo_get_by_email(db_session: AsyncSession, user_record: User):
    user = await UserRepository.get_by_email(email=user_record.email, session=db_session)
    assert user.id == user_record.id


async def test_repo_get_by_unknown_email(db_session: AsyncSession, user_record: User):
    user = await UserRepository.get_by_email(email=user_record.email + "postfix", session=db_session)
    assert user is None
