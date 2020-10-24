from django.utils.deprecation import MiddlewareMixin
import logging
from django.shortcuts import render


logger = logging.getLogger(__name__)


class UnknownExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        logger.error("path: {0}\r\nException:{1}\r\n\r\n".format(request.path, str(exception)))
        return None
        return render(request, template_name="shrinker/error.html", context={
            "title": "Произошла непредвиденнная ошибка",
        })
