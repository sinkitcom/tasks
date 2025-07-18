# Docker Usage

This document explains how to use the TickTick Export Docker container.

## Basic Usage

```bash
docker run --rm -v $(pwd)/tasks:/app/tasks \
  -e TICKTICK_ACCESS_TOKEN=your_token_here \
  ghcr.io/sinkitcom/tasks:latest
```

## Environment Variables

- `TICKTICK_ACCESS_TOKEN` (required): Your TickTick API access token

## Command Line Options

- `--title-in-filename`: Include task title in filename (default: only task ID)

Example:
```bash
docker run --rm -v $(pwd)/tasks:/app/tasks \
  -e TICKTICK_ACCESS_TOKEN=your_token_here \
  ghcr.io/sinkitcom/tasks:latest \
  --title-in-filename
```

## Volume Mounts

Mount a local directory to `/app/tasks` to export files to your host system:

```bash
# Export to current directory's 'tasks' folder
-v $(pwd)/tasks:/app/tasks

# Export to specific path
-v /path/to/export:/app/tasks
```

## Building Locally

```bash
# Build the image
docker build -t ticktick-export .

# Run locally built image
docker run --rm -v $(pwd)/tasks:/app/tasks \
  -e TICKTICK_ACCESS_TOKEN=your_token_here \
  ticktick-export
```
