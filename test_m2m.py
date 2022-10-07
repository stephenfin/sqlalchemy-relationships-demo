import uuid

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import schema


BASE = orm.declarative_base()


association_table = sa.Table(
    'association',
    BASE.metadata,
    sa.Column('parent_uuid', sa.String(36), primary_key=True),
    sa.Column('child_uuid', sa.String(36), primary_key=True),
)


class Parent(BASE):
    __tablename__ = 'parents'
    __table_args__ = (
        sa.Index('parents_uuid_idx', 'uuid', unique=True),
    )

    id = sa.Column(sa.Integer, primary_key=True)
    uuid = sa.Column(sa.String(36), nullable=False)
    name = sa.Column(sa.String)

    children = orm.relationship(
        'Child',
        secondary='association',
        primaryjoin='Parent.uuid == association.c.parent_uuid',
        secondaryjoin='association.c.child_uuid == Child.uuid',
        back_populates='parents',
    )


class Child(BASE):
    __tablename__ = 'children'
    __table_args__ = (
        sa.Index('children_uuid_idx', 'uuid', unique=True),
    )

    id = sa.Column(sa.Integer, primary_key=True)
    uuid = sa.Column(sa.String(36), nullable=False)
    name = sa.Column(sa.String)

    parents = orm.relationship(
        'Parent',
        secondary='association',
        primaryjoin='Child.uuid == association.c.child_uuid',
        secondaryjoin='association.c.parent_uuid == Parent.uuid',
        back_populates='children',
    )


def main():
    engine = sa.create_engine('sqlite://')
    session = orm.sessionmaker(bind=engine)()
    BASE.metadata.create_all(engine)

    parent = Parent(name='John Doe', uuid=str(uuid.uuid4()))
    session.add(parent)
    session.commit()

    child = Child(name='Jimmy Doe', uuid=str(uuid.uuid4()))
    session.add(child)
    session.commit()

    parent.children.append(child)

    print('# Parents')
    for parent in session.query(Parent).all():
        children = [x.name for x in parent.children]
        print(f'Parent: name={parent.name}, children={children}')
    print()

    print('# Children')
    for child in session.query(Child).all():
        parents = [x.name for x in child.parents]
        print(f'Child: name={child.name}, parents={parents}')
    print()

    print('# Schemas')
    print(schema.CreateTable(association_table))
    print(schema.CreateTable(Parent.__table__))
    print(schema.CreateTable(Child.__table__))


if __name__ == '__main__':
    main()
