# AI Agent

An agentic AI system built from scratch as part of a structured Agentic AI Engineer curriculum.

## Purpose
A research agent that autonomously searches the web, reads pages, and summarises findings — without step-by-step human instruction.

## Tech Stack
- Python
- Groq API (llama-3.3-70b-versatile)
- DuckDuckGo Search (ddgs)
- BeautifulSoup4
- Requests

## Progress

| Week | Topic | Status |
|------|-------|--------|
| Week 7 | AI Agent — Tool Building | ✅ In Progress |

## Milestones

| Milestone | Details | Status |
|-----------|---------|--------|
| Project setup | venv, .env, .gitignore | ✅ Done |
| search_web tool | DuckDuckGo search returning top 3 results | ✅ Done |
| read_page tool | Fetches and strips HTML from a URL | ✅ Done |
| Error handling | try-except in read_page — agent survives unreachable URLs | ✅ Done |
| Brain (LLM) | Groq API connection with tool awareness | ✅ Done |
| Agent Loop | ReAct loop — Reason, Act, Observe with 10 step limit | ✅ Done |
| System Prompt | Strict format enforcement for TOOL and FINAL responses | ✅ Done |
| Flask app.py | SSE streaming server with /research and /stream routes | ✅ Done |
| index.html UI | Live step feed, formatted final answer, SSE client | ✅ Done |
| LM Studio integration | Switched to local model for zero-cost testing | ✅ Done |
| Bug fixes | 415 error, SSE newline handling, startsWith typo, port conflict | ✅ Done |