from rest_framework import pagination
from rest_framework.response import Response


class DefaultPagination(pagination.PageNumberPagination):
    """
    Default paginator.
    """

    page_size_query_param = "page_size"
    page_size = 10
    max_page_size = 3000

    def get_paginated_response(self, data):
        """
        Annotate the response with pagination information.

        *Important*

        Ordering is required to have pagination working properly.
        Without that you can have few rows repeated across
        different pages and few missing.

        read : https://docs.djangoproject.com/en/2.2/
        topics/pagination/#required-arguments

        To use Pagination import DefaultPagination into
        pagination_class = DefaultPagination
        """
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "num_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "start": (self.page.number - 1) * self.get_page_size(self.request),
                "results": data,
            }
        )
