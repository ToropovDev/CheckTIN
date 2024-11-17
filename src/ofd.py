import httpx


from httpx import Response

from src.config import OFD_HEADERS, OFD_URL
from src.schemas import OfdDAta, OfdSubject


async def send_request(
    tin: int,
) -> Response:
    request_data = OfdDAta(query=tin)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=OFD_URL,
            data=request_data.model_dump(),
            headers=OFD_HEADERS,
        )

        return response


async def handle_ofd(tin: int) -> str | OfdSubject:
    response = await send_request(tin=tin)

    if response.status_code != 200:
        return (
            "Возникла ошибка при попытке получить данные с ofd\\.nalog\\.ru\n\n"
            "Попробуйте позже или вручную на сайте"
        )

    data = response.json().get("data")
    if not data:
        return f"Данных в системе ofd\\.nalog\\.ru по ИНН {tin} не найдено"

    if len(data) != 1:
        return f"По ИНН {tin} найдено несколько субъектов МСП\\. Это доработается"

    subject = OfdSubject.model_validate(data[0])
    return subject
