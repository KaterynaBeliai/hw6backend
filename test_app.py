from app_instance import app


def test_app_dispatch_and_404():
    @app.get("/alpha")
    def alpha(request):
        return "alpha"

    @app.get("/beta")
    def beta(request):
        return "beta"

    response_alpha = app.handle_request(type("Req", (), {"method": "GET", "path": "/alpha", "cookies": {}, "params": {}, "body": "", "query": {}})())
    response_beta = app.handle_request(type("Req", (), {"method": "GET", "path": "/beta", "cookies": {}, "params": {}, "body": "", "query": {}})())
    response_missing = app.handle_request(type("Req", (), {"method": "GET", "path": "/missing", "cookies": {}, "params": {}, "body": "", "query": {}})())

    assert response_alpha.status == 200
    assert response_alpha.body == "alpha"
    assert response_beta.status == 200
    assert response_beta.body == "beta"
    assert response_missing.status == 404


if __name__ == "__main__":
    test_app_dispatch_and_404()
    print("test_app: ok")
