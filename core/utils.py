from aiohttp import web


def redirect(request, router_name, *, permanent=False, **kwargs):
    """
    Redirect to given URL name
    """
    url = request.app.router[router_name].url(**kwargs)
    if permanent:
        raise web.HTTPMovedPermanently(url)
    raise web.HTTPFound(url)


async def get_object_or_404(request, model, **kwargs):
    """
    Get object or raise HttpNotFound
    """
    try:
        return await request.app.objects.get(model, **kwargs)
    except model.DoesNotExist:
        raise web.HTTPNotFound()