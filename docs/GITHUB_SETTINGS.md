# Ajustes de GitHub

GitHub **no copia los ajustes** al crear un repositorio con *Use this template*: solo copia
los archivos. Esta guía se repasa una vez en cada repositorio nuevo, sección por sección del
menú *Settings*, en el mismo orden.

Columnas: **Plantilla** = este repositorio (público). **Proyecto** = un repositorio creado
desde la plantilla, privado y con el plan Free. Si un proyecto es público, usa la columna
Plantilla salvo donde se indique otra cosa. "—" = no aparece o no aplica. Lo que esta guía no
menciona se deja como viene.

## General

| Opción | Plantilla | Proyecto | Por qué |
|---|---|---|---|
| Template repository | ✅ | ❌ | Solo la plantilla es plantilla. |
| Default branch | `main` | `main` | Los workflows y AGENTS.md cuentan con `main`. |
| Releases → Enable release immutability | ✅ | ✅ | Una release publicada no se puede alterar; el workflow nunca la modifica. |
| Wikis | ❌ | ❌ | Ver nota 1. |
| Issues | ✅ | ✅ | Para apuntar fallos o ideas desde el móvil; la planificación vive en `docs/`. |
| Issues → Creation allowed by | Collaborators only | — | En un repo público, evita que extraños abran issues. |
| Sponsorships | ❌ | ❌ | Necesita un perfil de GitHub Sponsors; y `FUNDING.yml` se copiaría a cada proyecto. |
| Discussions | ❌ | ❌ | Foro para comunidades; no la hay. |
| Projects | ❌ | ❌ | Ver nota 2. |
| Pull requests | ✅ | ✅ | Todo entra por PR. |
| Pull requests → Creation allowed by | Collaborators only | — | Igual que Issues. |
| Allow merge commits | ❌ | ❌ | Un solo método: squash. |
| Allow squash merging | ✅ | ✅ | Un commit por sesión en `main`. |
| → Default commit message | Pull request title and description | Pull request title and description | El commit guarda el plan y el checklist del PR. |
| Allow rebase merging | ❌ | ❌ | Un solo método. |
| Always suggest updating pull request branches | ❌ | ❌ | Cada actualización vuelve a pasar CI. |
| Allow auto-merge | ❌ | — (gris) | No lo usamos: el agente mergea sus PRs y CI mergea los de Dependabot. |
| Automatically delete head branches | ✅ | ✅ | Borra la rama al mergear, también las de Dependabot. |
| Require contributors to sign off on web-based commits | ❌ | ❌ | Requisito legal (DCO) de proyectos con muchos contribuidores. |
| Allow comments on individual commits | ✅ | ✅ | Como viene. |
| Include Git LFS objects in archives | ❌ | ❌ | No usamos LFS. |
| Auto-close issues with merged linked pull requests | ✅ | ✅ | "Fixes #12" en un PR cierra el issue 12. |
| Danger Zone | nada | nada | |

**Nota 1 — Wikis.** Son páginas de documentación fuera del código, editables desde la web y
guardadas en un repositorio aparte. Los agentes no las ven al clonar, no se revisan en los PRs
y se desincronizan del código. Toda la documentación va en `docs/`, versionada con el código.
En repos privados con el plan Free, además, no existen.

**Nota 2 — Projects o `docs/ROADMAP.md`.** ROADMAP. Projects es un tablero tipo Trello sobre
issues, útil para equipos de personas. Para un dueño con sesiones de IA pierde en todo:
- *Organización*: ROADMAP se actualiza en el mismo PR que el código, así que nunca dice algo
  distinto de lo que hay en `main`; un tablero se actualiza aparte y se queda atrás.
- *Calidad para la IA*: la sesión lee ROADMAP al clonar, sin permisos extra; Projects exige la
  API GraphQL con un permiso (`project`) que las sesiones no suelen tener, y su contenido no
  pasa por la revisión del PR.
- *Tokens*: el agente lee de ROADMAP solo la sección que necesita (`grep` + rango de líneas);
  la API de Projects devuelve JSON con todos los campos de cada tarjeta.

## Access

| Opción | Plantilla | Proyecto | Por qué |
|---|---|---|---|
| Collaborators | solo tú | solo tú | Quien tenga acceso de escritura puede mergear. |
| Moderation options → Interaction limits | sin límite | — | Ya limitan Issues y Pull requests (Collaborators only). |

## Code and automation

