async def ai_generate(text: str) -> str:
    prompt = "Ты — ассистент Hackify. Отвечай кратко и по делу."
    print(f"[DEBUG] Получен запрос: {text}")  # Логирование входящего запроса

    try:

        async with AsyncClient() as client:
            direct_response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {config.DEEPSEEK_API_KEY}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": text}],
                    "temperature": 0.7
                },
                timeout=30.0
            )
            print(f"[DEBUG] Ответ DeepSeek: {direct_response.status_code}")  # Логирование статуса

            if direct_response.status_code == 200:
                return direct_response.json()["choices"][0]["message"]["content"]

        # 2. Если прямой запрос не сработал, пробуем через OpenRouter
        openrouter_response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {config.OPENROUTER_API_KEY}"},
            json={
                "model": "deepseek/deepseek-chat",
                "messages": [{"role": "user", "content": text}]
            },
            timeout=30.0
        )
        print(f"[DEBUG] Ответ OpenRouter: {openrouter_response.status_code}")

        return openrouter_response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"[ERROR] Ошибка генерации: {str(e)}")  # Логирование ошибок
        return "⚠️ Ошибка: сервис временно недоступен"