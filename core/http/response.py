from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class ResponseFormat:
    """
    전역적으로 사용되는 API 응답 포맷입니다.
    """

    def __init__(self, code: int, message: str, data: dict | list | None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self) -> dict:
        return {
            "meta": {
                "code": self.code,
                "message": self.message,
            },
            "data": self.data,
        }


class CafehereRenderer(JSONRenderer):
    def render(
        self,
        data: dict,
        accepted_media_type: str | None = None,
        renderer_context: dict = None,
    ) -> bytes:
        response_context: Response = renderer_context["response"]

        if response_context.status_code == 204:
            return super().render(
                data,
                accepted_media_type,
                renderer_context,
            )

        response_format = ResponseFormat(
            code=response_context.status_code,  # 상태 코드 반환
            message="ok"
            if not response_context.exception
            else response_context.data.get(
                "detail", response_context.data
            ),  # 예외가 발생하지 않았다면 "ok"를, 발생했다면 예외 메시지를 반환
            data=response_context.data if not response_context.exception else None,
        ).to_dict()

        renderer_context["response"].data = response_format

        return super().render(
            response_format,
            accepted_media_type,
            renderer_context,
        )
