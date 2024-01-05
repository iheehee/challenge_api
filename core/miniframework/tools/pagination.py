class CustomPagination:
    page_size = None

    def __init__(self, query_set, page, offset, request):
        self.query_set = query_set
        self.page = page
        self.offset = offset
        self.request = request

    def _get_page_parms(self, request):
        page = request.GET.get("page", 1)
        return page

    def _pagination_query_set(self, query_set, offset, limit):
        pagination_query_result = query_set[offset:limit]
        return pagination_query_result

    def __call__(self, request, query_set):
        page = self._get_page_parms(request)
        limit = int(self.page_size * page)
        offset = int(limit - self.page_size)
        return self._pagination_query_set(query_set, offset, limit)

    def paginated_response(self, data):


class PaginationHandlerMixin:
    page_size = 2

    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None

        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
