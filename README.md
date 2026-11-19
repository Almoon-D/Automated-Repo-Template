# myproject

Una frase: qué hace y para quién.

## Cómo usar esta plantilla (borra esta sección después)

1. En GitHub, en la plantilla: **Use this template → Create a new repository**. Sin marcar
   *Include all branches*: el proyecto nuevo empieza sin historial y en la versión 0.0.0.
2. En el repositorio nuevo, abre una sesión de Claude Code y pídele:
   `make setup`, `python3 scripts/init_project.py <nombre_del_paquete> --author "Tu Nombre"`,
   `uv lock` y `make check`, y que lo suba en un PR.
3. Ajustes del repositorio nuevo: los de la sección siguiente.
4. Rellena `docs/MASTER_PLAN.md` y la primera sesión en `docs/sessions/01-foundation.md`.
   Esa sesión publica la versión 0.1.0.
5. Revisa la licencia: por defecto es AGPL-3.0 (`LICENSE` y `license` en `pyproject.toml`).
   Si el proyecto necesita otra, cámbiala en los dos sitios antes de la 0.1.0.

## Ajustes de GitHub

**Settings → General**
- *Releases*: activa **Enable release immutability** (una release publicada no se puede
  alterar; el workflow nunca la modifica).
- *Features*: **Issues** y **Pull requests** sí; Wikis, Sponsorships, Discussions y
  Projects no (salvo que los uses). En un repo público, *Creation allowed by:
  Collaborators only* en los dos.
- *Pull Requests*: solo **Allow squash merging**, con *Default commit message*: **Pull request
  title** (las descripciones de los agentes son largas y se quedan en el PR); **Always
  suggest updating pull request branches** no; **Allow auto-merge** sí si GitHub lo permite
  (no hace falta: CI mergea Dependabot por su cuenta); **Automatically delete head branches** sí.
- *Commits, Archives, Issues*: como vienen.

**Settings → Advanced Security**
- **Dependency graph**, **Dependabot alerts**, **Dependabot security updates** y
  **Grouped security updates**: activados.
- **Automatic dependency submission**: desactivado (uv no la necesita).

**Settings → Actions → General**
- *Workflow permissions*: **Read repository contents and packages permissions**; **Allow
  GitHub Actions to create and approve pull requests** desmarcado. Los workflows que
  escriben (release, el merge de Dependabot) piden su propio permiso.

**Settings → Rules → Rulesets** (repos públicos, o privados con Pro): uno sobre la rama por
defecto, *Enforcement: Active*, sin bypass, con **Restrict deletions**, **Block force
pushes**, **Require a pull request before merging** (0 aprobaciones) y **Require status
checks to pass** → `ci`. El check `ci` siempre informa, también en PRs de solo documentación.

**Tu cuenta → Settings → Billing and licensing → Budgets and alerts**: presupuesto de
Actions de 0 € con **Stop usage**, para no pagar nunca por error.

## Qué trae

| Pieza | Para qué |
|---|---|
| `AGENTS.md` (+ `CLAUDE.md`, `GEMINI.md`) | Manual del agente: qué leer, reglas, protocolo de PR → revisión → merge |
| `docs/sessions/` | Un archivo por sesión; `make prompt S=01` imprime el prompt |
| `docs/decisions/` | Una decisión por archivo, con índice |
| `docs/ROADMAP.md`, `docs/MASTER_PLAN.md`, `docs/knowledge/` | Plan, estado y lo observado de servicios externos |
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
