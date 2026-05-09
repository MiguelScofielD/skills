from flask import Flask, render_template, request, url_for, redirect
import jinja2
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# forms
from forms import CreateContactForm

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
ckeditor = CKEditor(app)
bootstrap = Bootstrap5(app)


def send_email(message, address):
    my_email = os.getenv("EMAIL_USER")
    my_password = os.getenv("EMAIL_PASSWORD")

    email = EmailMessage()
    email["From"] = my_email
    email["To"] = address
    email["Subject"] = "Hi!"
    email.add_alternative(message, subtype="html")
    # email.set_content(message)  # automaticamente usa UTF-8

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.send_message(email)


@app.route("/")
def index():
    whatsapp = os.getenv("WHATSAPP_NUMBER")
    return render_template("index.html", whatsapp=whatsapp)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = CreateContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        send_message = f"""
        <h2>Novo contato</h2>

        <p><strong>Nome:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>

        <hr>

        {message}
        """

        send_email(send_message, "antdp408@gmail.com")
        return redirect(url_for("contact", sent="true"))
    msg_sent = request.args.get("sent") == "true"
    return render_template("contact.html", form=form, msg_sent=msg_sent)


if __name__ == "__main__":
    app.run(debug=True)
