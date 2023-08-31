from rest_framework.renderers import JSONRenderer


class CafehereRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context["response"]

        response_format = {
            "meta": {
                "code": response.status_code,
                "message": "success" if not response.exception else "error",
            },
            "data": data if not response.exception else None,
        }

        return super().render(response_format, accepted_media_type, renderer_context)
