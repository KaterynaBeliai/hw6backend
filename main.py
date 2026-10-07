try:
    from .server import HTTPServer
    from .templater import Templater
except Exception:
    # Allow running `python main.py` from inside the folder
    from server import HTTPServer
    from templater import Templater

from app_instance import app

# Import routes at startup so the decorators run and register handlers on the shared app instance.
# Without this import, app.router.routes stays empty and every request resolves to a 404.
import routes


def demo_render():
    t = Templater()
    html = t.render("demo", {"name": "John", "lang": "Python"})
    print("--- Rendered demo (hardcoded) ---")
    print(html)


if __name__ == "__main__":
    demo_render()
    HTTPServer(app).start()
