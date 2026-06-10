from ddgs import DDGS
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from groq import Groq

load_dotenv()

SYSTEM_PROMPT = """You are a research agent. You have access to two tools:
                1. search_web(query) - searches the web and returns top 3 results with title, url and snippet
                2. read_page(url) - fetches and returns the text content of a webpage
                To use a tool, respond in EXACTLY this format:
                TOOL: tool_name
                INPUT: your_input
                
                When you have enough information to answer the goal, respond in EXACTLY this format:
                FINAL: your comprehensive answer is here
                
                Rules:
                - Use search_web first to find relevant URLs
                - Use read_page to dig deeper into promising results
                - Never make up information. Only use what the tools return
                - Always end with FINAL when you have enough information
                - Your FINAL answer must be structured with clear headings and bullet points. Never write a wall of text. Make it skimmable.
                - CRITICAL: Your response must ALWAYS start with either TOOL: or FINAL: - no exceptions. Never add explanations or commentary before these keywords.
                  """

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages = messages
    )
    return response.choices[0].message.content

def search_web(query):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=3):
            results.append({
                "title" : r["title"],
                "url" : r["href"],
                "snippet" : r["body"]
            })
    return results

def read_page(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return text[:2000]
    except Exception as e:
        return f"Could not read page {str(e)}"

def run_agent(goal):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": goal}
    ]

    for i in range(10):
        yield f"Step {i+1}: Thinking..."
        response = call_llm(messages)

        messages.append({"role": "assistant", "content": response})

        if response.startswith("FINAL:"):
            yield f"FINAL:{response[6:].strip()}"
            break

        elif response.startswith("TOOL:"):
            lines = response.strip().split("\n")
            tool_name = lines[0].replace("TOOL:", "").strip()
            tool_input = lines[1].replace("INPUT:", "").strip()

            if tool_name == "search_web":
                yield f"🔍 Searching the web for: {tool_input}"
                result = search_web(tool_input)
            elif tool_name == "read_page":
                yield f"📄 Reading page: {tool_input}"
                result = read_page(tool_input)
            else:
                result = "Unknown tool requested"
            
            messages.append({"role": "user", "content": f"TOOL RESULT:\n{result}"})

        else:
            print("Unexpected response format. Stopping")
            break

if __name__ == "__main__":
    goal = input("What do you want the agent to research? ")
    for update in run_agent(goal):
        if update.startswith("FINAL:"):
            print("\n=== Research Complete ===")
            print(update[6:].strip())
        else:
            print(update)