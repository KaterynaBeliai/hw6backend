import unittest

try:
    from ..router import Router
except ImportError:
    from router import Router


class RouterTests(unittest.TestCase):
    def test_routes_are_stored_per_router(self):
        router = Router()
        other_router = Router()
        handler = object()

        router.add_route("GET", "/", handler)

        self.assertEqual(router.routes, [("GET", "/", handler)])
        self.assertEqual(other_router.routes, [])

    def test_match_returns_first_matching_route_and_captures_params(self):
        router = Router()
        first_handler = object()
        second_handler = object()
        router.add_route("GET", "/users/{user_id}", first_handler)
        router.add_route("GET", "/users/{name}", second_handler)

        handler, params = router.match("GET", "/users/42")

        self.assertIs(handler, first_handler)
        self.assertEqual(params, {"user_id": "42"})

    def test_match_ignores_repeated_and_trailing_slashes(self):
        self.assertEqual(
            Router._match_pattern("/users/{user_id}/", "//users//42/"),
            {"user_id": "42"},
        )

    def test_literal_segments_must_match(self):
        self.assertIsNone(Router._match_pattern("/users", "/posts"))

    def test_segment_counts_must_match(self):
        self.assertIsNone(Router._match_pattern("/users/{user_id}", "/users"))
        self.assertIsNone(Router._match_pattern("/users", "/users/42"))

    def test_method_mismatch_and_unmatched_path_return_none_pair(self):
        router = Router()
        router.add_route("GET", "/users/{user_id}", object())

        self.assertEqual(router.match("POST", "/users/42"), (None, None))
        self.assertEqual(router.match("GET", "/posts/42"), (None, None))


if __name__ == "__main__":
    unittest.main()