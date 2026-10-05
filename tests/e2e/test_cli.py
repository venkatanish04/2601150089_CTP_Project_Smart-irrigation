"""End-to-end: drive the real CLI the way a user would."""

from app.cli.dashboard import Dashboard, render_needs
from app.main import build_system, main

FAST = (0.001, 0.003)


def test_interactive_session(capsys) -> None:  # type: ignore[no-untyped-def]
    answers = iter(["1", "2", "3", "4", "5", "6", "7", "x", "9"])
    dash = Dashboard(build_system(delay=FAST), 40, input_fn=lambda _: next(answers))
    dash.run()
    out = capsys.readouterr().out
    for expected in (
        "Sensor Readings",
        "Rain Probability",
        "Irrigation Needs",
        "IRRIGATION PLAN (Greedy)",
        "IRRIGATION PLAN (Dynamic Programming)",
        "ALGORITHM COMPARISON",
        "Speedup",
        "Invalid choice",
        "Goodbye",
    ):
        assert expected in out


def test_benchmark_menu_option(capsys) -> None:  # type: ignore[no-untyped-def]
    dash = Dashboard(build_system(delay=FAST), 40)
    assert dash.handle("8") is True
    assert "SENSOR POLLING" in capsys.readouterr().out


def test_render_needs_empty() -> None:
    assert "No field" in render_needs([])


def test_demo_flag_and_log(tmp_path, capsys, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    import app.main as m

    monkeypatch.setattr(m, "build_system", lambda seed, budget: build_system(seed, budget, FAST))
    log = tmp_path / "run.log"
    assert main(["--demo", "--budget", "40", "--log", str(log)]) == 0
    assert "Schedule generated successfully." in capsys.readouterr().out
    assert len(log.read_text().splitlines()) == 2
