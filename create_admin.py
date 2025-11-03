# create_admin.py
import getpass
import auth
import database

def setup_initial_admin():
    """
    A one-time script to create the first administrator account for the application.
    """
    print("--- Initial Administrator Setup ---")
    print("The application database and tables will be created if they don't exist.")
    database.create_tables()

    print("\nPlease create the first Admin account.")

    while True:
        username = input("Enter a username for the new Admin: ").strip()
        if username:
            break
        print("Username cannot be empty.")

    while True:
        password = getpass.getpass("Enter a password for the new Admin: ")
        if password:
            password_confirm = getpass.getpass("Confirm password: ")
            if password == password_confirm:
                break
            else:
                print("Passwords do not match. Please try again.")
        else:
            print("Password cannot be empty.")

    success, message = auth.create_user(username, password, "Admin")

    if success:
        print(f"\n✅ {message}")
        print(f"You can now run the application by executing 'python gui.py' and log in as '{username}'.")
    else:
        print(f"\n❌ Error: {message}")
        print("Please try running the script again.")

if __name__ == "__main__":
    setup_initial_admin()
