from __future__ import annotations

import subprocess
from collections.abc import Iterator, Sequence
from pathlib import Path

import httpx
import pytest

ROOT = Path(__file__).resolve().parents[1]
TIMETABLE_XML = "/fixtures/timetable/rozvrh.xml"


@pytest.fixture(scope="session")
def docker_compose_file() -> list[str]:
    return [
        str(ROOT / "compose.yaml"),
        str(ROOT / "compose.test.yaml"),
    ]


@pytest.fixture(scope="session")
def docker_setup() -> list[str]:
    # Tear down first so interrupted IDE runs do not leave duplicate stacks.
    return ["down -v", "up --wait"]


def _compose_exec(
    compose_files: Sequence[str],
    project_name: str,
    args: list[str],
    *,
    stdin: str | None = None,
) -> None:
    command = ["docker", "compose", "-p", project_name]
    for compose_file in compose_files:
        command.extend(["-f", compose_file])
    command.extend(["exec", "-T", "legacy", *args])
    subprocess.run(
        command,
        check=True,
        cwd=ROOT,
        input=stdin,
        text=True,
    )


@pytest.fixture(scope="session")
def seeded_database(
    docker_services: object,
    docker_compose_file: list[str],
    docker_compose_project_name: str,
) -> None:
    """Create schema and load timetable XML via legacy Symfony tasks."""
    _ = docker_services
    _compose_exec(
        docker_compose_file,
        docker_compose_project_name,
        ["./symfony", "doctrine:insert-sql"],
    )
    # candle:import prompts for confirmation; slugify needs locales the image lacks.
    _compose_exec(
        docker_compose_file,
        docker_compose_project_name,
        [
            "./symfony",
            "candle:import",
            TIMETABLE_XML,
        ],
        stdin="y\ny\n",
    )


@pytest.fixture(scope="session")
def gateway_url(docker_ip: str, docker_services: object, seeded_database: None) -> str:
    _ = seeded_database
    port = docker_services.port_for("gateway", 80)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=180.0,
        pause=1.0,
        check=lambda: _gateway_up(url),
    )
    return url


def _gateway_up(url: str) -> bool:
    try:
        response = httpx.get(url, timeout=2.0)
    except httpx.HTTPError:
        return False
    return response.status_code < 500


@pytest.fixture
def client(gateway_url: str) -> Iterator[httpx.Client]:
    with httpx.Client(base_url=gateway_url, follow_redirects=False) as http_client:
        yield http_client
