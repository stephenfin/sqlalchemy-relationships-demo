import uuid

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import schema


BASE = orm.declarative_base()


class User(BASE):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    uuid = sa.Column(sa.String(36), nullable=False)
    name = sa.Column(sa.String)

    addresses = orm.relationship(
        'Address',
        primaryjoin='User.uuid == Address.user_uuid',
        back_populates='user',
        foreign_keys='Address.user_uuid',
    )


class Address(BASE):
    __tablename__ = 'addresses'
    __tableargs__ = (
        sa.Index('addresses_user_uuid_idx', 'user_uuid'),
    )

    id = sa.Column(sa.Integer, primary_key=True)
    user_uuid = sa.Column(sa.String(36), nullable=False)

    user = orm.relationship(
        'User',
        primaryjoin='Address.user_uuid == User.uuid',
        back_populates='addresses',
        foreign_keys=user_uuid,
    )


def main():
    engine = sa.create_engine('sqlite://')
    session = orm.sessionmaker(bind=engine)()
    BASE.metadata.create_all(engine)

    user = User(name='John Doe', uuid=str(uuid.uuid4()))

    session.add(user)
    session.commit()

    address = Address(user_uuid=user.uuid)
    session.add(address)
    session.commit()

    print('# Users')
    for user in session.query(User).all():
        print(f'User: name={user.name}')
    print()

    print('# Addresses')
    for address in session.query(Address).all():
        print(f'Address: user={address.user_uuid}')
    print()

    print('# Schemas')
    print(schema.CreateTable(User.__table__))
    print(schema.CreateTable(Address.__table__))


if __name__ == '__main__':
    main()
