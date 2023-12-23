import g4f


async def run_chatbase(prompt: str):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
            provider=g4f.Provider.ChatBase,
        )
        return "ChatBase", response
    except Exception as e:
        return "ChatBase", str(e)


async def get_chatbase_response(prompt: str):
    provider, response = await run_chatbase(prompt)
    if not isinstance(response, Exception):
        return response
    else:
        return f"Ошибка от {provider}: {response}"
