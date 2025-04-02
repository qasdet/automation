from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from gitlab_conf import ENV_VARIABLES

Base = declarative_base()


def establish_postgresql_connection():
    """Подключение к основной БД приложения"""
    return postgresql_connect(
        ENV_VARIABLES['db_name'],
        ENV_VARIABLES['db_host'],
        ENV_VARIABLES['db_user'],
        ENV_VARIABLES['db_password'],
        ENV_VARIABLES['db_schema'],
    )


def establish_postgresql_connection_for_user_cand_db():
    """Подключение к БД dev-user-cand-db"""
    return postgresql_connect(
        ENV_VARIABLES['candidate_db_name'],
        ENV_VARIABLES['candidate_db_host'],
        ENV_VARIABLES['candidate_db_user'],
        ENV_VARIABLES['candidate_db_password'],
        ENV_VARIABLES['candidate_db_schema'],
    )


def establish_postgresql_connection_for_reporting_db():
    """Подключение к БД directory"""
    return postgresql_connect(
        ENV_VARIABLES['reporting_db_name'],
        ENV_VARIABLES['reporting_db_host'],
        ENV_VARIABLES['reporting_db_user'],
        ENV_VARIABLES['reporting_db_password'],
        ENV_VARIABLES['reporting_db_schema'],
    )


def postgresql_connect(name: str, host: str, user: str, password: str, schema: str):
    engine = create_engine(
        f'postgresql://{user}:{password}@{host}:5432/{name}',
        pool_size=10,
        pool_recycle=3600,
        max_overflow=20,
        echo=True,
        connect_args={'options': '-csearch_path={}'.format(schema)}
    )
    inspect(engine)
    Session = sessionmaker(bind=engine, autoflush=True, expire_on_commit=True)
    session = Session()
    return session
