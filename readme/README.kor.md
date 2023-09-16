# Your Cafe is right HERE! - CafeHere

## 이것은 무엇인가요?

상품을 등록하고, 나만의 카페를 운영하고 싶은 사장님들을 위한 `HTTP API` 서버입니다.  
해당 서버를 이용하여 카페의 상품을 관리할 수 있습니다.

## 조금 더 자세히 설명해주세요.

### 회원 관련 API

- 사장님은 전화번호와 비밀번호로 회원가입을 할 수 있습니다.
    - 회원가입 시, 전화번호는 `E.164` 포맷을 따라야 합니다. (https://www.itu.int/rec/T-REC-E.164-201011-I/en)
    - 회원가입 시, 비밀번호는 단방향 암호화되어 저장됩니다.
- 사장님은 전화번호와 비밀번호로 로그인을 할 수 있습니다.
    - 로그인은 JWT를 이용하여 구현되었습니다.
    - Access Token 만료 시간은 5분, Refresh Token 만료 시간은 1주일로 설정되어 있습니다.
    - 한 번 사용된 Refresh Token은 더 이상 사용할 수 없습니다. (Refresh Token Rotation)
    - 사용자는 Refresh Token 을 블랙리스트에 추가함으로서, 로그아웃을 할 수 있습니다.

### 카페 관련 API

- 사장님은 로그인 후 카페 관련 아래의 행동을 할 수 있습니다.
    - 카페를 등록할 수 있습니다.
    - 카페의 속성을 부분 수정할 수 있습니다.
    - 등록한 카페의 상세 정보를 조회할 수 있습니다.
    - 등록한 카페를 삭제할 수 있습니다.
    - 로그인하지 않았다면 카페 관련 API를 사용할 수 없습니다.
    - 로그인했더라도, 다른 사장님의 카페를 조회할 수 없습니다.

### 상품 관련 API

- 사장님은 로그인 후 상품 관련 아래의 행동을 할 수 있습니다.
    - 상품을 등록할 수 있습니다.
    - 상품의 속성을 부분 수정할 수 있습니다.
    - 등록한 상품의 목록을 조회할 수 있습니다. Cursor 기반의 페이징을 지원합니다.
    - 등록한 상품을 검색할 수 있습니다. 초성 검색과 이름 검색을 지원합니다.
    - 등록한 상품의 상세 정보를 조회할 수 있습니다.
    - 등록한 상품을 삭제할 수 있습니다.
    - 로그인하지 않았다면 상품 관련 API를 사용할 수 없습니다.
    - 로그인했더라도, 다른 사장님의 카페의 상품을 조회할 수 없습니다.
- 사장님은 로그인 후 카테고리 관련 아래의 행동을 할 수 있습니다.
    - 카테고리를 등록할 수 있습니다.
    - 카테고리의 속성을 부분 수정할 수 있습니다.
    - 등록한 카테고리의 목록을 조회할 수 있습니다.
    - 등록한 카테고리의 상세정보를 조회할 수 있습니다.
    - 로그인하지 않았다면 카테고리 관련 API를 사용할 수 없습니다.
    - 로그인했더라도, 다른 사장님의 카테고리를 조회할 수 없습니다.
- 사장님은 로그인 후 상품의 옵션 관련 아래의 행동을 할 수 있습니다.
    - 옵션 그룹을 등록할 수 있습니다.
    - 옵션 그룹을 삭제할 수 있습니다.
    - 로그인하지 않았다면 상품 옵션 관련 API를 사용할 수 없습니다.
    - 로그인했더라도, 다른 사장님의 상품 옵션 정보를 조회할 수 없습니다.

### 데이터베이스 ERD
![erd.svg](..%2Ferd.svg)

## 어떤 기술을 사용했나요?

메인 언어로 `Python 3.11`을 사용하였습니다.

`Django` 와 `Django REST Framework` 를 사용하여 서버를 구현하였습니다.

`Docker` 와 `Docker Compose` 를 사용하여 언어와 상관없이 서버를 실행할 수 있습니다.

`MySQL 5.7` 데이터베이스를 사용했습니다.

## 고민되는 점이 있었나요?

#### 1. 전화번호 포맷을 어떻게 검증할까?

- 전화번호에 대한 유효성 검증을 하는 것이 많이 고민이었습니다. 국내 번호의 경우뿐만 아니라, 국제 번호까지 고려해야 했기 때문이죠.
- 전화번호는 `E.164` 포맷을 따라야 합니다. (https://www.itu.int/rec/T-REC-E.164-201011-I/en)
- "국제 번호" 와 "전화번호" 사이에는 하이픈(-)이 들어가야 합니다.
- 결과적으로는, `r"^\+[0-9]{1,4}+-[0-9]{1,14}$"` 정규식을 사용하여 검증하도록 구현했습니다.
- 한계점은, 국가 코드가 실제 존재하는 국가의 것인지 확인하지 못한다는 것입니다.

#### 2. 사장님은 하나의 가게만 가질 수 있을까?

- 현재는 사장님이 여러 개의 가게를 가질 수 있도록 구현되어 있습니다.
- 사업 수완이 좋으신 분들은 여러 개의 가게를 운영하실 수도 있으니까요.
- 그래서, 먼저 "내 가게를 오픈하는 API" 를 구현해야겠다고 마음먹었습니다.

#### 3. 상품의 옵션은 어떻게 구현할까?

- 예를 들어, 커피라면 "사이즈", "샷 추가", "시럽 추가" 등의 옵션을 선택할 수 있습니다.
- 혹은 케이크의 경우 "사이즈", "토핑" 등의 옵션을 선택할 수 있겠죠.
- 그래서, 옵션을 묶는 옵션 그룹을 만들고, 옵션 그룹 API 를 통해서 옵션을 관리하도록 구현했습니다.
- 또, 데이터베이스에는 동일한 이름의 옵션 그룹이 저장될 수 있지만 한 카페 내에서는 동일한 옵션 그룹 이름을 가지지 않도록 구현했습니다.
- 결과적으로, 하나의 카페는 해당 카페 안에서 유일한 이름을 가지는 옵션 그룹을, 하나의 옵션 그룹은 해당 옵션 그룹 안에서 유일한 이름을 가지는 옵션을 가질 수 있습니다.
- 하나의 상품은 여러 개의 옵션 그룹을, 하나의 옵션 그룹은 여러 개의 상품을 가질 수 있도록 구현했습니다.

#### 4. 인증 정보에 따른 권한을 어떻게 처리해야 할까?

- 가장 먼저 든 생각은 HTTP 표준 상태 코드를 따르자는 것이었습니다.
- `401 Unauthorized` 는 인증 정보가 없는 경우, `403 Forbidden` 은 인증 정보가 있지만 권한이 없는 경우에 사용됩니다.
- 아래와 같은 `Permission` 클래스를 구현하여, `403 Forbidden` 을 반환하도록 구현했습니다.

```python
class IsCafeOwner(IsAuthenticated):
    def has_permission(self, request, view):
        cafe = Cafe.objects.filter(uuid__exact=view.kwargs["cafe_uuid"]).first()
        if cafe:
            return super().has_permission(request, view) and (
                    request.user == cafe.owner
            )

        return super().has_permission(request, view)
```

#### 5. 상품의 검색을 어떻게 구현할까?

- 검색은 간단한 `Django-filter` 를 사용하여 구현했습니다.
- 초성 검색은, 데이터베이스에 따로 "초성" 필드를 저장함으로서 구현되었습니다.
    - 데이터베이스에 새로운 상품이 저장되거나 정보가 업데이트 될 때마다, 해당 상품의 이름을 초성으로 변환하여 저장합니다.
    - 추후 검색 시, 초성으로 검색할 수 있습니다.
    - 초성 정보는 상세 정보 등 조회 시에는 반환되지 않습니다.

#### Custom JSON Response 를 어떻게 구현할까?

- 해당 서버에서 반환하는 모든 API 가 일관된 형식을 가지도록 구현하기 위해, 아래와 같은`Custom JSON Renderer` 를 구현했습니다.

```python
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
```

- 하지만 위의 구현은, `Django REST Framework` 를 사용하는 경우에만 적용됩니다.
- 그리하여, `Django` 에서 반환하는 404, 500 등의 예외에 대해서는 별도로 `handler` 를 작성했습니다.
- 아쉬운 점은, 문서화 도구인 `drf-spectacular` 가 그것에 대한 처리를 별도로 해 주지 못한다는 것입니다.
    - 관련 Github issue : https://github.com/tfranzel/drf-spectacular/issues/429
    - 그리하여 현재 생성되는 OpenAPI 사양은 완벽하지 않습니다.

#### 코드의 스타일을 어떻게 통일할까?

- `black` 을 사용하여 코드의 스타일을 통일했습니다.
- `isort` 를 사용하여 코드의 import 순서를 통일했습니다.
- `flake8` 을 사용하여 코드의 스타일을 검사했습니다.
- `pre-commit` 을 사용하여 위의 세 가지를 자동으로 수행하도록 했습니다.

#### 내 코드가 잘 작동하는지 어떻게 확인할까?

- `Unittest` 를 사용하여 코드의 테스트를 작성했습니다.
- 응답 포맷이 원하는 대로 나오는 것인지 테스트하기 위해서, 응답 포맷을 테스트하는 메서드를 가지는 기본 클래스를 작성했습니다.

```python
class BaseAPITestCase(APITestCase):
    def _test_response_format(self, response):
        """
        응답 포맷이 올바른지 테스트하는 메서드입니다.

        1. STATUS_CODE 가 204 인 경우
        2. STATUS_CODE 가 200 혹은 201 인 경우
        3. 그 외의 경우 ( 400, 401, 403, 404, 500 등 )
        """

        if response.status_code == status.HTTP_204_NO_CONTENT:
            self._test_204_response_format(response)
        elif (
                response.status_code == status.HTTP_200_OK
                or response.status_code == status.HTTP_201_CREATED
        ):
            self._test_success_response_format(response)
        else:
            self._test_error_response_format(response)

    def _test_success_response_format(self, response):
        """
        201 혹은 201 응답인 경우, "data" 키는 null 이 들어가면 안 됩니다.
        """
        self._test_base_response_format(response)
        self.assertIsNotNone(response.data["data"])

    def _test_error_response_format(self, response):
        """
        에러 응답인 경우, "data" 키에는 null 이 들어가야 합니다.
        """
        self._test_base_response_format(response)
        self.assertIsNone(response.data["data"])

    def _test_base_response_format(self, response):
        """
        {
            "meta": {
                "code": 200,
                "message": "ok",
            },
            "data": {"products": [...]},
        }
        위의 형식에 따른 키를 가지고 있는지 테스트합니다.
        """
        self.assertIn("meta", response.data)
        self.assertIn("code", response.data["meta"])
        self.assertIn("message", response.data["meta"])
        self.assertIn("data", response.data)

    def _test_204_response_format(self, response):
        """
        상태 코드가 204 NO CONTENT 인 경우를 테스트합니다.
        """

        self.assertEqual(response.data, None)
```

- 현재, 31개의 테스트 케이스를 통과했습니다.

## 실행 방법을 알려주세요. 사용해 보고 싶어요!

### 1. 환경 변수 설정

`.env.example` 파일의 예시에 맞춰 `.env` 파일을 생성합니다.

```.env
SECRET_KEY= # Django 에서 사용될 SECRET_KEY 입니다.

DJANGO_SUPERUSER_MOBILE= # Django 에서 사용될 슈퍼유저의 전화번호입니다.
DJANGO_SUPERUSER_PASSWORD= # Django 에서 사용될 슈퍼유저의 비밀번호입니다.

# 데이터베이스 접속 정보입니다. Django 와 MySQL 컨테이너 둘 다 이 환경 변수를 공유합니다.
MYSQL_ROOT_PASSWORD=root-password
MYSQL_DATABASE=cafehere-db
MYSQL_USER=cafehere-admin
MYSQL_PASSWORD=root-password
```

### 2. Docker Compose 실행

아래의 명령어를 작업 디렉토리에서 수행하여 컨테이너를 실행합니다.

현재 `Docker Compose` 는 `Mac M1` 전용으로 작성되었습니다. (MySQL 컨테이너)

```bash
docker compose up -d
```

### 3. django 셋업

아래의 명령어를 작업 디렉토리에서 수행하여 데이터베이스 마이그레이션, 슈퍼유저 생성, 정적 파일 수집을 수행합니다.

```bash
docker compose run cafehere-was python manage.py migrate --settings core.settings.production &&\
docker compose run cafehere-was python manage.py createsuperuser --no-input --settings core.settings.production&&\
docker compose run cafehere-was python manage.py collectstatic --settings core.settings.production
```

http://127.0.0.1:8000/ 에 접속해 보세요. :) 멋진 Swagger UI 가 나올 겁니다.

현재 Swagger UI 는 `drf-spectacular` 를 사용하여 자동으로 생성되고 있습니다만, `Custom JSON Renderer` 를 사용하기 때문에 완벽하지 않습니다.
이에 유의해 주세요!


