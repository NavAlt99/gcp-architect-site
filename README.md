# GCP Architect Roadmap Site

Static, credential-free learning site generated from the roadmap Markdown source and the Brightloaf narrative. Open `index.html` directly for browsing, or serve this directory with any static HTTP server.

## Rebuild and validate

From the parent RoadMap directory:

```bash
python3 gcp-architect-site/scripts/build_site.py \
  --roadmap gcp-architect-roadmap.md
```

The command repairs the generated pages, writes `generated/manifest.md`, validates links/content/specs, and runs the shared diagram integration checks. The roadmap can also be supplied with `ROADMAP_PATH`.

## Optional hands-on work

The pages are safe to read without credentials. Any live cloud work is opt-in and should use a disposable project, a confirmed region, a budget alert, least-privilege identity, and an explicit cleanup step. Demo snippets expect `DEMO_PROJECT_ID`, compare it with the active gcloud project, and require a reviewed Terraform plan before apply.

```bash
gcloud auth application-default login
gcloud config set project "$DEMO_PROJECT_ID"
terraform init
terraform validate
terraform plan -var="project_id=$DEMO_PROJECT_ID"
```

Never commit Terraform state, service-account keys, tokens, or customer data. Verify current pricing, quotas, product behavior, and exam guidance against authoritative documentation before using them in production.

## Site contract

Each canonical roadmap topic has six interactive SVG views (D1–D6), a Cloud City analogy scene, a mapping table, four review bands, a failure/trade-off depth ladder, and either a guarded demo or a read-only practice exercise. Diagram JSON includes summaries, steps, telemetry checks, and at least three failure scenarios.
