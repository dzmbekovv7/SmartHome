import openai

openai.api_key = "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"  # Твой ключ

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Привет, кто ты?"}
    ]
)

print(response['choices'][0]['message']['content'])
