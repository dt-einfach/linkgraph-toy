# LinkGraph toy project
## by David Tsarev

### Installation

Create a new file `.env` and copy the contents from `env.sample`.
Ensure that all variables are set.

Build:
```bash
make build
```

Run containers:
```bash
make up
```

Migrate:
```bash
make migrate
```

Run tests (optional):
```bash
make test
```

Run linter (optional):
```bash
make flake8
```

Run web server:
```bash
make server
```
