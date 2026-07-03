import pytest
import requests


# ========== GET /posts ==========

@pytest.mark.api
@pytest.mark.fast
def test_get_all_posts_returns_200(api_session, api_url):
    """
    Базовый тест на получение списка постов.
    Проверяем, что сервер отвечает успешным статусом и возвращает список.
    Это аналог проверки "сервис жив и отдаёт данные".
    """
    response = api_session.get(f"{api_url}/posts")
    
    # Главная проверка: сервер доступен и отвечает без ошибок
    assert response.status_code == 200
    # Убеждаемся, что ответ — список (JSON-массив), а не объект или пустота
    assert isinstance(response.json(), list)


@pytest.mark.api
@pytest.mark.fast
def test_get_all_posts_contains_expected_fields(api_session, api_url):
    """
    Структурный тест: проверяем, что каждый пост содержит обязательные поля.
    Если завтра разработчик переименует 'title' в 'heading', тест упадёт,
    и мы сразу узнаем, что контракт нарушен.
    """
    response = api_session.get(f"{api_url}/posts")
    posts = response.json()
    assert len(posts) > 0  # список не пустой
    
    post = posts[0]
    required_fields = ["userId", "id", "title", "body"]
    for field in required_fields:
        assert field in post, f"Отсутствует поле {field}"


@pytest.mark.api
@pytest.mark.fast
def test_get_single_post_returns_correct_id(api_session, api_url):
    """
    Запрашиваем конкретный пост по ID и проверяем, что вернулись именно его данные.
    Это аналог запроса баланса конкретного пользователя или ордера по ID.
    """
    response = api_session.get(f"{api_url}/posts/1")
    assert response.status_code == 200
    # ID в ответе должен совпадать с запрошенным
    assert response.json()["id"] == 1


@pytest.mark.api
@pytest.mark.fast
def test_get_nonexistent_post_returns_404(api_session, api_url):
    """
    Негативный тест: запрашиваем несуществующий ресурс.
    Сервер должен вернуть 404, а не пустой ответ или 500.
    Проверяем, что ошибка обрабатывается корректно и предсказуемо.
    """
    response = api_session.get(f"{api_url}/posts/99999")
    assert response.status_code == 404


# ========== POST /posts ==========

@pytest.mark.api
@pytest.mark.fast
@pytest.mark.parametrize("payload,expected_id", [
    ({"title": "foo", "body": "bar", "userId": 1}, 101),
    ({"title": "", "body": "", "userId": 0}, 101),
])
def test_create_post_returns_201(api_session, api_url, payload, expected_id):
    """
    Тест на создание ресурса. Отправляем корректные данные и проверяем:
    - статус 201 (Created)
    - в ответе присвоен ID (значит, объект сохранён)
    - заголовок в ответе совпадает с отправленным (сервер не исказил данные)
    
    Параметризация гоняет один и тот же тест с разными данными.
    """
    response = api_session.post(f"{api_url}/posts", json=payload)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["id"] == expected_id
    assert json_data["title"] == payload["title"]


@pytest.mark.api
@pytest.mark.fast
def test_create_post_without_required_fields(api_session, api_url):
    """
    Проверяем поведение при отправке пустого тела.
    Идеальный сервер должен бы вернуть 400 (Bad Request), но JSONPlaceholder
    принимает всё. Мы фиксируем реальное поведение: 201 и отсутствие title.
    
    В проекте мужа это станет тестом на валидацию обязательных полей.
    """
    response = api_session.post(f"{api_url}/posts", json={})
    assert response.status_code == 201
    json_data = response.json()
    assert "title" not in json_data or json_data["title"] == ""


# ========== PUT /posts/1 ==========

@pytest.mark.api
@pytest.mark.fast
def test_update_post_returns_200(api_session, api_url):
    """
    Тест на полное обновление ресурса (PUT).
    Отправляем новый объект и проверяем, что сервер его принял и вернул обновлённые данные.
    """
    new_data = {"id": 1, "title": "updated", "body": "new body", "userId": 1}
    response = api_session.put(f"{api_url}/posts/1", json=new_data)
    assert response.status_code == 200
    assert response.json()["title"] == "updated"


# ========== DELETE /posts/1 ==========

@pytest.mark.api
@pytest.mark.fast
def test_delete_post_returns_200(api_session, api_url):
    """
    Тест на удаление ресурса. Проверяем, что сервер отвечает 200
    и удаление проходит без ошибок. В реальном проекте после удаления
    GET на этот же ID должен возвращать 404.
    """
    response = api_session.delete(f"{api_url}/posts/1")
    assert response.status_code == 200


# ========== Таймауты и надёжность ==========

@pytest.mark.api
@pytest.mark.slow
def test_api_response_time(api_session, api_url):
    """
    Нефункциональный тест: проверяем, что API отвечает за приемлемое время.
    Если сервер начнёт тормозить, тест упадёт и сообщит точное время ответа.
    Порог 2 секунды — с большим запасом для учебного примера.
    """
    import time
    start = time.perf_counter()
    response = api_session.get(f"{api_url}/posts")
    elapsed = time.perf_counter() - start
    assert response.status_code == 200
    assert elapsed < 2.0, f"Слишком долго: {elapsed:.2f} сек"