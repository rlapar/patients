import random
import string

from factory import lazy_attribute
from factory.alchemy import SQLAlchemyModelFactory
from faker import Factory
from faker.providers import BaseProvider


from patients.dbmodels import models
from patients.dbmodels.database import db_session


class CustomProvider(BaseProvider):
    @staticmethod
    def char():
        return random.choice(string.ascii_letters)

    @staticmethod
    def dict():
        return faker.pydict(10, True, 'str', 'int', 'float')

    @staticmethod
    def id():
        return random.randint(1, 10000000)

    @staticmethod
    def id_str():
        return ''.join([
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(20)
        ])

    @staticmethod
    def small_int():
        return random.randint(0, 5)

    @staticmethod
    def bool():
        return random.choice([True, False])


faker = Factory.create()
faker.add_provider(CustomProvider)

lazy = lambda call: lazy_attribute(lambda obj: call())


class Patient(SQLAlchemyModelFactory):
    class Meta:
        model = models.Patient
        sqlalchemy_session = db_session

    name = lazy(faker.name)
    surname = lazy(faker.name)
    birthday = lazy(faker.date_time_this_year)
    deceased = lazy(faker.boolean)

class Disease(SQLAlchemyModelFactory):
    class Meta:
        model = models.Disease
        sqlalchemy_session = db_session

    name = lazy(faker.word)
    international_code = lazy(faker.id_str)
