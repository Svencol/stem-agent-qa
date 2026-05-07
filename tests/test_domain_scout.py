"""Tests for domain scout — does not make real network calls."""

from unittest.mock import patch

from stem_agent.domain_scout import scout_domain, _generate_search_queries


def test_generate_search_queries_returns_list():
    with patch("stem_agent.domain_scout.call_json_model") as mock:
        mock.return_value = {"queries": ["q1", "q2", "q3"]}
        queries = _generate_search_queries("Python QA")

    assert isinstance(queries, list)
    assert len(queries) == 3


def test_scout_domain_falls_back_on_no_results():
    with patch("stem_agent.domain_scout._generate_search_queries") as mq, patch(
        "stem_agent.domain_scout._web_search"
    ) as ms:
        mq.return_value = ["some query"]
        ms.return_value = []
        result = scout_domain("Python QA")

    assert isinstance(result, str)
    assert len(result) > 0


def test_scout_domain_summarises_results():
    fake_results = [{"title": "Testing Python", "body": "Use pytest and edge cases."}]

    with patch("stem_agent.domain_scout._generate_search_queries") as mq, patch(
        "stem_agent.domain_scout._web_search"
    ) as ms, patch("stem_agent.domain_scout.call_text_model") as mt:
        mq.return_value = ["query"]
        ms.return_value = fake_results
        mt.return_value = "Domain brief content."

        result = scout_domain("Python QA")

    assert result == "Domain brief content."
