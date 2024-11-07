# Orbidi Challenge #

## Project Set-Up

### Dependencies

- [Docker](https://www.docker.com/)

### Start

Run `make run` to start all the servers and check out the [SwaggerUI Project's](http://127.0.0.1:8080/docs)

## Development

### Dev Dependencies

- [Poetry](https://python-poetry.org/)
- [PyEnv](https://github.com/pyenv/pyenv)

### Dev Set Up

1. Install python using pyenv (could omit this step in CI environments installing the right py version): `pyenv install`
2. Init poetry: `poetry install --with test --with dev`
3. Install pre-commit: `pre-commit install` (inside poetry virtual env)

## Additional Considerations (System Design / Patterns / Others)

Although these elements were not fully implemented due to time constraints, they are important considerations for a
production-ready system:

- Circuit Breaker pattern
- Dead Letter Queue
- CI/CD pipelines
- Rate limiting (potentially through an API Gateway)
- Throttling mechanisms
- HTTP Compression
- Business Metrics tracking
- Health-Check endpoint for system monitoring

## TL;DR

In conclusion, I’m happy to discuss any questions or optimizations regarding the design choices and the trade-offs made
in this project.

If anything is unclear, feel free to reach out for further discussion.
