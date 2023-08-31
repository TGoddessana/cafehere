from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenBlacklistView as _TokenBlacklistView
from rest_framework_simplejwt.views import TokenObtainPairView as _TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView as _TokenRefreshView

from apps.authentication.models import User
from apps.authentication.serializers import RegisterSerializer

TAG = "Authentication API"


@extend_schema(
    tags=[TAG],
    summary="회원가입 API 입니다.",
    description="""
사용자는 전화번호와 비밀번호를 입력하여 회원가입을 할 수 있습니다.

E.164(International Public Telecommunication Numbering Plan) 의 규칙을 따릅니다.

문자열은 다음과 같아야 합니다.

- 전화번호의 시작 부분에 더하기 기호(+)로 시작합니다.
- 더하기 기호 뒤에는 국가 코드를 나타내는 최대 네 자리 숫자(0-9)가 와야 합니다.
- 국가 코드 뒤에는 나머지 번호와 구분하기 위해 하이픈(-)이 있어야 합니다.
- 하이픈 뒤에는 길이가 1~14인 또 다른 숫자 시퀀스(0~9)가 와야 합니다.
- 문자열은 마지막 숫자 집합과 하이픈($) 바로 뒤에서 끝나야 합니다.
""",
    external_docs={
        "description": "E.164",
        "url": "https://www.itu.int/rec/T-REC-E.164-201011-I/en",
    },
)
class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@extend_schema(
    tags=[TAG],
    summary="로그아웃 API 입니다.",
    description="""
사용자는 로그아웃을 할 수 있습니다.

로그아웃은 `Refresh Token` 을 블랙리스트에 추가하는 것으로 이루어집니다.
""",
)
class LogoutAPIView(_TokenBlacklistView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


@extend_schema(
    tags=[TAG],
    summary="로그인 API 입니다.",
    description=f"""
사용자는 전화번호와 비밀번호를 입력하여 로그인을 할 수 있습니다.

로그인 시, `Access Token` 과 `Refresh Token` 을 발급받습니다.

각 토큰의 만료시간은 아래와 같습니다.

- `Access Token`: {int(api_settings.ACCESS_TOKEN_LIFETIME.seconds / 60)} 분
- `Refresh Token`: {api_settings.REFRESH_TOKEN_LIFETIME.days} 일
""",
)
class LoginAPIView(_TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


@extend_schema(
    tags=[TAG],
    summary="토큰 갱신 API 입니다.",
    description="""
사용자는 `Refresh Token` 을 이용하여 `Access Token` 을 재발급 받을 수 있습니다.

한 번 사용된 `Refresh Token` 은 블랙리스트에 추가되어 재사용이 불가능합니다.
""",
)
class RefreshAPIVIew(_TokenRefreshView):
    pass
