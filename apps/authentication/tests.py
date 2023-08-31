from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

from core.utils.test import BaseAPITestCase

REGISTER_URL_NAME = "register"
LOGIN_URL_NAME = "login"
REFRESH_URL_NAME = "refresh"
LOGOUT_URL_NAME = "logout"

User = get_user_model()


class RegisterAPITestCase(BaseAPITestCase):
    def test_register_with_valid_data(self):
        """
        유효한 전화번호와 비밀번호를 사용하여 회원가입을 할 수 있는지 테스트
        """

        valid_data = {
            "mobile": "+82-1012345678",
            "password": "test_password",
        }

        url = reverse(REGISTER_URL_NAME)
        response = self.client.post(url, data=valid_data)
        self._test_response_format(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_with_invalid_mobile(self):
        """
        유효하지 않은 전화번호로 회원가입을 할 수 없는지 테스트
        """

        invalid_data = {
            "mobile": "invalid_mobile",
            "password": "test_password",
        }

        url = reverse(REGISTER_URL_NAME)
        response = self.client.post(url, data=invalid_data)
        self._test_response_format(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_password_hashed(self):
        """
        비밀번호가 해시되어 저장되는지 테스트
        """

        valid_data = {
            "mobile": "+82-1012345678",
            "password": "test_password",
        }

        url = reverse(REGISTER_URL_NAME)
        response = self.client.post(url, data=valid_data)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(User.objects.get().password, valid_data["password"])


class LoginTestCase(BaseAPITestCase):
    def setUp(self):
        """
        테스트에 필요한 유저를 생성
        """
        self.user = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )

    def test_login_with_valid_data(self):
        """
        유효한 전화번호와 비밀번호로 로그인이 가능한지 테스트
        """

        valid_data = {
            "mobile": "+82-1012345678",
            "password": "test_password",
        }

        url = reverse(LOGIN_URL_NAME)
        response = self.client.post(url, data=valid_data)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])

    def test_login_with_invalid_mobile(self):
        """
        유효하지 않은 전화번호로 로그인이 불가능한지 테스트
        """

        invalid_data = {
            "mobile": "invalid_mobile",
            "password": "test_password",
        }

        url = reverse(LOGIN_URL_NAME)
        response = self.client.post(url, data=invalid_data)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_invalid_password(self):
        """
        유효하지 않은 비밀번호로 로그인이 불가능한지 테스트
        """

        invalid_data = {
            "mobile": "+82-1012345678",
            "password": "invalid_password",
        }

        url = reverse(LOGIN_URL_NAME)
        response = self.client.post(url, data=invalid_data)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutTestCase(BaseAPITestCase):
    def setUp(self):
        """
        테스트에 필요한 유저를 생성
        """
        self.user = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )

    def test_logout(self):
        """
        로그아웃이 가능한지 테스트

        1. 사용자가 로그인하면, 액세스 토큰과 리프레시 토큰을 발급받는다.
        2. 사용자가 로그아웃을 하면, 리프레시 토큰은 블랙리스트에 추가된다.
        3. 블랙리스트에 추가된 리프레시 토큰은 더 이상 사용할 수 없다.
        """

        # 1. 사용자가 로그인하면, 액세스 토큰과 리프레시 토큰을 발급받는다.
        login_data = {
            "mobile": "+82-1012345678",
            "password": "test_password",
        }
        login_url = reverse(LOGIN_URL_NAME)
        login_response = self.client.post(login_url, data=login_data)
        self._test_response_format(login_response)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data["data"])
        self.assertIn("refresh", login_response.data["data"])

        # 2. 사용자가 로그아웃을 하면, 리프레시 토큰은 블랙리스트에 추가된다.
        logout_url = reverse(LOGOUT_URL_NAME)
        logout_data = {
            "refresh": login_response.data["data"]["refresh"],
        }
        logout_response = self.client.post(logout_url, data=logout_data)
        self._test_response_format(logout_response)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        # 3. 블랙리스트에 추가된 리프레시 토큰은 더 이상 사용할 수 없다.
        refresh_url = reverse(REFRESH_URL_NAME)
        refresh_data = {
            "refresh": login_response.data["data"]["refresh"],
        }
        refresh_response = self.client.post(refresh_url, data=refresh_data)
        self._test_response_format(logout_response)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_rotation(self):
        """
        리프레시 토큰 로테이션 테스트

        1. 사용자가 로그인하면, 액세스 토큰과 리프레시 토큰을 발급받는다.
        2. 사용자가 가지고 있는 리프레시 토큰을 사용해 액세스 토큰을 갱신한다.
        3. 원래 가지고 있던 리프레시 토큰은 더 이상 액세스 토큰 갱신을 위해 사용할 수 없다.
        """

        # 1. 사용자가 로그인하면, 액세스 토큰과 리프레시 토큰을 발급받는다.
        login_data = {
            "mobile": "+82-1012345678",
            "password": "test_password",
        }
        login_url = reverse(LOGIN_URL_NAME)
        login_response = self.client.post(login_url, data=login_data)
        self._test_response_format(login_response)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data["data"])
        self.assertIn("refresh", login_response.data["data"])

        # 2. 사용자가 가지고 있는 리프레시 토큰을 사용해 액세스 토큰을 갱신한다.
        refresh_url = reverse(REFRESH_URL_NAME)
        refresh_data = {
            "refresh": login_response.data["data"]["refresh"],
        }
        refresh_response = self.client.post(refresh_url, data=refresh_data)
        self._test_response_format(refresh_response)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data["data"])
        self.assertIn("refresh", refresh_response.data["data"])

        # 3. 원래 가지고 있던 리프레시 토큰은 더 이상 액세스 토큰 갱신을 위해 사용할 수 없다.
        refresh_response = self.client.post(refresh_url, data=refresh_data)
        self._test_response_format(refresh_response)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
