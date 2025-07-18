# TickTick Export

A Docker-based tool to automatically export your TickTick tasks to markdown files. Perfect for creating automated backups of your tasks in your own repositories.

## What This Project Does

This project provides:
- **Docker container** that exports TickTick tasks to markdown files with frontmatter
- **GitHub Action workflow** for automated hourly exports in your private repository  
- **Markdown files** with structured frontmatter (status, priority, dates, etc.)
- **Hierarchical task organization** with proper parent-child relationships

## Quick Start

### Option 1: Use in GitHub Actions (Recommended)

Add this reusable workflow to your private repository to automatically export your TickTick tasks every hour:

```yaml
# .github/workflows/ticktick-export.yml
name: Export TickTick Tasks

on:
  schedule:
    - cron: '0 * * * *'  # Every hour
  workflow_dispatch:  # Manual trigger

jobs:
  export:
    uses: sinkitcom/tasks/.github/workflows/export.yml@main
    secrets:
      TICKTICK_ACCESS_TOKEN: ${{ secrets.TICKTICK_ACCESS_TOKEN }}
```

### Option 2: Run Docker Container Locally

```bash
docker run --rm -v $(pwd)/tasks:/app/tasks \
  -e TICKTICK_ACCESS_TOKEN=your_token_here \
  ghcr.io/sinkitcom/tasks:latest
```

## Setup

1. **Get Access Token**: Follow the [access token guide](docs/getting-access-token.md)
2. **Add Secret**: In your repository settings, add `TICKTICK_ACCESS_TOKEN` as a secret
3. **Add Workflow**: Copy the workflow file above to `.github/workflows/ticktick-export.yml`

## Output Format

Tasks are exported as markdown files with YAML frontmatter:

```markdown
---
title: My Important Task
project: Work
icon: ⬜
priority: 🔴
dueDate: 2025-07-20 15:00:00
---

## Description
Task description here

## Subtasks
- [[subtask-file|Subtask Title]]
```

## Documentation

- [Getting Access Token](docs/getting-access-token.md) - How to obtain TickTick API credentials
- [Docker Usage](docs/docker-usage.md) - Advanced Docker configuration options
- [Workflow Customization](docs/workflow-customization.md) - Customize the export workflow

## Container Registry

The Docker image is available at:
- `ghcr.io/sinkitcom/tasks:latest`
- `ghcr.io/sinkitcom/tasks:v1.0.0`
