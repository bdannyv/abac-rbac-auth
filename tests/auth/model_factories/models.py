from uuid import uuid4

import factory
from factory.alchemy import SQLAlchemyModelFactory

# Update the import as needed if your User model is in a different module.
from models.user import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(uuid4)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    is_active = True
