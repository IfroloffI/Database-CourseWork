import bcrypt

password = "adminpass"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
print("Сгенерированный хэш:", hashed)