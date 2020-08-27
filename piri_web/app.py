import json

import falcon
from attr import dataclass
from piri.process import process
from piri.schema import SCHEMA


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

        resp.body = json.dumps(
            process(post_data['data'], post_data['configuration']),
        )


application = falcon.API()

application.add_route('/', Mapper())
