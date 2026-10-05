"""End-to-end tests driving the CLI application and verifying user output."""

import app.main as m
from app.cli.dashboard import Dashboard
from app.main import build_system, main

FAST = (0.001, 0.002)


def test_cli_dashboard_interaction(capsys) -> None:  # type: ignore[no-untyped-def]
    inputs = iter(["1", "2", "3", "4", "5", "6", "9"])
    dash = Dashboard(build_system(delay=FAST), 40, input_fn=lambda _: next(inputs))
    dash.run()
    captured = capsys.readouterr().out
    assert "Sensor Readings" in captured
    assert "Weather" in captured
    assert "IRRIGATION PLAN" in captured
    assert "ALGORITHM COMPARISON" in captured
    assert "Goodbye" in captured


def test_main_demo_execution(capsys) -> None:  # type: ignore[no-untyped-def]
    exit_code = main(["--demo", "--budget", "35"])
    assert exit_code == 0
    captured = capsys.readouterr().out
    assert "IRRIGATION PLAN (Greedy)" in captured
    assert "IRRIGATION PLAN (Dynamic Programming)" in captured
