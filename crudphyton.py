import psycopg2

def connect_to_db():
    try:
        connection = psycopg2.connect(
            database="crud",
            user="victor",
            password="4dwtp1icDHTATJPoyQfB_w",
            host="blue-fawn-13857.7tt.aws-us-east-1.cockroachlabs.cloud",
            port="26257",
            options="-c parameters=extended",
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error al conectarse a PostgreSQL", error)

def create_user(connection, cursor):
    try:
        id = int(input("Ingrese el ID del usuario: "))
        nombre = input("Ingrese el nombre del usuario: ")
        apellido = input("Ingrese el apellido del usuario: ")

        cursor.execute("INSERT INTO usuario (id, nombre, apellido) VALUES (%s, %s, %s)", (id, nombre, apellido))
        connection.commit()
        print("Usuario creado exitosamente")
    except (Exception, psycopg2.Error) as error:
        print("Error al crear el usuario", error)

def read_users(connection, cursor):
    try:
        cursor.execute("SELECT * FROM usuario")
        users = cursor.fetchall() 
        return [dict(zip([col.name for col in cursor.description], user)) for user in users]
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener los usuarios", error)
        return [] 

def update_user(connection, cursor):
    try:
        id = int(input("Ingrese el ID del usuario a actualizar: "))
        nombre = input("Ingrese el nuevo nombre del usuario (o presione Enter para no modificar): ")
        apellido = input("Ingrese el nuevo apellido del usuario (o presione Enter para no modificar): ")

        update_query = "UPDATE usuario SET "
        update_fields = []
        if nombre:
            update_fields.append("nombre = %s")
        if apellido:
            update_fields.append("apellido = %s")
        update_query += ", ".join(update_fields)
        update_query += " WHERE id = %s"

        if update_fields:  
            cursor.execute(update_query, (nombre, apellido, id))
            connection.commit()
            print("Usuario actualizado exitosamente")
        else:
            print("No se proporcionaron campos para actualizar")
    except (Exception, psycopg2.Error) as error:
        print("Error al actualizar el usuario", error)

def delete_user(connection, cursor):
    try:
        id = int(input("Ingrese el ID del usuario a eliminar: "))
        cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
        connection.commit()
        print("Usuario eliminado exitosamente")
    except (Exception, psycopg2.Error) as error:
        print("Error al eliminar el usuario", error)

if __name__ == "__main__":
    connection = connect_to_db()
    cursor = connection.cursor()

    while True:
        print("Seleccione una operación:")
        print("1. Crear usuario")
        print("2. Leer usuarios")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("5. Salir")

        opcion = int(input("Ingrese su opción: "))

        if opcion == 1:
            create_user(connection, cursor)
        elif opcion == 2:
            users = read_users(connection, cursor)
            if users:
                print("Usuarios:")
                for user in users:
                    print(f"ID: {user['id']}")
                    print(f"Nombre: {user['nombre']}")
                    print(f"Apellido: {user['apellido']}")
                    print()
            else:
                print("No hay usuarios registrados")
        elif opcion == 3:
            update_user(connection, cursor)
        elif opcion == 4:
            delete_user(connection, cursor)
        elif opcion == 5:
            break
        else:
            print("Opción inválida. Intente nuevamente.")

        print()

    cursor.close()
    connection.close()
