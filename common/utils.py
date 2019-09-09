from aiohttp import web


async def get_object_or_404(request, model, **kwargs):
    """
    Get object or raise HttpNotFound
    """
    try:
        return await request.app.objects.get(model, **kwargs)
    except model.DoesNotExist:
        raise web.HTTPNotFound()