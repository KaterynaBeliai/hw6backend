from app_instance import app
from auth import login_required
from http_parser import parse_query_string
from response import HTMLResponse, RedirectResponse, JSONResponse, Response
from sessions import sessions, create_session
from users import check_password, USERS
from tokens import make_token, verify_token


@app.get("/")
def home(request):
    return app._render_home(request, "en")


@app.get("/reset")
def reset(request):
    return app.handle_reset(request)


@app.get("/logout")
def logout(request):
    return app.handle_logout(request)


@app.get("/login")
def login(request):
    return app.login_form()


@app.post("/login")
def login_post(request):
    form = parse_query_string(request.body or "")
    username = form.get("username") or ""
    password = form.get("password") or ""
    if not check_password(username, password):
        return app.login_form(error="Login failed")

    role = "admin" if username == "admin" else "user"
    email = USERS.get(username, {}).get("email")
    session_id = create_session({"user": username, "role": role, "email": email})
    response = RedirectResponse("/profile")
    response.set_cookie("session_id", session_id, max_age=3600, http_only=True)
    return response


@app.get("/profile")
@login_required(sessions)
def profile(request):
    profile_data = {
        "user": request.session.get("user"),
        "role": request.session.get("role"),
        "email": request.session.get("email"),
    }
    return app._render_page("profile", request, profile_data)


@app.post("/api/login")
def api_login(request):
    form = parse_query_string(request.body or "")
    username = form.get("username") or ""
    password = form.get("password") or ""
    if not check_password(username, password):
        return JSONResponse({"error": "invalid_credentials"}, status=401)
    role = "admin" if username == "admin" else "user"
    return JSONResponse({"token": make_token(username, role)})


@app.get("/api/profile")
def api_profile(request):
    auth = (request.headers or {}).get("authorization")
    if not auth or not auth.lower().startswith("bearer "):
        return JSONResponse({"error": "missing_authorization"}, status=401)
    payload = verify_token(auth.split(None, 1)[1])
    if payload is None:
        return JSONResponse({"error": "invalid_token"}, status=401)
    return JSONResponse({"user": payload.get("username"), "role": payload.get("role")})


@app.get("/admin")
def admin(request):
    session_id = (request.cookies or {}).get("session_id")
    session = sessions.get_session(session_id) if session_id else None
    role = session.get("role") if session is not None else (request.cookies or {}).get("role")
    if session_id is None and role is None:
        return RedirectResponse("/login")
    if role != "admin":
        return HTMLResponse("403 Forbidden", status=403)
    return HTMLResponse("Welcome to admin area")


@app.get("/about")
def about(request):
    return app._render_page("about", request)


@app.get("/demo")
def demo(request):
    return app._render_page("demo", request)


@app.get("/echo")
def echo_get(request):
    return app._render_page("demo", request)


@app.post("/echo")
def echo_post(request):
    return Response(request.body or "", content_type="text/plain; charset=utf-8")


@app.get("/{lang}")
def home_lang(request):
    lang = request.params["lang"]
    if lang not in {"en", "ua"}:
        return HTMLResponse("Not Found", status=404)
    return app._render_home(request, lang)


@app.get("/{code}/{lang}")
def localized_page(request):
    code = request.params["code"]
    lang = request.params["lang"]
    if code not in {"index", "about", "demo"} or lang not in {"en", "ua"}:
        return HTMLResponse("Not Found", status=404)
    if code == "index":
        return app._render_home(request, lang)
    return app._render_page(code, request, lang=lang)


# Legacy compatibility only; App no longer reads this list for registration.
ROUTE_TABLE = [
    ("GET", "/", "home"),
    ("GET", "/reset", "reset"),
    ("GET", "/logout", "logout"),
    ("GET", "/login", "login"),
    ("POST", "/login", "login_post"),
    ("GET", "/profile", "profile"),
    ("POST", "/api/login", "api_login"),
    ("GET", "/api/profile", "api_profile"),
    ("GET", "/admin", "admin"),
    ("GET", "/about", "about"),
    ("GET", "/demo", "demo"),
    ("GET", "/echo", "echo_get"),
    ("POST", "/echo", "echo_post"),
    ("GET", "/{lang}", "home_lang"),
    ("GET", "/{code}/{lang}", "localized_page"),
]
