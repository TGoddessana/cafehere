# Your Cafe is right HERE! - CafeHere

korean version: [README.kor.md](readme/README.kor.md)

## What is this?

This is an `HTTP API` server for owners who want to register products and operate their own cafes.  
You can use this server to manage your cafe's products.

## Tell me more.

### Member-related API

- Owners can sign up with their phone number and password.
    - When signing up, the phone number must follow the `E.164`
      format. (https://www.itu.int/rec/T-REC-E.164-201011-I/en)
    - When signing up, the password is stored securely through one-way encryption.
- Owners can log in with their phone number and password.
    - Login is implemented using JWT.
    - Access Token expires in 5 minutes, and Refresh Token expires in 1 week.
    - Once a Refresh Token is used, it cannot be used again (Refresh Token Rotation).
    - Users can log out by adding the Refresh Token to the blacklist.

### Cafe-related API

- After logging in, owners can perform the following actions related to cafes:
    - Register a cafe.
    - Partially modify the cafe's attributes.
    - Retrieve detailed information about registered cafes.
    - Delete registered cafes.
    - If not logged in, owners cannot use cafe-related APIs.
    - Even if logged in, they cannot access other owners' cafes.

### Product-related API

- After logging in, owners can perform the following actions related to products:
    - Register a product.
    - Partially modify the product's attributes.
    - Retrieve a list of registered products. Supports cursor-based paging.
    - Search for registered products. Supports initial search and name search.
    - Retrieve detailed information about registered products.
    - Delete registered products.
    - If not logged in, owners cannot use product-related APIs.
    - Even if logged in, they cannot access other owners' cafe products.
- After logging in, owners can perform the following actions related to categories:
    - Register a category.
    - Partially modify the category's attributes.
    - Retrieve a list of registered categories.
    - Retrieve detailed information about registered categories.
    - If not logged in, owners cannot use category-related APIs.
    - Even if logged in, they cannot access other owners' categories.
- After logging in, owners can perform the following actions related to product options:
    - Register an option group.
    - Delete an option group.
    - If not logged in, owners cannot use product option-related APIs.
    - Even if logged in, they cannot access other owners' product option information.

## What technologies were used?

The main language used is `Python 3.11`.

The server is implemented using `Django` and `Django REST Framework`.

`Docker` and `Docker Compose` are used to run the server regardless of the language.

`MySQL 5.7` is used as the database.

## Were there any challenges?

#### 1. How to validate the phone number format?

- Validating phone numbers was a significant challenge. It had to consider both domestic and international numbers.
- Phone numbers must follow the `E.164` format. (https://www.itu.int/rec/T-REC-E.164-201011-I/en)
- A hyphen (-) must be included between the "international code" and the "phone number."
- In the end, validation was implemented using the regular expression `r"^\+[0-9]{1,4}+-[0-9]{1,14}$"`.
- One limitation is that it cannot verify if the country code corresponds to a real country.

#### 2. Can owners have only one cafe?

- Currently, owners can have multiple cafes.
- For those who are entrepreneurial, they can operate multiple cafes.
- Therefore, I decided to implement the "Open My Cafe API" first.

#### 3. How to implement product options?

- For example, for coffee, options like "size," "extra shot," and "syrup" can be selected.
- Or for cakes, options like "size" and "topping" can be selected.
- So, I created option groups to group options and implemented option management through the option group API.
- Additionally, I ensured that the same option group name cannot exist in the same cafe in the database.
- As a result, one cafe can have unique-named option groups, and one option group can have unique-named options.
- One product can have multiple option groups, and one option group can have multiple products.

#### 4. How to handle permissions based on authentication?

- My initial thought was to follow HTTP standard status codes.
- `401 Unauthorized` is used when there is no authentication, and `403 Forbidden` is used when there is authentication
  but no permission.
- I implemented a `Permission` class as shown below to return `403 Forbidden`.

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

#### 5. How to implement product searching?

- Searching was implemented using `Django-filter`.
- Initial search was implemented by storing the "initial" field in the database separately.
    - Whenever a new product is saved or updated, its name is converted to initials and stored.
    - This allows searching by initials.
    - Initials are not returned when viewing detailed information.

#### How to implement a Custom JSON Response?

- To ensure a consistent response format for all APIs on the server, I implemented a `Custom JSON Renderer` as follows:

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
            code=response_context.status_code,  # Return the status code
            message="ok"
            if not response_context.exception
            else response_context.data.get(
                "detail", response_context.data
            ),  # Return "ok" if no exception, otherwise return the exception message
            data=response_context.data if not response_context.exception else None,
        ).to_dict()

        renderer_context["response"].data = response_format

        return super().render(
            response_format,
            accepted_media_type,
            renderer_context,
        )
```

- However, this implementation applies only when using `Django REST Framework`.
- Therefore, for exceptions like 404 and 500 returned by Django, a separate handler was written.
- Note that the documentation tool `drf-spectacular` does not handle this separately.
    - Related Github issue: https://github.com/tfranzel/drf-spectacular/issues/429
    - As a result, the generated OpenAPI specification is not perfect.

#### How to unify code style?

- Code style was standardized using `black`.
- Import order was standardized using `isort`.
- Code style was checked using `flake8`.

- The above three operations were automated using `pre-commit`.

#### How to test if my code works correctly?

- Tests were written using `Unittest`.
- To test if the response format is as expected, a base class with a method for testing response format was created.

```python
class BaseAPITestCase(APITestCase):
    def _test_response_format(self, response):
        """
        Test if the response format is correct.

        1. When STATUS_CODE is 204
        2. When STATUS_CODE is 200 or 201
        3. For other cases (e.g., 400, 401, 403, 404, 500, etc.)
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
        When STATUS_CODE is 201 or 201, the "data" key should not be null.
        """
        self._test_base_response_format(response)
        self.assertIsNotNone(response.data["data"])

    def _test_error_response_format(self, response):
        """
        When it's an error response, the "data" key should be null.
        """
        self._test_base_response_format(response)
        self.assertIsNone(response.data["data"])

    def _test_base_response_format(self, response):
        """
        Test if the response format has the following keys:

        {
            "meta": {
                "code": 200,
                "message": "ok",
            },
            "data": {"products": [...]},
        }
        """
        self.assertIn("meta", response.data)
        self.assertIn("code", response.data["meta"])
        self.assertIn("message", response.data["meta"])
        self.assertIn("data", response.data)

    def _test_204_response_format(self, response):
        """
        Test when the STATUS_CODE is 204 NO CONTENT.
        """

        self.assertEqual(response.data, None)
```

- Currently, it has passed 31 test cases.

## How to run it? I want to try it out!

### 1. Set Environment Variables

Create a `.env` file following the example in the `.env.example` file.

```.env
SECRET_KEY= # Your Django SECRET_KEY here

DJANGO_SUPERUSER_MOBILE= # Mobile number for the Django superuser
DJANGO_SUPERUSER_PASSWORD= # Password for the Django superuser

# Database connection information shared by both Django and MySQL containers
MYSQL_ROOT_PASSWORD=root-password
MYSQL_DATABASE=cafehere-db
MYSQL_USER=cafehere-admin
MYSQL_PASSWORD=root-password
```

### 2. Run Docker Compose

Run the following command in your working directory to start the containers.

Currently, the Docker Compose file is designed for `Mac M1` (MySQL container).

```bash
docker compose up -d
```

### 3. Set up Django

Run the following command in your working directory to perform database migration, create a superuser, and collect
static files.

```bash
docker compose run cafehere-was python manage.py migrate --settings core.settings.production &&\
docker compose run cafehere-was python manage.py createsuperuser --no-input --settings core.settings.production&&\
docker compose run cafehere-was python manage.py collectstatic --settings core.settings.production
```

Visit http://127.0.0.1:8000/ to see the Swagger UI. Enjoy exploring! :)

Please note that the current Swagger UI is automatically generated using `drf-spectacular` but is not perfect due to the
use of `Custom JSON Renderer`. Keep this in mind!