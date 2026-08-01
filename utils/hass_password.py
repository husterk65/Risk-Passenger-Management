import bcrypt

password = "123456"

password_hash = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
).decode()

print(password_hash)