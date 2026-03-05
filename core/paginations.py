from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"

    def get_page_size(self, request):
        try:
            page_size = int(
                request.query_params.get(self.page_size_query_param, self.page_size)
            )
        except (TypeError, ValueError):
            return self.page_size

        return min(page_size, self.max_page_size)

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "page": self.page.number,
                "page_size": self.get_page_size(self.request),
                "results": data,
            }
        )