| Sección | Plantilla | Proyecto | Por qué |
|---|---|---|---|
| Branches (reglas clásicas) | nada | nada | Usamos Rulesets, que las sustituyen. |
| Tags | nada | nada | La inmutabilidad de releases ya protege sus tags. |
| Rules → Rulesets | ver abajo | — | Los repos privados con el plan Free no los tienen. |
| Actions | ver abajo | ver abajo | |
| Models | nada | nada | GitHub Models (IA de GitHub); usamos Claude. |
| Webhooks | nada | nada | Avisan a otros servicios (Discord, un servidor…). Solo si un proyecto lo necesita, con una decisión en `docs/decisions/`. |
| Copilot | todo desactivado | todo desactivado | Revisión y agente de Copilot gastan peticiones de pago y duplican la revisión que ya hace Claude. |
| Environments | nada | nada al empezar | Cuando un proyecto despliegue, un environment `production` guarda sus secretos y puede exigir tu aprobación. |
| Codespaces | nada | nada | Trabajas con Claude Code. |
| Pages | desactivado | desactivado | Web pública de documentación; no la necesitamos. |

**Rulesets (Plantilla, o proyectos públicos).** *New ruleset → New branch ruleset*:
- *Ruleset name*: `main`; *Enforcement status*: **Active**; *Bypass list*: vacía.
- *Target branches*: **Include default branch**.
- Marca **Restrict deletions**, **Block force pushes**, **Require a pull request before
  merging** (*Required approvals*: 0) y **Require status checks to pass** → añade `ci`.
- Nada más: el check `ci` siempre informa, también en PRs de solo documentación, así que no
  bloquea nada que deba pasar.

**Actions → General.**
- *Actions permissions*: **Allow Almoon-D, and select non-Almoon-D, actions and reusable
  workflows**, con **Allow actions created by GitHub** y, en la lista,
  `astral-sh/setup-uv@*, dependabot/fetch-metadata@*`. Una acción nueva en un workflow se
  añade aquí en el mismo momento.
- **Require actions to be pinned to a full-length commit SHA**: ✅ (todas lo están).
- *Approval for running fork pull request workflows*: **Require approval for all external
  contributors** (Plantilla; en Proyecto no aparece).
- *Workflow permissions*: **Read repository contents and packages permissions**; **Allow
  GitHub Actions to create and approve pull requests**: ❌. Los workflows que escriben
  (release, el merge de Dependabot) piden su propio permiso.
- *Runners*, *Caches*: nada.

## Security

| Opción | Plantilla | Proyecto | Por qué |
|---|---|---|---|
| Private vulnerability reporting | ❌ | — | Para que extraños avisen de fallos; no hay usuarios. |
| Dependency graph | ✅ | ✅ | Base de las alertas. |
| Automatic dependency submission | ❌ | ❌ | uv no la necesita; gasta ejecuciones. |
| Dependabot alerts | ✅ | ✅ | |
| Dependabot security updates | ✅ | ✅ | Abre el arreglo en cuanto sale un aviso; CI lo mergea si no es major. |
| Grouped security updates | ✅ | ✅ | Un PR en lugar de varios. |
| Dependabot on Actions runners | ✅ | ✅ | Como viene; sus trabajos son gratis. |
| Code scanning (CodeQL) | ❌ | — | La plantilla apenas tiene código. En un proyecto público con código: **Default setup**. |
| Secret Protection / Push protection | ✅ | — si no aparece | Bloquea un push que contenga una clave. |
| Deploy keys | nada | nada | |
| Secrets and variables → Actions | nada | solo lo que pida un workflow | Nunca credenciales de producción (AGENTS.md). |
| Secrets and variables → Dependabot / Codespaces | nada | nada | |

## Integrations

| Opción | Plantilla | Proyecto | Por qué |
|---|---|---|---|
| GitHub Apps | Claude | Claude | La app de Claude necesita acceso al repo para las sesiones. |
| Email notifications | nada | nada | |
| Autolink references | nada | nada | Enlaza referencias a gestores externos (Jira…). |

## Tu cuenta (una sola vez, vale para todos los repos)

- *Settings → Billing and licensing → Budgets and alerts*: presupuesto de **Actions** de 0 €
  con **Stop usage when budget limit is reached**. Nunca pagas por error.
- *Settings → Planning* (Issue types, Issue fields): nada. Clasifican issues para equipos;
  aquí la planificación vive en `docs/`.
- *Settings → Applications → Claude*: acceso a cada repositorio nuevo (o a todos).
