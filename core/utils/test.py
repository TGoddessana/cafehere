from rest_framework import status
from rest_framework.test import APITestCase


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
