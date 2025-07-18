# Workflow Customization

This document explains how to customize the TickTick export workflow for your needs.

## Basic Workflow Setup

Create `.github/workflows/ticktick-export.yml` in your repository:

```yaml
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

## Customization Options

### Export Schedule

Change the cron schedule to fit your needs:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
    - cron: '0 9 * * *'    # Daily at 9 AM
    - cron: '0 9 * * 1'    # Weekly on Monday at 9 AM
```

### Export Path

Export to a different directory:

```yaml
jobs:
  export:
    uses: sinkitcom/tasks/.github/workflows/export.yml@main
    with:
      export_path: 'my-tasks/'
    secrets:
      TICKTICK_ACCESS_TOKEN: ${{ secrets.TICKTICK_ACCESS_TOKEN }}
```

### Filename Format

Include task titles in filenames:

```yaml
jobs:
  export:
    uses: sinkitcom/tasks/.github/workflows/export.yml@main
    with:
      title_in_filename: true
    secrets:
      TICKTICK_ACCESS_TOKEN: ${{ secrets.TICKTICK_ACCESS_TOKEN }}
```

### Multiple Export Jobs

Export to different paths with different settings:

```yaml
name: Export TickTick Tasks

on:
  schedule:
    - cron: '0 * * * *'
  workflow_dispatch:

jobs:
  export-with-ids:
    uses: sinkitcom/tasks/.github/workflows/export.yml@main
    with:
      export_path: 'tasks-by-id/'
      title_in_filename: false
    secrets:
      TICKTICK_ACCESS_TOKEN: ${{ secrets.TICKTICK_ACCESS_TOKEN }}
      
  export-with-titles:
    uses: sinkitcom/tasks/.github/workflows/export.yml@main
    with:
      export_path: 'tasks-by-title/'
      title_in_filename: true
    secrets:
      TICKTICK_ACCESS_TOKEN: ${{ secrets.TICKTICK_ACCESS_TOKEN }}
```

## Manual Triggers

The workflow includes `workflow_dispatch` for manual triggering:

1. Go to your repository's Actions tab
2. Select "Export TickTick Tasks" workflow
3. Click "Run workflow"

## Troubleshooting

### No Changes Committed

If tasks haven't changed, the workflow won't create a commit. This is normal behavior.

### Authentication Issues

Ensure your `TICKTICK_ACCESS_TOKEN` secret is set correctly:

1. Go to repository Settings → Secrets and variables → Actions
2. Add `TICKTICK_ACCESS_TOKEN` with your token value
3. The token should have `tasks:read` scope

### File Conflicts

If you're editing exported files manually, you may encounter conflicts. Consider:

1. Using a separate branch for exports
2. Adding `.gitignore` entries for files you don't want tracked
3. Using different export paths for different purposes
