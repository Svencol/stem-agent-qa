"""
domain_scout.py
---------------
Reads the environment to learn how a task domain is typically approached.

The stem agent calls this before generating a config. Instead of relying
purely on the model's prior, it searches for how practitioners actually
solve problems in this domain, extracts the strategies they use, and
returns a domain brief the config generator can act on.
"""

from stem_agent.llm import call_text_model, call_json_model


def _generate_search_queries(task_class: str) -> list[str]:
    """Ask the LLM to generate targeted search queries for this domain."""
    system_prompt = (
        "You are a research planner. Given a task domain, generate 3 specific "
        "web search queries that would reveal: (1) how experts approach this "
        "type of task, (2) what tools and techniques are standard, (3) what "
        "common failure modes look like. Return only JSON: {\"queries\": [str]}"
    )
    data = call_json_model(system_prompt, f"Task domain: {task_class}")
    return data.get("queries", [f"how to approach {task_class} professionally"])


def _web_search(query: str, max_results: int = 4) -> list[dict]:
    """Search the web using DuckDuckGo. Returns list of {title, body} dicts."""
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))
    except Exception:
        return []


def _format_results(results: list[dict]) -> str:
    return "\n\n".join(
        f"Title: {r.get('title', '')}\nSnippet: {r.get('body', '')}"
        for r in results
    )


def scout_domain(task_class: str) -> str:
    """
    Search the web to learn how this task domain is typically approached.

    Returns a domain brief: a short structured summary of observed strategies,
    tools, and failure modes that the stem agent uses to select skills.
    """
    print(f"  [SCOUT] Generating search queries for '{task_class}'...")
    queries = _generate_search_queries(task_class)

    all_results = []
    for query in queries:
        print(f"  [SCOUT] Searching: {query}")
        all_results.extend(_web_search(query))

    if not all_results:
        print("  [SCOUT] No search results, falling back to model prior.")
        return f"Domain: {task_class}. Use model prior knowledge."

    combined = _format_results(all_results)

    system_prompt = (
        "You are a domain analyst. Given search results about a task domain, "
        "extract a structured brief with these sections:\n"
        "1. Typical approach: how practitioners break down this type of task\n"
        "2. Standard tools and techniques\n"
        "3. Common failure modes and what good output avoids\n"
        "4. Recommended skills for an AI agent in this domain\n"
        "Be concrete and specific. 200 words max."
    )
    user_prompt = f"Task domain: {task_class}\n\nSearch results:\n{combined}"

    brief = call_text_model(system_prompt, user_prompt)
    print(f"  [SCOUT] Domain brief extracted ({len(brief)} chars).")
    return brief
