from rest_framework.pagination import PageNumberPagination

class FeedPagination(PageNumberPagination):
    """
        Custom pagination class for the feed endpoint.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5