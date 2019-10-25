from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 200
    max_page_size = 100000
    page_size_query_param = "page_size"
