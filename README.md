# myproject

Una frase: qué hace y para quién.

## Cómo usar esta plantilla (borra esta sección después)

1. En GitHub, en la plantilla: **Use this template → Create a new repository**. Sin marcar
   *Include all branches*: el proyecto nuevo empieza sin historial y en la versión 0.0.0.
2. En el repositorio nuevo, abre una sesión de Claude Code y pídele:
   `make setup`, `python3 scripts/init_project.py <nombre_del_paquete> --author "Tu Nombre"`,
   `uv lock` y `make check`, y que lo suba en un PR.
3. Ajustes del repositorio nuevo: [`docs/GITHUB_SETTINGS.md`](docs/GITHUB_SETTINGS.md).
4. Rellena `docs/MASTER_PLAN.md` y la primera sesión en `docs/sessions/01-foundation.md`.
   Esa sesión publica la versión 0.1.0.
5. Revisa la licencia: por defecto es AGPL-3.0 (`LICENSE` y `license` en `pyproject.toml`).
   Si el proyecto necesita otra, cámbiala en los dos sitios antes de la 0.1.0.

## Ajustes de GitHub

GitHub no copia los ajustes de la plantilla al repositorio nuevo. Repásalos con
[`docs/GITHUB_SETTINGS.md`](docs/GITHUB_SETTINGS.md): cada opción de *Settings*, activa o no,
y por qué.

## Qué trae

| Pieza | Para qué |
|---|---|
| `AGENTS.md` (+ `CLAUDE.md`, `GEMINI.md`) | Manual del agente: qué leer, reglas, protocolo de PR → revisión → merge |
| `docs/sessions/` | Un archivo por sesión; `make prompt S=01` imprime el prompt |
| `docs/decisions/` | Una decisión por archivo, con índice |
| `docs/ROADMAP.md`, `docs/MASTER_PLAN.md`, `docs/knowledge/` | Plan, estado y lo observado de servicios externos |
| `docs/GITHUB_SETTINGS.md` | Todos los ajustes de GitHub, opción por opción |
| `config/defaults/` + `config/owner.yaml` | Nada hardcodeado: valores por defecto y tus cambios |
| `.github/workflows/ci.yml` | `make check` en cada PR (en segundos si solo cambian docs) |
| `.github/workflows/release.yml` | Publica la release cuando cambia la versión (la 0.0.0 no) |
| `.github/dependabot.yml` | Una tanda al mes, agrupada; CI mergea sola lo que no es major |

## Comandos

```
make setup     # entorno + hooks
make check     # todo lo que corre CI
uv run myproject --help
```
