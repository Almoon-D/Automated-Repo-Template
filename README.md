# myproject

Una frase: qué hace y para quién.

## Cómo usar esta plantilla (borra esta sección después)

1. En GitHub, en la plantilla: **Use this template → Create a new repository** (privado).
2. En el repositorio nuevo, abre una sesión de Claude Code y pídele:
   `python3 scripts/init_project.py <nombre_del_paquete> --author "Tu Nombre"`,
   luego `uv lock`, `make check`, y que haga commit y push a `main`.
3. En **Settings** del repositorio nuevo:
   - *General → Pull Requests*: solo **Allow squash merging**; activa **Automatically delete
     head branches**; desactiva **Always suggest updating pull request branches** y
     **Allow auto-merge**.
   - *Advanced Security*: activa **Dependency graph**, **Dependabot alerts**,
     **Dependabot security updates** y **Grouped security updates**; desactiva
     **Automatic dependency submission** (uv no la necesita y gasta ejecuciones).
   - *Actions → General → Workflow permissions*: **Read repository contents and packages
     permissions**, y desmarca **Allow GitHub Actions to create and approve pull requests**
     (el workflow de release pide su propio permiso de escritura).
   - Solo si el repo es público (o tienes Pro): *Rules → Rulesets* sobre `main` con
     **Restrict deletions** y **Block force pushes**. No exijas checks: los PRs de solo
     documentación no pasan CI y se quedarían bloqueados.
   - En tu cuenta, *Billing and licensing → Budgets and alerts*: presupuesto de Actions de
     0 € con **Stop usage** activado, para no pagar nunca por error.
4. Rellena `docs/MASTER_PLAN.md` y la primera sesión en `docs/sessions/01-foundation.md`.
5. Revisa la licencia: por defecto es AGPL-3.0 (`LICENSE` y `license` en `pyproject.toml`).
   Si el proyecto necesita otra, cámbiala en los dos sitios antes del primer release.

## Qué trae

| Pieza | Para qué |
|---|---|
| `AGENTS.md` (+ `CLAUDE.md`, `GEMINI.md`) | Manual del agente: qué leer, reglas, protocolo de PR → revisión → merge |
| `docs/sessions/` | Un archivo por sesión; `make prompt S=01` imprime el prompt |
| `docs/decisions/` | Una decisión por archivo, con índice |
| `docs/ROADMAP.md`, `docs/MASTER_PLAN.md`, `docs/knowledge/` | Plan, estado y lo observado de servicios externos |
| `config/defaults/` + `config/owner.yaml` | Nada hardcodeado: valores por defecto y tus cambios |
| `.github/workflows/ci.yml` | `make check` en cada PR (no en docs), barato para GitHub Free |
| `.github/workflows/release.yml` | Publica la release cuando cambia la versión |
| `.github/dependabot.yml` | Una tanda al mes, agrupada, sin rebases automáticos |

## Comandos

```
make setup     # entorno + hooks
make check     # todo lo que corre CI
uv run myproject --help
```
