import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content":"what is AI"
        }
    ]
)
print(response["message"]["content"])