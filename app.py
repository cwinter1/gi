import base64
import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_IMAGE_BYTES = 10 * 1024 * 1024  # 10 MB


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def index():
    if session.get("logged_in"):
        return render_template("gi.html")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if (username == os.getenv("SITE_USERNAME", "admin") and
                password == os.getenv("SITE_PASSWORD", "gi123")):
            session["logged_in"] = True
            return redirect(url_for("index"))
        error = "שם משתמש או סיסמה שגויים"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/finance/")
@app.route("/finance/index.html")
def finance_index():
    return render_template("finance/index.html")


@app.route("/finance/budget.html")
def finance_budget():
    return render_template("finance/budget.html")


@app.route("/finance/overdraft.html")
def finance_overdraft():
    return render_template("finance/overdraft.html")


@app.route("/analyse", methods=["POST"])
@require_login
def analyse():
    file = request.files.get("photo")
    if not file or not file.filename:
        return render_template("gi.html", error="נא לבחור תמונה")

    media_type = file.mimetype or "image/jpeg"
    if media_type not in ALLOWED_IMAGE_TYPES:
        return render_template("gi.html", error="פורמט לא נתמך — השתמש ב-JPEG, PNG או WEBP")

    image_bytes = file.read()
    if len(image_bytes) > MAX_IMAGE_BYTES:
        return render_template("gi.html", error="הקובץ גדול מדי (מקסימום 10 MB)")

    try:
        from agents.gi_agent import analyse_image
        result = analyse_image(image_bytes, media_type)
    except ValueError as e:
        return render_template("gi.html", error=f"שגיאת הגדרות: {e}")
    except Exception as e:
        return render_template("gi.html", error=f"שגיאה בניתוח: {e}")

    photo_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    return render_template("gi.html", result=result, photo_b64=photo_b64, photo_mime=media_type)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)
