from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time_created):
    with mock_db_time_created(model=User) as time:
        new_user = User(
            username='alice', email='alice@dunossauro.com', password='secret'
        )

        session.add(new_user)
        session.commit()

        user_alice = session.scalar(
            select(User).where(User.username == 'alice')
        )

    assert asdict(user_alice) == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@dunossauro.com',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }


def test_update_user(session, mock_db_time_created):
    with mock_db_time_created(model=User) as time:
        new_user = User(
            username='alice', email='alice@dunossauro.com', password='secret'
        )

        session.add(new_user)
        session.commit()

        user_alice = session.scalar(
            select(User).where(User.username == 'alice')
        )

        user_alice.email = 'alice@teste'
        session.commit()

    assert asdict(user_alice) == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@teste',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }
