import json

import falcon
from attr import dataclass
from falcon import Response
from piri.process import Process
from piri.schema import SCHEMA
from returns.result import safe


@safe
def create_success_response(*args, **kwargs) -> Response:
    """Return success response."""
    return (args, falcon.HTTP_200)


@safe
def create_failure_response(failure: Exception) -> Response:
    """Return failure response."""
    error_message = '{failure}'.format(
        failure=failure.args[0],
    )
    return ({'error': error_message}, falcon.HTTP_400)


@dataclass(frozen=True, slots=True)
class Mapper(object):
    """Handle get and post request for mapping."""

    schema: str = json.dumps(SCHEMA)

    def on_get(self, req, resp):
        """Return schema."""
        resp.body = self.schema

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        """Map stuff."""
        if not req.content_length:
            resp.status = falcon.HTTP_BAD_REQUEST
            return

        post_data = json.loads(req.stream.read(req.content_length))

        body, code = Process()(
            post_data['data'],
            post_data['configuration'],
        ).bind(
            create_failure_response,
        ).rescue(
            create_failure_response,
        ).unwrap()

        resp.body = json.dumps(body)
        resp.status = code


application = falcon.API()

application.add_route('/', Mapper())
