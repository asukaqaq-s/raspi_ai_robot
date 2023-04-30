import openai

def send_2_gpt(content: str, role: str):
    openai.api_key = ""
    model = "gpt-3.5-turbo"

    # response = openai.Completion.create(model=model, prompt=content)
    response = openai.ChatCompletion.create(
        model = model
        messages = [{"role":role,
                    "content": content}]
    )
    return response['choices'][0]['message']['content']
