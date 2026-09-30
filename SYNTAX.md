# Python Syntax Used This Session

- Class with list state (`self.routes = []`) — `router.py` — each `Router` owns its route list.
- Bound method passed without parentheses — `app.py` — `getattr(self, handler_name)` returns a handler to register.
- `@staticmethod` — `router.py` — `_match_pattern()` uses only its arguments and needs no instance state.
- `getattr(obj, name)` — `app.py` — resolves the handler name at registration time; a typo in the string fails then, while `self.name` is checked directly in code.
- List comprehension filtering empty segments — `router.py` — `pattern_segments` drops empty slash-separated parts.
- `zip()` for parallel iteration — `router.py` — compares each pattern segment with its matching path segment.
- Return two values as a tuple and unpack them — `router.py`, `app.py` — `match()` returns `(handler, params)`, unpacked by `handle_request()`.
- `unittest.TestCase` — `tests/test_router.py` — `RouterTests` inherits test runner assertions.
- `setUp()` — `tests/test_app.py` — creates a fresh `App` for each test.
- `assertEqual`, `assertIsNone`, and `assertIs` — `tests/test_router.py` — check values, no-match results, and handler identity.