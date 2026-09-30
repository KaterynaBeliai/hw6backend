class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, method, pattern, handler):
        self.routes.append((method, pattern, handler))

    def match(self, method, path):
        for route_method, pattern, handler in self.routes:
            if route_method != method:
                continue

            params = self._match_pattern(pattern, path)
            if params is not None:
                return handler, params

        return None, None

    @staticmethod
    def _match_pattern(pattern, path):
        """Return captured parameters when pattern matches path."""
        pattern_segments = [segment for segment in pattern.split("/") if segment]
        path_segments = [segment for segment in path.split("/") if segment]

        if len(pattern_segments) != len(path_segments):
            return None

        params = {}
        for pattern_segment, path_segment in zip(pattern_segments, path_segments):
            if pattern_segment.startswith("{") and pattern_segment.endswith("}"):
                params[pattern_segment[1:-1]] = path_segment
            elif pattern_segment != path_segment:
                return None

        return params