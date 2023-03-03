#!/usr/bin/env python
"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys
from secrets import compare_digest

from sqlalchemy.exc import IntegrityError

from modules import db, app
from modules.users.models import User, Role

def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        try:
            create = input("Create admin user? (y/n): ")
            if create.lower() == 'n':
                return
        except EOFError:
            pass

        admin_sid = input("Enter admin user ID (min=10, max=30 characters): ")
        admin_name = input("Enter admin name: ")

        def get_password():
            password = getpass("Enter admin password (min=12, max=50 characters): ")
            confirm_password = getpass("Confirm admin password: ")

            if not compare_digest(password, confirm_password):
                print("Passwords do not match. Retry.")
                return get_password()
            return password

        admin_password = get_password()
        admin_gender = input("Enter admin gender? (M/F): ")

        admin_role = Role()
        admin_role.purpose = "admin"
        admin_role.permission_level = True

        user_exist = User.query.filter(User.sid == admin_sid.upper().replace("/", "_")).first()
        if user_exist is not None:
            print(f"Admin user with ID: {admin_sid} already exist.")
            return

        admin_user = User()
        admin_user.name = admin_name.lower()
        admin_user.sid = admin_sid.upper().replace("/", "_")
        admin_user.password = admin_password
        admin_user.show_pswd = admin_password
        admin_user.gender = admin_gender.upper()

        try:
            admin_role.users.append(admin_user)
            admin_role.update()
            print("Admin user added")
        except IntegrityError as e:
            print(e)
            db.session.rollback()


if __name__ == '__main__':
    sys.exit(main())