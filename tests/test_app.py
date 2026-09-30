import unittest

try:
    from ..app import App
    from ..request import Request
    from ..routes import ROUTE_TABLE
except ImportError:
    from app import App
    from request import Request
    from routes import ROUTE_TABLE


class AppRoutingTests(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def make_request(self, method, path, body="", headers=None, cookies=None):
        return Request(
            method=method,
            path=path,
            headers=headers or {},
            body=body,
            cookies=cookies or {},
        )

    def test_home_route(self):
        response = self.app.handle_request(self.make_request("GET", "/"))
        self.assertEqual(response.status, 200)
        self.assertIn("Welcome to the Example Site", response.body)

    def test_reset_route(self):
        response = self.app.handle_request(self.make_request("GET", "/reset"))
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers["Location"], "/")

    def test_logout_route(self):
        response = self.app.handle_request(self.make_request("GET", "/logout"))
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers["Location"], "/")

    def test_login_get_route(self):
        response = self.app.handle_request(self.make_request("GET", "/login"))
        self.assertEqual(response.status, 200)
        self.assertIn("<form", response.body)

    def test_login_post_route(self):
        request = self.make_request("POST", "/login", body="username=unknown&password=invalid")
        response = self.app.handle_request(request)
        self.assertEqual(response.status, 200)
        self.assertIn("Login failed", response.body)

    def test_profile_route(self):
        response = self.app.handle_request(self.make_request("GET", "/profile"))
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers["Location"], "/login")

    def test_api_login_route(self):
        request = self.make_request("POST", "/api/login", body="username=unknown&password=invalid")
        response = self.app.handle_request(request)
        self.assertEqual(response.status, 401)
        self.assertIn("invalid_credentials", response.body)

    def test_api_profile_route(self):
        response = self.app.handle_request(self.make_request("GET", "/api/profile"))
        self.assertEqual(response.status, 401)
        self.assertIn("missing_authorization", response.body)

    def test_admin_route(self):
        response = self.app.handle_request(self.make_request("GET", "/admin"))
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers["Location"], "/login")

    def test_about_route(self):
        response = self.app.handle_request(self.make_request("GET", "/about"))
        self.assertEqual(response.status, 200)
        self.assertIn("<h1>About</h1>", response.body)

    def test_demo_route(self):
        response = self.app.handle_request(self.make_request("GET", "/demo"))
        self.assertEqual(response.status, 200)

    def test_home_language_route(self):
        response = self.app.handle_request(self.make_request("GET", "/ua"))
        self.assertEqual(response.status, 200)
        self.assertIn("Мова: Українська", response.body)
        self.assertIn("Вітаємо на демонстраційному сайті", response.body)

    def test_two_parameter_page_route(self):
        response = self.app.handle_request(self.make_request("GET", "/about/ua"))
        self.assertEqual(response.status, 200)
        self.assertIn("<h1>Про сайт</h1>", response.body)

    def test_unknown_route_returns_404(self):
        response = self.app.handle_request(self.make_request("GET", "/zz"))
        self.assertEqual(response.status, 404)

    def test_request_params_contains_captured_values(self):
        request = self.make_request("GET", "/about/ua")
        self.app.handle_request(request)
        self.assertEqual(request.params, {"code": "about", "lang": "ua"})

    def test_table_contains_route_for_each_registered_handler(self):
        self.assertEqual(len(self.app.router.routes), len(ROUTE_TABLE))


if __name__ == "__main__":
    unittest.main()