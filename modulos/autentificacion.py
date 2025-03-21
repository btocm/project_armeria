from flask import redirect, render_template, request, session, url_for

from db import mysql
from utils import Logger

log = Logger()


def rutas_autentificacion(app):

    # Ruta para mostrar el menú inicio de sesión
    @app.route("/")
    def index():
        try:
            log.log_info(error="00", pretext="Se accedio a la pagina de Inicio de Sesion")
            return render_template("index.html")
        except Exception as e:
            log.log_error(error="01", posttext=e)
            return render_template("error.html")

    # Ruta para iniciar sesión
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            usuario = request.form["usuario"]
            password = request.form["password"]
            log.log_info(pretext=f"Intento de inicio de sesion para el usuario: {usuario}")

            try:
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
                user = cur.fetchone()
                cur.close()
            except Exception as e:
                log.log_error(error="03", posttext=e)
                return render_template("error.html")

            if user and user["password"] == password:
                session["user"] = user
                log.log_info(
                    posttext=f"Inicio de sesion para: {usuario} - {user['rol']}",
                    error="00",
                )

                # Redirección basada en el rol del usuario
                rutas_por_rol = {
                    "almacen": "menu_almacen",
                    "mantenimiento": "menu_mantenimiento",
                    "ventas": "menu_ventas",
                    "proveedores": "menu_proveedores",
                    "envios": "menu_envios",
                }
                return redirect(url_for(rutas_por_rol.get(user["rol"], "index")))
            else:
                log.log_warning(error="02")
                return render_template("index.html")

        return render_template("index.html")

    # Ruta para cerrar sesión
    @app.route("/logout", methods=["POST"])
    def logout():
        # try:
        if "user" in session:
            usuario = session["user"]["usuario"]
            log.log_info(pretext=f'El usuario {usuario} cerro sesion', error="00")
            session.pop("user", None)
        else:
            log.log_warning(error="04")
            return render_template("error.html")
        return redirect(url_for("index"))

    return app
