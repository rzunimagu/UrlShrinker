from django.utils.deprecation import MiddlewareMixin
import logging


logger = logging.getLogger(__name__)


class UnknownExceptionMiddleware(MiddlewareMixin):

    """Обрабатываем все исключения, которые не были перехвачены и сохраняем их в лог"""
    def process_exception(self, request, exception):
        logger.error("path: {0}. Exception:{1}".format(request.path, str(exception)))
        return None
