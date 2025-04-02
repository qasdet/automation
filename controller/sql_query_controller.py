from sqlalchemy import delete, func, insert, select, update
from db_stuff.sqlalchmy_interactions import establish_postgresql_connection


class SQLRepository:
    @classmethod
    def insert(cls, values: int, Table):
        """Добавление записей в таблицу INSERT метод"""
        with establish_postgresql_connection() as session:
            stmt = insert(Table).values(**values).returning(Table)
            new_query = session.execute(stmt)
            session.commit()
            return new_query.scalar_one()


    @classmethod
    def get(cls, id: int, Table):
        """Получение записей из таблицы SELECT метод"""
        query = select(Table.__table__.columns).filter_by(id=id)
        with establish_postgresql_connection() as session:
            queries = session.execute(query)
            session.commit()
            return queries.mappings().one()


    @classmethod
    def list(cls, filter_by: dict, Table):
        """Получение списка всех записей из таблицы SELECT метод"""
        query = select(Table).filter_by(**filter_by)
        with establish_postgresql_connection() as session:
            queries = session.execute(query)
            session.commit()
            return queries.scalars().all()


    @classmethod
    def count(cls, Table) -> int:
        """Вывод количества списка всех записей из таблицы SELECT метод"""
        query = select(func.count(Table.id)).select_from(Table)
        with establish_postgresql_connection() as session:
            queries_cnt = session.execute(query)
            session.commit()
            return queries_cnt.scalar()


    @classmethod
    def update(cls, id: int, values: dict, Table):
        """Обновление записи из таблицы UPDATE метод"""
        stmt = update(Table).where(Table.id == id).values(**values)
        with establish_postgresql_connection() as session:
            session.execute(stmt)
            session.commit()


    @classmethod
    def finish(cls, id: int, values: dict, Table):
        stmt = update(Table).where(Table.id == id).values(**values)
        with establish_postgresql_connection() as session:
            session.execute(stmt)
            session.commit()


    @classmethod
    def delete(cls, id: int, Table):
        """Удаление записи из таблицы DELETE метод"""
        stmt = delete(Table).where(Table.id == id)
        with establish_postgresql_connection() as session:
            session.execute(stmt)
            session.commit()


    @classmethod
    def delete_all(cls, Table):
        """Удаление записей из таблицы DELETE метод"""
        stmt = delete(Table)
        with establish_postgresql_connection() as session:
            session.execute(stmt)
            session.commit()
