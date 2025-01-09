from .table_models import User


class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_user(self, name, surname, nickname):
        try:
            new_user = User(name=name, surname=surname, nickname=nickname)
            self.db_manager.add(new_user)
            self.db_manager.commit()
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error adding user: {e}")

    def get_all_users(self):
        try:
            users = self.db_manager.session.query(User).all()
            return users
        except Exception as e:
            print(f"Error getting users: {e}")
            return []


