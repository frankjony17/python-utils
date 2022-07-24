
import time
from typing import Optional

from loguru import logger
from prometheus_client import Counter, Gauge, Histogram
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class PrometheusMiddleware:

    _metrics = {}

    def __init__(
        self, app: ASGIApp, group_paths: bool = False, app_name: str = "starlette",
        prefix: str = "fksolutions", filter_unhandled_paths: bool = False,
        buckets=(0.1, 0.2, 0.5, 1, 2, 3, 5, 10, float('inf'))
    ) -> None:
        self.app = app
        self.group_paths = group_paths
        self.app_name = app_name
        self.prefix = prefix
        self.filter_unhandled_paths = filter_unhandled_paths
        self.buckets = buckets

    @property
    def request_count(self):
        metric_name = f"{self.prefix}_request_count_total"
        if metric_name not in PrometheusMiddleware._metrics:
            PrometheusMiddleware._metrics[metric_name] = Counter(
                metric_name,
                "Total HTTP requests",
                ("method", "endpoint", "http_status", "app_name"),
            )
        return PrometheusMiddleware._metrics[metric_name]

    @property
    def request_count_gauge(self):
        metric_name = f"{self.prefix}_concurrent_request_count"
        if metric_name not in PrometheusMiddleware._metrics:
            PrometheusMiddleware._metrics[metric_name] = Gauge(
                metric_name,
                "Concurrent Request Count",
                multiprocess_mode='livesum'
            )
        return PrometheusMiddleware._metrics[metric_name]

    @property
    def request_time(self):
        metric_name = f"{self.prefix}_request_latency_ms"
        if metric_name not in PrometheusMiddleware._metrics:
            PrometheusMiddleware._metrics[metric_name] = Histogram(
                metric_name,
                "HTTP request duration, in mile seconds",
                ("method", "endpoint", "http_status", "app_name"), buckets=self.buckets)
        return PrometheusMiddleware._metrics[metric_name]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http"]:
            await self.app(scope, receive, send)
            return
        request = Request(scope)
        method = request.method
        path = request.url.path
        begin = time.perf_counter()
        status_code = 500

        async def wrapped_send(message: Message) -> None:
            if message['type'] == 'http.response.start':
                nonlocal status_code
                status_code = message['status']
            await send(message)

        try:
            await self.app(scope, receive, wrapped_send)
        finally:
            grouped_path = None

            if self.filter_unhandled_paths or self.group_paths:
                grouped_path = self._get_router_path(request)

                if self.group_paths and grouped_path is not None:
                    path = grouped_path

            if not(self.filter_unhandled_paths and grouped_path is None):
                end = time.perf_counter()
                labels = [method, path, status_code, self.app_name]
                self.request_count.labels(*labels).inc()
                self.request_time.labels(*labels).observe(end - begin)

    @staticmethod
    def _get_router_path(request: Request) -> Optional[str]:
        """Returns the original router path (with url param names) for given request."""
        try:
            if not (request.scope.get('endpoint') and request.scope.get('router')):
                return None

            for route in request.scope['router'].routes:
                if ((hasattr(route, 'endpoint') and route.endpoint == request.scope['endpoint']) or
                        (hasattr(route, 'app') and route.app == request.scope['endpoint'])):
                    return route.path
        except Exception as e:
            logger.opt(exception=True).error(f'[-] Error: {e}')
        return None
