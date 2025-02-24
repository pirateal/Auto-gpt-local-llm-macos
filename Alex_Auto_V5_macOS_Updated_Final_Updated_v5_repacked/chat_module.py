
from openai import OpenAI

def generate_markdown(title, items):
    markdown_text = f"# {title}\n\n"
    for item in items:
        markdown_text += f"- {item}\n"
    return markdown_text

def start_chat_session():
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    history = [
        {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
        {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
    ]

    while True:
        completion = client.chat.completions.create(
            model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
            messages=history,
            temperature=0.7,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                new_message["content"] += chunk.choices[0].delta.content

        history.append(new_message)
        print()
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        history.append({"role": "user", "content": user_input})
