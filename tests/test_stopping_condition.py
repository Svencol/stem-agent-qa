from unittest.mock import patch

from stem_agent.specialize import propose_stopping_condition


def test_propose_stopping_condition_returns_float():
    with patch("stem_agent.specialize.call_json_model") as mock:
        mock.return_value = {"min_improvement": 0.3, "reasoning": "hard domain"}
        result = propose_stopping_condition("some brief", "bug_detection_rate")

    assert isinstance(result, float)
    assert 0.05 <= result <= 0.95


def test_propose_stopping_condition_clamps_high_value():
    with patch("stem_agent.specialize.call_json_model") as mock:
        mock.return_value = {"min_improvement": 2.5, "reasoning": "unreasonable"}
        result = propose_stopping_condition("brief", "metric")

    assert result == 0.95


def test_propose_stopping_condition_clamps_low_value():
    with patch("stem_agent.specialize.call_json_model") as mock:
        mock.return_value = {"min_improvement": 0.001, "reasoning": "too easy"}
        result = propose_stopping_condition("brief", "metric")

    assert result == 0.05


def test_propose_stopping_condition_handles_missing_key():
    with patch("stem_agent.specialize.call_json_model") as mock:
        mock.return_value = {"reasoning": "forgot the number"}
        result = propose_stopping_condition("brief", "metric")

    assert result == 0.15
