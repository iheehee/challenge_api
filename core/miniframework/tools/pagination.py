class CustomPagination:
    page_size = None

    def _get_page_parms(self, request):
        page = request.GET.get("page", 1)
        return page

    def _count_page(self, paginated_query):
        page_count = paginated_query.count()
        return page_count

    def paginated_query_set(self, request, query_set):
        page = self._get_page_parms(request)
        limit = self.page_size * int(page)
        offset = limit - self.page_size
        pagination_query_result = query_set[offset:limit]
        return pagination_query_result

    def paginated_response(self, request, paginated_query, data):
        return {
            "page": self._get_page_parms(request),
            "page_count": self._count_page(paginated_query),
            "result": data,
        }
