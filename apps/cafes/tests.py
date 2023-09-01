from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

from apps.cafes.models import Cafe
from apps.cafes.urls import CAFE_DETAIL_URL_NAME, CAFE_LIST_URL_NAME, CAFE_URL_KEYWORD
from core.utils.test import BaseAPITestCase

User = get_user_model()


class CafeCreateTestCase(BaseAPITestCase):
    def setUp(self):
        """
        테스트에 필요한 유저를 생성
        """
        self.cafe_owner_james = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )
        self.cafe_owner_jenny = User.objects.create_user(
            mobile="+82-1012345679", password="test_password"
        )

    def test_create_cafe_with_valid_data(self):
        """
        유효한 이름으로 카페를 생성할 수 있는지 테스트합니다.
        """
        valid_data = {
            "name": "My Cafe",
        }

        url = reverse(CAFE_LIST_URL_NAME)

        before_count = Cafe.objects.count()

        # 로그인 한 사용자만 카페를 생성할 수 있습니다.
        self.client.force_login(self.cafe_owner_james)
        response = self.client.post(url, data=valid_data)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 카페가 생성되었습니다.
        self.assertEqual(Cafe.objects.count(), before_count + 1)

    def test_create_cafe_with_invalid_data(self):
        """
        모델의 제약 조건에 따라, 30자가 넘는 이름으로 카페를 생성할 수 없습니다.
        """
        invalid_data = {
            "name": "how dare you create this cafe with current cafe name? this is over 30 characters!",
        }

        url = reverse(CAFE_LIST_URL_NAME)

        before_count = Cafe.objects.count()

        # 로그인 한 사용자만 카페를 생성할 수 있습니다.
        self.client.force_login(self.cafe_owner_james)
        response = self.client.post(url, data=invalid_data)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 카페가 생성되지 않았습니다.
        self.assertEqual(Cafe.objects.count(), before_count)

    def test_create_cafe_withdout_login(self):
        """
        로그인하지 않은 사용자는 카페를 생성할 수 없습니다.
        """
        valid_data = {
            "name": "My Cafe",
        }

        url = reverse(CAFE_LIST_URL_NAME)

        before_count = Cafe.objects.count()

        # 로그인하지 않은 사용자는 카페를 생성할 수 없습니다.
        response = self.client.post(url, data=valid_data)
        self._test_response_format(response)

        # 전해진 권한 정보가 없으므로 401 UNAUTHORIZED가 반환되어야 합니다.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 카페가 생성되지 않았습니다.
        self.assertEqual(Cafe.objects.count(), before_count)

    def test_create_cafe_with_duplicated_name(self):
        """
        한 사용자는 중복된 이름의 카페를 생성할 수 없습니다.
        """
        valid_data = {
            "name": "My Cafe",
        }

        Cafe.objects.create(name="My Cafe", owner=self.cafe_owner_james)

        url = reverse(CAFE_LIST_URL_NAME)
        invalid_data = {
            "name": "My Cafe",
        }

        # 로그인 한 사용자만 카페를 생성할 수 있습니다.
        self.client.force_login(self.cafe_owner_james)
        response = self.client.post(url, data=invalid_data)
        self._test_response_format(response)

        # 같은 이름으로 카페를 생성할 수 없습니다.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 하지만, 다른 사용자 jenny는 같은 이름으로 카페를 생성할 수 있습니다.
        self.client.force_login(self.cafe_owner_jenny)
        response = self.client.post(url, data=invalid_data)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CafeListTestCase(BaseAPITestCase):
    def setUp(self):
        """
        테스트에 필요한 유저를 생성
        """
        self.cafe_owner_james = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )
        self.cafe_owner_jenny = User.objects.create_user(
            mobile="+82-1012345679", password="test_password"
        )

    def test_list_only_show_per_user(self):
        """
        로그인한 사용자가 소유한 카페만 조회할 수 있습니다.
        """

        Cafe.objects.bulk_create(
            [
                Cafe(name=f"James Cafe {i}", owner=self.cafe_owner_james)
                for i in range(0, 10)
            ]
        )
        Cafe.objects.bulk_create(
            [
                Cafe(name=f"Jenny Cafe {i}", owner=self.cafe_owner_jenny)
                for i in range(0, 1)
            ]
        )

        url = reverse(CAFE_LIST_URL_NAME)

        # James는 James의 카페만 조회할 수 있습니다.
        self.client.force_login(self.cafe_owner_james)
        response = self.client.get(url)
        self._test_response_format(response)

        # 응답으로 온 카페 정보가 James의 카페인지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for cafe in response.data["data"]:
            self.assertIn("James Cafe", cafe["name"]) and self.assertNotIn(
                "Jenny Cafe", cafe["name"]
            )

        # James 의 카페 개수는 10개 입니다.
        self.assertEqual(len(response.data["data"]), 10)

    def test_list_without_login(self):
        """
        로그인하지 않은 사용자는 카페를 조회할 수 없습니다.
        """
        url = reverse(CAFE_LIST_URL_NAME)

        # 로그인하지 않은 사용자는 카페를 조회할 수 없습니다.
        response = self.client.get(url)
        self._test_response_format(response)

        # 전해진 권한 정보가 없으므로 401 UNAUTHORIZED가 반환되어야 합니다.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CafeRetrieveTestCase(BaseAPITestCase):
    """
    카페 상세 조회 테스트
    """

    def setUp(self):
        """
        테스트에 필요한 유저를 생성
        """
        self.cafe_owner_james = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )
        self.cafe_owner_jenny = User.objects.create_user(
            mobile="+82-1012345679", password="test_password"
        )

    def test_retrieve_cafe(self):
        """
        로그인한 사용자는 소유한 카페의 상세 정보를 조회할 수 있습니다.
        """

        james_cafe = Cafe.objects.create(name="James Cafe", owner=self.cafe_owner_james)
        jenny_cafe = Cafe.objects.create(name="Jenny Cafe", owner=self.cafe_owner_jenny)

        url = reverse(CAFE_DETAIL_URL_NAME, kwargs={CAFE_URL_KEYWORD: james_cafe.uuid})

        # James는 James의 카페만 조회할 수 있습니다.
        self.client.force_login(self.cafe_owner_james)
        response = self.client.get(url)
        self._test_response_format(response)

        # 응답으로 온 카페 정보가 James의 카페인지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["name"], james_cafe.name)

        # Jenny는 James의 카페를 조회할 수 없습니다.
        self.client.force_login(self.cafe_owner_jenny)
        response = self.client.get(url)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Jenny는 Jenny의 카페만 조회할 수 있습니다.
        url = reverse(CAFE_DETAIL_URL_NAME, kwargs={CAFE_URL_KEYWORD: jenny_cafe.uuid})
        response = self.client.get(url)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["name"], jenny_cafe.name)

    def test_retrieve_cafe_without_login(self):
        """
        로그인하지 않은 사용자는 카페를 조회할 수 없습니다.
        """
        james_cafe = Cafe.objects.create(name="James Cafe", owner=self.cafe_owner_james)

        url = reverse(CAFE_DETAIL_URL_NAME, kwargs={CAFE_URL_KEYWORD: james_cafe.uuid})

        # 로그인하지 않은 사용자는 카페를 조회할 수 없습니다.
        response = self.client.get(url)
        self._test_response_format(response)

        # 전해진 권한 정보가 없으므로 401 UNAUTHORIZED가 반환되어야 합니다.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CafeUpdateTestCase(BaseAPITestCase):
    """
    카페 수정 테스트
    """

    def setUp(self):
        """
        테스트에 필요한 유저를 생성
        """
        self.cafe_owner_james = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )
        self.cafe_owner_jenny = User.objects.create_user(
            mobile="+82-1012345679", password="test_password"
        )

    def test_update_cafe(self):
        """
        로그인한 사용자는 소유한 카페의 정보를 수정할 수 있습니다.
        """

        james_cafe = Cafe.objects.create(name="James Cafe", owner=self.cafe_owner_james)
        jenny_cafe = Cafe.objects.create(name="Jenny Cafe", owner=self.cafe_owner_jenny)

        url = reverse(CAFE_DETAIL_URL_NAME, kwargs={CAFE_URL_KEYWORD: james_cafe.uuid})

        # James는 James의 카페만 수정할 수 있습니다.
        self.client.force_login(self.cafe_owner_james)
        response = self.client.put(url, data={"name": "James Cafe 2"})
        self._test_response_format(response)

        # 응답으로 온 카페 정보가 James의 카페인지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["name"], "James Cafe 2")

        # Jenny는 James의 카페를 수정할 수 없습니다.
        self.client.force_login(self.cafe_owner_jenny)
        response = self.client.put(url, data={"name": "James Cafe 3"})
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Jenny는 Jenny의 카페만 수정할 수 있습니다.
        url = reverse(CAFE_DETAIL_URL_NAME, kwargs={CAFE_URL_KEYWORD: jenny_cafe.uuid})
        response = self.client.put(url, data={"name": "Jenny Cafe 2"})
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["name"], "Jenny Cafe 2")

    def test_update_cafe_without_login(self):
        """
        로그인하지 않은 사용자는 카페를 수정할 수 없습니다.
        """
        james_cafe = Cafe.objects.create(name="James Cafe", owner=self.cafe_owner_james)

        url = reverse(CAFE_DETAIL_URL_NAME, kwargs={CAFE_URL_KEYWORD: james_cafe.uuid})

        # 로그인하지 않은 사용자는 카페를 수정할 수 없습니다.
        response = self.client.put(url, data={"name": "James Cafe 2"})
        self._test_response_format(response)

        # 전해진 권한 정보가 없으므로 401 UNAUTHORIZED가 반환되어야 합니다.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_cafe_with_invalid_data(self):
        """
        유효하지 않은 이름으로 카페를 수정할 수 없습니다.
        """
        james_cafe = Cafe.objects.create(name="James Cafe", owner=self.cafe_owner_james)

        url = reverse(CAFE_DETAIL_URL_NAME, kwargs={CAFE_URL_KEYWORD: james_cafe.uuid})

        # James는 James의 카페만 수정할 수 있습니다.
        self.client.force_login(self.cafe_owner_james)
        response = self.client.put(
            url,
            data={
                "name": "how dare you create this cafe with current cafe name? this is over 30 characters!"
            },
        )
        self._test_response_format(response)

        # API 는 400 BAD REQUEST를 반환합니다.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CafeDestroyTestCase(BaseAPITestCase):
    """
    카페 삭제 테스트
    """

    def setUp(self):
        """
        테스트에 필요한 유저를 생성
        """
        self.cafe_owner_james = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )
        self.cafe_owner_jenny = User.objects.create_user(
            mobile="+82-1012345679", password="test_password"
        )

    def test_destroy_cafe(self):
        """
        로그인한 사용자는 소유한 카페를 삭제할 수 있습니다.
        """

        james_cafe = Cafe.objects.create(name="James Cafe", owner=self.cafe_owner_james)
        jenny_cafe = Cafe.objects.create(name="Jenny Cafe", owner=self.cafe_owner_jenny)

        url = reverse(CAFE_DETAIL_URL_NAME, kwargs={CAFE_URL_KEYWORD: james_cafe.uuid})

        # James는 James의 카페만 삭제할 수 있습니다.
        self.client.force_login(self.cafe_owner_james)
        response = self.client.delete(url)
        self._test_response_format(response)

        # 응답으로 온 카페 정보가 James의 카페인지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Jenny는 James의 카페를 삭제할 수 없습니다.
        self.client.force_login(self.cafe_owner_jenny)
        response = self.client.delete(url)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Jenny는 Jenny의 카페만 삭제할 수 있습니다.
        url = reverse(CAFE_DETAIL_URL_NAME, kwargs={CAFE_URL_KEYWORD: jenny_cafe.uuid})
        response = self.client.delete(url)
        self._test_response_format(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_cafe_without_login(self):
        """
        로그인하지 않은 사용자는 카페를 삭제할 수 없습니다.
        """
        james_cafe = Cafe.objects.create(name="James Cafe", owner=self.cafe_owner_james)

        url = reverse(CAFE_DETAIL_URL_NAME, kwargs={CAFE_URL_KEYWORD: james_cafe.uuid})

        # 로그인하지 않은 사용자는 카페를 삭제할 수 없습니다.
        response = self.client.delete(url)
        self._test_response_format(response)

        # 전해진 권한 정보가 없으므로 401 UNAUTHORIZED가 반환되어야 합니다.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
