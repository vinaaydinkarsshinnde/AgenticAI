from AgentExecutor import agent_executor

print("Agentic AI Assistant (CLI)")
print("Type 'quit' or 'exit' to stop.\n")

while True:
    try:
        query = input("Ask something: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not query:
            continue

        print("\n> Entering new AgentExecutor chain...")
        response = agent_executor.invoke({"input": query})
        print("\n> Response:")
        print(response["output"])
        print("\n---\n")

    except KeyboardInterrupt:
        print("\nSession interrupted by user.")
        break
    except Exception as e:
        print(f"Error: {str(e)}")
