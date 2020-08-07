

def pagination(request):
    page = request.args.get('page', None)
    if page:
        page = page.encode('utf-8')
        skip = int(page)
    else:
        skip = 0
    limit = 4
    offset = skip * limit
    return skip, offset, limit


def more_pages(limit, current_len):
    if current_len > limit:
        return True
    else:
        return False
