# Smart Irrigation Running Commands

Run these commands from the project root:

```powershell
cd C:\Users\venka\OneDrive\Desktop\smart_irrigation
```

## Local setup

Create and activate a Python 3.12 virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the application and development tools:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If PowerShell blocks activation, run this once for the current terminal session and
then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the application

Run the application using the helper script on macOS, Linux, Git Bash, or WSL:

```bash
chmod +x run.sh
./run.sh
```

Pass application arguments through the script:

```bash
./run.sh --demo
./run.sh --demo --budget 30 --log schedule.log
./run.sh --benchmark
```

Start the interactive dashboard:

```powershell
python -m app.main
```

Run a one-shot demo comparing the Greedy and Dynamic Programming schedulers:

```powershell
python -m app.main --demo
```

Run the demo with a 30-litre budget and write schedules to `schedule.log`:

```powershell
python -m app.main --demo --budget 30 --log schedule.log
```

Run the demo with a fixed random seed and verbose logging:

```powershell
python -m app.main --demo --seed 42 --verbose
```

Run the performance benchmarks:

```powershell
python -m app.main --benchmark
```

The module entry point is also supported:

```powershell
python -m app
```

## Test and quality commands

Run all tests:

```powershell
python -m pytest
```

Run tests with coverage:

```powershell
python -m pytest --cov=app --cov-report=term-missing
```

Run static checks:

```powershell
python -m ruff check app tests
python -m black --check .
python -m mypy app
```

Run the complete quality gate:

```powershell
python -m ruff check app tests
python -m black --check .
python -m mypy app
python -m pytest --cov=app --cov-report=term-missing
```

## Docker commands

Build the image:

```powershell
docker build -t smart-irrigation .
```

Start the interactive dashboard in Docker:

```powershell
docker run --rm -it smart-irrigation
```

Run the demo in Docker:

```powershell
docker run --rm smart-irrigation python -m app.main --demo
```

Run the benchmark service with Docker Compose:

```powershell
docker compose run --rm benchmark
```

Start the interactive irrigation service with Docker Compose:

```powershell
docker compose run --rm irrigation
```

Stop Compose services:

```powershell
docker compose down
```
