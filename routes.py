from flask import render_template, Blueprint, request, redirect, url_for
from flask import session as client_session
from database import *

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return render_template("main.html")

@bp.route("/login", methods=["POST", "GET"])
def login():
    message = ""
    if request.method == "POST":
        if request.form.get("form_name") == "register-form":
            email, passw, username, passw_2 = [request.form["email"], request.form["password"], request.form["username"], request.form["confim_password"]]

            verifications = credencials_verification(passw, passw_2, username, email)
            can_register = verifications.can_register
            message = verifications.message

            # can register?
            if can_register:
                new_user = User(email=email, password=passw, username=username)
                session.add(new_user)
                session.commit()

                return redirect(url_for("main.register_warn"))
        
        # LOGIN
        if request.form.get("form_name") == "login-form":
            _email = request.form["email"]
            password = request.form["password"]

            try:
                the_user = session.query(User).filter_by(email=_email).first() # THE USER IN DATABASE

                if the_user.password == password:
                    print("Acesso permitido!")
                    session.permanent = True
                    client_session['usuario'] = _email

                    return redirect(url_for("main.profile_settings"))
                else:
                    print("Acesso negado!")
            except:
                print("Usuario não existe.")

    return render_template("login.html", error_message=message)

@bp.route("/get")
def get():
    # Pega algum usuario com base na senha ou no email
    # a = session.query(User).filter_by(email="vh555@gmail.com").first()
    a, b = [1, 2]
    return f"{a, b}"

@bp.route("/register_warn")
def register_warn():
    return render_template("register-response.html")

@bp.route("/profile_settings", methods=["POST", "GET"])
def profile_settings():
    """
    Pagina de alteração de dados do perfil. Faz alterações direto no bando de dados

    1. Get das infomações                                 --> FEITO
    2. Verificação de senha atual                         --> FEITO
    3. Comando de alterações de dados do banco de dados   --> FEITO
    4. Verificação da função de credenciais válidas       --> NÃO
    5. Avisos após envio da aquisição de mudança de dados --> NÂO
    """
    if not "usuario" in client_session:
        return redirect(url_for("main.login"))

    the_user = session.query(User).filter_by(email=client_session['usuario']).first()
    print(the_user.username)
    print(client_session["usuario"])
    error_message = ""

    if request.method == "POST":
        new_username = request.form["username"] if request.form["username"] != "" else the_user.username
        new_email = request.form["email"] if request.form["email"] != "" else the_user.email
        new_password = request.form["new_password"] if request.form["new_password"] != "" else the_user.password
        current_password = request.form["current_password"]

        print(new_username, new_email, new_password, current_password)

        verifications = credencials_verification(new_password, new_password, new_username, new_email, email_to_remove=the_user.email)
        error_message = verifications.message

        if current_password == the_user.password:
            if verifications.can_register:

                # Change the username
                if len(new_username) != 0:
                    if the_user.username != new_username:
                        the_user.username = new_username
                        print(f"Username mudado para {new_username}")

                # Change the email
                if len(new_email) != 0:
                    if the_user.email != new_email:
                        the_user.email = new_email
                        print(f"email mudado para {new_email}")
                
                # Change the password
                if len(new_password) != 0:
                    if the_user.password != new_password:
                        the_user.password = new_password
                        print(f"passw mudado para {new_password}")

                # Update the changes
                session.commit()

            else:
                print(f"Erro > {verifications.message} < ocurred.") # message about can't register
        else:
            print("Incorrect password")

    return render_template("profile_settings.html", atual_user=the_user.username, error_message=error_message)

def credencials_verification(passw, passw_2, username, email, email_to_remove=""):
    """
    PASSW: the new password
    PASSW_2: the confirmation password
    USERNAME: the new username
    EMAIL: the new email
    EMAIL_TO_REMOVE: remove an especific email from the list of emails
    """
    list_of_users = [c.email for c in session.query(User).all()]
    if email_to_remove != "":
        list_of_users.remove(email_to_remove)


    verifications = {
        "The password length need to be higher than 5 characters": len(passw) >= 5, # if 3 > 5 = FALSE 
        "Username length need to be higher than 3 characters": len(username) >= 3, # FALSE TOO
        "This email is already registered.": email not in list_of_users, # FALSE
        "Password don't match!": passw_2 == passw, # FALSE
        "Fill the username camp": username != "",
        "Fill the email camp": email != "",
    }
    class t:
        def __init__(self, can_register, message):
            self.can_register = can_register
            self.message = message

    for v, k in enumerate(verifications):
        if not verifications[k]:
            return t(False, k) # TEM Q SER FALSO PRA DAR ERRO CARALHO
    return t(True, k)

