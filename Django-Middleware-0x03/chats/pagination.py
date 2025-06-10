from rest_framework.pagination import PageNumberPagination
class CustomPagination(PageNumberPagination):
    """
    Custom pagination class to handle pagination in the API.
    """
    page_size = 20  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 100  # Maximum number of items per page
    page_query_param = 'page'  # Query parameter for the page number

    def get_paginated_response(self, data):
        """
        Returns a paginated response with the given data.
        """
        return {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }