# Queries for users
get_users_query = "SELECT * FROM users"
get_user_by_id_query = "SELECT * FROM users WHERE userid = %s"
check_email_exists_query = "SELECT * FROM users WHERE email = %s"
add_user_query = "INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)"
delete_user_query = "DELETE FROM users WHERE userid = %s"
update_user_query = "UPDATE users SET email = %s, password = %s, phoneno = %s WHERE userid = %s"