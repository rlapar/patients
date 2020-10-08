from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence
from sqlalchemy.sql import func

Base = declarative_base()

###################################
# <ASSOCIATION TABLES>

patients_diseases = Table('patients_diseases', Base.metadata,
    Column('patient_id', BigInteger, ForeignKey('patients.id'), index=True),
    Column('disease_id', BigInteger, ForeignKey('diseases.id'), index=True),
)

# </ASSOCIATION TABLES>
###################################



patients_seq = Sequence('patients_seq')


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(
        BigInteger,
        patients_seq,
        primary_key=True,
        server_default=patients_seq.next_value(),
    )
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False, index=True)
    birthday = Column(DateTime, nullable=False, index=True)
    deceased = Column(Boolean, nullable=False)

    diseases = relationship(
        'Disease', secondary=patients_diseases, back_populates='patients'
    )

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.name} {self.surname}, ' \
               f'{self.birthday}, deceased={self.deceased}>'


diseases_seq = Sequence('diseases_seq')


class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(
        BigInteger,
        diseases_seq,
        primary_key=True,
        server_default=diseases_seq.next_value(),
    )
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())
    name = Column(String, nullable=False, index=True)
    international_code = Column(String, nullable=False, index=True)

    patients = relationship(
        'Patient', secondary=patients_diseases, back_populates='diseases'
    )
