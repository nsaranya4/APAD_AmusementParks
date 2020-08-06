

def pagination(request):
    page = request.args.get('page', None)
    if page:
        page = page.encode('utf-8')
        skip = int(page)
    else:
        skip = 0
    limit = 5
    offset = skip * limit
    return skip, offset, limit
