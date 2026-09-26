# Contributing to lead-platform

Thanks for looking. A quick word on where things stand, then how to work on the code.

## The project is finished

As of v1.0.0, lead-platform is complete and is not actively maintained. It works as-is, and no further updates are planned. Issues and pull requests are welcome, but they may go unanswered. Please don't wait on a reply: fork it, reuse it and grow it in whatever direction you need.

## License

The code is under the [MIT License](LICENSE), with no extra conditions. Use it, change it, host it or sell it. The license only asks that its notice stays with copies of the code.

A mention of lead-platform in your project is appreciated, never required.

## Changing the code

The API comes first. The backend owns the contract, and the frontend uses TypeScript types generated from it. The code keeps these rules (details in [`CLAUDE.md`](CLAUDE.md) and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)):

- **Views handle requests and responses only.** Business logic goes in `apps/*/services.py`: `Request → View → Serializer → Service → Database`.
- **Service functions are transactional**, and they are the only code that writes activity records. A change and its timeline entry are saved together, or neither is.
- **Status only changes through `change_lead_status`**, which enforces the transitions in `apps/leads/constants.py`.
- **Never hand-write API types in the frontend.** After changing a view or serializer, regenerate the schema and the types:

  ```sh
  cd backend && python manage.py spectacular --validate --fail-on-warn --file schema.yml
  cd ../frontend && pnpm exec openapi-typescript ../backend/schema.yml -o src/types/api.ts
  ```

Use Python 3.12 or later, Node.js 22 and [pnpm](https://pnpm.io/). These are the checks CI runs on every push and pull request, along with a Docker build and smoke test:

```sh
# backend/ (tests need SECRET_KEY and DATABASE_URL, e.g. sqlite:///:memory:)
pip install -r requirements.txt
flake8
python manage.py makemigrations --check --dry-run
python manage.py spectacular --validate --fail-on-warn --file schema.yml
pytest

# frontend/
pnpm install --frozen-lockfile
pnpm lint
pnpm test
pnpm build
```

The 99 backend tests cover authentication, token rotation and blacklisting, role permissions, lead visibility for each role, create and edit with the activities they record, every allowed and blocked status change, assignment, notes and their owners, filtering, search, ordering, pagination, the public form and its rate limit, the schema, and the production settings. The 74 frontend tests cover the auth guard and the shared token refresh, the login flow, the dashboard, the lead list and its query parameters, and the lead page's status, assignment and notes against a fake API that enforces the backend's status rules.

To release a fork, set `version` in `frontend/package.json`, add a `CHANGELOG.md` entry and push a `v*` tag. CI then publishes the container image to the GitHub Container Registry and creates the GitHub Release. See [`docs/DEPLOY.md`](docs/DEPLOY.md#ci-and-releases).
