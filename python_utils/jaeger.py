
def init_jaeger_tracer(service_name='python-utils'):
    """
    Initializes and configures the Jaeger tracer.
    """
    from jaeger_client import Config
    from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
    config = Config(
        config={},
        service_name=service_name,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(service_name_label=service_name),
    )
    return config.initialize_tracer()
