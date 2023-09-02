import uuid

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse

from apps.cafes.models import Cafe
from apps.products.models import Category, Product
from apps.products.urls import PRODUCT_LIST_URL_NAME
from core.utils.test import BaseAPITestCase

CAFE_DETAIL_URL_NAME = "cafe-detail"
CATEGORY_LIST_URL_NAME = "category-list"
CATEGORY_DETAIL_URL_NAME = "category-detail"

User = get_user_model()


class CategoryListTestCase(BaseAPITestCase):
    """
    카테고리 목록 읽기 테스트
    """

    def setUp(self):
        """
        테스트에 필요한 유저, 카페, 카테고리를 생성
        """
        self.owner_james = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )
        self.cafe_for_james = Cafe.objects.create(
            name="James's Cafe", owner=self.owner_james
        )
        self.category_for_james = Category.objects.create(
            name="Coffee", cafe=self.cafe_for_james
        )

        self.owner_jenny = User.objects.create_user(
            mobile="+82-1012345679", password="test_password"
        )
        self.cafe_for_jenny = Cafe.objects.create(
            name="Jenny's Cafe", owner=self.owner_jenny
        )
        self.category_for_jenny = Category.objects.create(
            name="Tea", cafe=self.cafe_for_jenny
        )

    def test_list_with_login(self):
        """
        로그인한 사용자만 목록을 조회할 수 있고,
        해당 카페의 카테고리만 조회할 수 있습니다.
        카페를 조회하려면 카페의 owner 이어야 합니다.
        """

        url = reverse(
            CATEGORY_LIST_URL_NAME,
            kwargs={"cafe_uuid": self.cafe_for_james.uuid},
        )

        # 로그인하지 않은 상태에서는 접근할 수 없습니다.
        response = self.client.get(url, cafe_uuid=self.cafe_for_james.uuid)
        self._test_response_format(response)
        self.assertEqual(response.status_code, 401)

        # 로그인합니다.
        self.client.force_login(self.owner_james)

        # 자신의 카페의 카테고리 목록을 조회할 수 있습니다.
        response = self.client.get(url)
        self._test_response_format(response)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], self.category_for_james.name)

        # 다른 카페의 카테고리 목록은 조회할 수 없습니다.
        url = reverse(
            CATEGORY_LIST_URL_NAME,
            kwargs={"cafe_uuid": self.cafe_for_jenny.uuid},
        )
        response = self.client.get(url)
        self._test_response_format(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_without_login(self):
        """
        로그인하지 않은 사용자는 카테고리 목록을 조회할 수 없습니다.
        """
        url = reverse(
            CATEGORY_LIST_URL_NAME,
            kwargs={"cafe_uuid": self.cafe_for_james.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_list_with_invalid_uuid(self):
        """
        유효하지 않은 uuid 를 가진 카페의 카테고리 목록은 조회할 수 없습니다.
        """
        url = reverse(
            CATEGORY_LIST_URL_NAME,
            kwargs={"cafe_uuid": uuid.uuid4()},
        )
        self.client.force_login(self.owner_james)
        response = self.client.get(url)
        self._test_response_format(response)
        self.assertEqual(response.status_code, 404)


class ProductListTestCase(BaseAPITestCase):
    """
    상품 목록 읽기 테스트
    """

    def setUp(self):
        """
        테스트에 필요한 유저, 카페, 카테고리, 상품을 생성
        """
        self.owner_james = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )
        self.cafe_for_james = Cafe.objects.create(
            name="James's Cafe", owner=self.owner_james
        )
        self.category_for_james = Category.objects.create(
            name="Coffee", cafe=self.cafe_for_james
        )
        self.category_for_james2 = Category.objects.create(
            name="Cake", cafe=self.cafe_for_james
        )
        self.product_for_james1 = Product.objects.create(
            name="아메리카노",
            description="Icy Americano!",
            cost=2000,
            price=3000,
            expireation_date=timezone.now(),
            category=self.category_for_james,
        )
        self.product_for_james2 = Product.objects.create(
            name="에스프레소",
            description="Simple Espresso!",
            cost=2000,
            price=3000,
            expireation_date=timezone.now(),
            category=self.category_for_james,
        )
        self.product_for_james3 = Product.objects.create(
            name="초코케이크",
            description="Chocolate Cake!",
            cost=2000,
            price=3000,
            expireation_date=timezone.now(),
            category=self.category_for_james2,
        )

        self.owner_jenny = User.objects.create_user(
            mobile="+82-1012345679", password="test_password"
        )
        self.cafe_for_jenny = Cafe.objects.create(
            name="Jenny's Cafe", owner=self.owner_jenny
        )
        self.category_for_jenny = Category.objects.create(
            name="Tea", cafe=self.cafe_for_jenny
        )
        self.product_for_jenny = Product.objects.create(
            name="녹차",
            cost=2000,
            price=4000,
            expireation_date=timezone.now(),
            category=self.category_for_jenny,
        )

    def test_list_with_login(self):
        """
        로그인한 사용자만 목록을 조회할 수 있고,
        해당 카페의 상품만 조회할 수 있습니다.
        카페를 조회하려면 카페의 owner 이어야 합니다.
        """

        url = reverse(
            PRODUCT_LIST_URL_NAME,
            kwargs={"cafe_uuid": self.cafe_for_james.uuid},
        )

        # 로그인하지 않은 상태에서는 접근할 수 없습니다.
        response = self.client.get(url, cafe_uuid=self.cafe_for_james.uuid)
        self._test_response_format(response)
        self.assertEqual(response.status_code, 401)

        # 로그인합니다.
        self.client.force_login(self.owner_james)

        # 자신의 카페의 상품 목록을 조회할 수 있습니다.
        response = self.client.get(url)
        self._test_response_format(response)
        self.assertEqual(len(response.data["data"]), 3)

    def test_list_another_cafe(self):
        """
        다른 카페의 상품 목록은 조회할 수 없습니다.
        """
        url = reverse(
            PRODUCT_LIST_URL_NAME,
            kwargs={"cafe_uuid": self.cafe_for_jenny.uuid},
        )
        self.client.force_login(self.owner_james)
        response = self.client.get(url)
        self._test_response_format(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.owner_jenny)
        response = self.client.get(url)
        self._test_response_format(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_list_with_filtering_category(self):
        """
        카테고리 필터링이 가능한지 테스트합니다.
        카테고리 이름으로 검색을 수행하면, 해당 카테고리에 속한 상품만 검색되어야 합니다.
        """
        url = reverse(
            PRODUCT_LIST_URL_NAME,
            kwargs={"cafe_uuid": self.cafe_for_james.uuid},
        )
        self.client.force_login(self.owner_james)
        response = self.client.get(url, {"category": self.category_for_james2.name})
        self._test_response_format(response)
        self.assertEqual(len(response.data["data"]), 1)

    def test_list_with_filtering_initial_consonant(self):
        """
        한글 초성으로 검색이 가능한지 테스트합니다.
        """
        url = reverse(
            PRODUCT_LIST_URL_NAME,
            kwargs={"cafe_uuid": self.cafe_for_james.uuid},
        )
        self.client.force_login(self.owner_james)
        response = self.client.get(url, {"search": "ㅇㅅㅍㄹ"})
        self._test_response_format(response)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], self.product_for_james2.name)

    def test_list_with_filtering_name(self):
        """
        이름으로 검색이 가능한지 테스트합니다.
        """
        url = reverse(
            PRODUCT_LIST_URL_NAME,
            kwargs={"cafe_uuid": self.cafe_for_james.uuid},
        )
        self.client.force_login(self.owner_james)
        response = self.client.get(f"{url}?search=아메리카노")
        self._test_response_format(response)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], self.product_for_james1.name)

    def test_list_with_filtering_not_filter_another_cafe(self):
        """
        다른 카페의 상품은 검색되지 않아야 합니다.
        """
        url = reverse(
            PRODUCT_LIST_URL_NAME,
            kwargs={"cafe_uuid": self.cafe_for_jenny.uuid},
        )
        self.client.force_login(self.owner_james)
        response = self.client.get(url, {"search": "녹차"})
        self._test_response_format(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProductDetailTestCase(BaseAPITestCase):
    """
    상품 상세 조회 테스트
    """

    def setUp(self):
        """
        테스트에 필요한 유저, 카페, 카테고리, 상품을 생성
        """
        self.owner_james = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )
        self.cafe_for_james = Cafe.objects.create(
            name="James's Cafe", owner=self.owner_james
        )
        self.category_for_james = Category.objects.create(
            name="Coffee", cafe=self.cafe_for_james
        )
        self.category_for_james2 = Category.objects.create(
            name="Cake", cafe=self.cafe_for_james
        )
        self.product_for_james1 = Product.objects.create(
            name="아메리카노",
            description="Icy Americano!",
            cost=2000,
            price=3000,
            expireation_date=timezone.now(),
            category=self.category_for_james,
        )
        self.product_for_james2 = Product.objects.create(
            name="에스프레소",
            description="Simple Espresso!",
            cost=2000,
            price=3000,
            expireation_date=timezone.now(),
            category=self.category_for_james,
        )
        self.product_for_james3 = Product.objects.create(
            name="초코케이크",
            description="Chocolate Cake!",
            cost=2000,
            price=3000,
            expireation_date=timezone.now(),
            category=self.category_for_james2,
        )

        self.owner_jenny = User.objects.create_user(
            mobile="+82-1012345679", password="test_password"
        )
        self.cafe_for_jenny = Cafe.objects.create(
            name="Jenny's Cafe", owner=self.owner_jenny
        )
        self.category_for_jenny = Category.objects.create(
            name="Tea", cafe=self.cafe_for_jenny
        )
        self.product_for_jenny = Product.objects.create(
            name="녹차",
            cost=2000,
            price=4000,
            expireation_date=timezone.now(),
            category=self.category_for_jenny,
        )

    def test_detail_with_login(self):
        """
        로그인한 사용자만 상세 조회할 수 있고,
        해당 카페의 상세정보를 잘 조회할 수 있어야 합니다.
        """
        url = reverse(
            "product-detail",
            kwargs={
                "cafe_uuid": self.cafe_for_james.uuid,
                "product_id": self.product_for_james1.id,
            },
        )

        # 로그인하지 않은 상태에서는 접근할 수 없습니다.
        response = self.client.get(url)
        self._test_response_format(response)
        self.assertEqual(response.status_code, 401)

        # 로그인합니다.
        self.client.force_login(self.owner_james)

        # 자신의 카페의 상품 상세정보를 조회할 수 있습니다.
        response = self.client.get(url)
        self._test_response_format(response)
        self.assertEqual(response.data["data"]["name"], self.product_for_james1.name)

        # 다른 카페의 상품 상세정보는 조회할 수 없습니다.
        url = reverse(
            "product-detail",
            kwargs={
                "cafe_uuid": self.cafe_for_jenny.uuid,
                "product_id": self.product_for_jenny.id,
            },
        )
        response = self.client.get(url)
        self._test_response_format(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProductDeleteTestCase(BaseAPITestCase):
    """
    상품 삭제 테스트
    """

    def setUp(self):
        """
        테스트에 필요한 유저, 카페, 카테고리, 상품을 생성
        """
        self.owner_james = User.objects.create_user(
            mobile="+82-1012345678", password="test_password"
        )
        self.cafe_for_james = Cafe.objects.create(
            name="James's Cafe", owner=self.owner_james
        )
        self.category_for_james = Category.objects.create(
            name="Coffee", cafe=self.cafe_for_james
        )
        self.category_for_james2 = Category.objects.create(
            name="Cake", cafe=self.cafe_for_james
        )
        self.product_for_james1 = Product.objects.create(
            name="아메리카노",
            description="Icy Americano!",
            cost=2000,
            price=3000,
            expireation_date=timezone.now(),
            category=self.category_for_james,
        )
        self.product_for_james2 = Product.objects.create(
            name="에스프레소",
            description="Simple Espresso!",
            cost=2000,
            price=3000,
            expireation_date=timezone.now(),
            category=self.category_for_james,
        )
        self.product_for_james3 = Product.objects.create(
            name="초코케이크",
            description="Chocolate Cake!",
            cost=2000,
            price=3000,
            expireation_date=timezone.now(),
            category=self.category_for_james2,
        )

        self.owner_jenny = User.objects.create_user(
            mobile="+82-1012345679", password="test_password"
        )
        self.cafe_for_jenny = Cafe.objects.create(
            name="Jenny's Cafe", owner=self.owner_jenny
        )
        self.category_for_jenny = Category.objects.create(
            name="Tea", cafe=self.cafe_for_jenny
        )
        self.product_for_jenny = Product.objects.create(
            name="녹차",
            cost=2000,
            price=4000,
            expireation_date=timezone.now(),
            category=self.category_for_jenny,
        )

    def test_delete_own_product(self):
        """
        자신의 상품만 삭제할 수 있습니다.
        """
        url = reverse(
            "product-detail",
            kwargs={
                "cafe_uuid": self.cafe_for_james.uuid,
                "product_id": self.product_for_james1.id,
            },
        )
        self.client.force_login(self.owner_james)
        response = self.client.delete(url)
        self._test_response_format(response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 삭제된 상품은 조회할 수 없습니다.

        response = self.client.delete(url)
        self._test_response_format(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_another_cafe_product(self):
        """
        자신이 소유하고 있지 않은 카페의 상품은 삭제할 수 없습니다.
        """
        url = reverse(
            "product-detail",
            kwargs={
                "cafe_uuid": self.cafe_for_jenny.uuid,
                "product_id": self.product_for_jenny.id,
            },
        )
        self.client.force_login(self.owner_james)
        response = self.client.delete(url)
        self._test_response_format(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
