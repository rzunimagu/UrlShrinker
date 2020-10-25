# UrlShrinker

Требуется реализовать web-приложение - аналог bit.ly и подобных систем.
То есть для длинных урлов создает их короткие аналоги <domain>/<subpart>.

Приложение содержит одну страницу на которой:
Форма в которой можно ввести URL, который должен быть сокращен
Табличку со всеми сокращенными URL (с пагинацией) данного юзера

Обязательные требования:
Приложение НЕ содержит авторизации
Приложение отслеживает юзеров по сессии, т.е. у каждого юзера свой набор редиректов (правил)
Данные хранятся в MySQL
При заходе на сжатый URL приложение редиректит на соответствующий URL (который был сжат)
Пользователь по желанию может указать свой <subpart>. Если такой <subpart> уже используется, нужно сообщить об этом юзеру.
Реализация на Django
Кэширование редиректов в редисе
Очистка старых правил по расписанию

Особое внимание нужно уделить:
Логгированию
Обработке ошибок
Чистоте и понятности кода
Документации к основным методам

Плюсом будет:
DjangoRestFramework для реализации API 
Реализация как SPA на React/Vue.js
Докеризация результата (docker-compose up для запуска сервиса и всех зависимостей)

Ориентировочное время выполнения - 8 часа. Максимальное - 16 часов. 
