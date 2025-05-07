# cli.py

from agent import agent

print("💬 Welcome to the RAG-Powered Multi-Agent Q&A Assistant (Local Mode)")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("❓ Ask a question: ")
    if user_input.lower() == "exit":
        break
    response = agent.run(user_input)
    print("🧠 Response:", response)
    print("-" * 50)