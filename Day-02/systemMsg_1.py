import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content":"what is AI"
        },
        {
            "role":"user",
            "content":"Explain AI"
        }
    ]
)
print(response["message"]["content"])