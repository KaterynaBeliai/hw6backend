from app_instance import app
from auth import login_required
from sessions import sessions


def test_login_required_redirects_without_session():
    @app.get("/secure")
    @login_required(sessions)
    def secure(request):
        raise AssertionError("handler should not run without a valid session")

    request = type("Req", (), {"method": "GET", "path": "/secure", "cookies": {}, "params": {}, "body": "", "query": {}})()
    response = app.handle_request(request)
    assert response.status == 302
    assert response.headers["Location"] == "/login"


def test_login_required_allows_valid_session():
    session_id = sessions.create_session({"name": "alice"})

    @app.get("/profile2")
    @login_required(sessions)
    def profile(request):
        return request.session["name"]

    request = type("Req", (), {"method": "GET", "path": "/profile2", "cookies": {"session_id": session_id}, "params": {}, "body": "", "query": {}})()
    response = app.handle_request(request)
    assert response.status == 200
    assert response.body == "alice"


if __name__ == "__main__":
    test_login_required_redirects_without_session()
    test_login_required_allows_valid_session()
    print("test_auth: ok")
