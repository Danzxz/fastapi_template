from fastapi import FastAPI
from infrastructure.ioc.container import Container
from opentelemetry import trace
from web.api.v1.example.router import example_router

tracer = trace.get_tracer(__name__)


def register_callback(app: FastAPI, container: Container) -> None:
    with tracer.start_as_current_span("register_callback"):

        def shutdown():
            container.shutdown_resources()

        app.add_event_handler("shutdown", shutdown)

        app.include_router(example_router, prefix="/example")
