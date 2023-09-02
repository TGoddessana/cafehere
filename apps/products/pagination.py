from rest_framework.pagination import CursorPagination


class CafehereCursorPagination(CursorPagination):
    page_size = 10
    ordering = "-id"
