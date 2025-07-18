# Docker Usage

Simple guide to run the TickTick Export Docker container.

## Basic Usage

```bash
docker run --rm \
  -v $(pwd)/tasks:/app/tasks \
  -e TICKTICK_ACCESS_TOKEN=your_token_here \
  ghcr.io/sinkitcom/tasks:latest
```

### Alternative: Using .env file

Create a `.env` file with your token:
```bash
echo "TICKTICK_ACCESS_TOKEN=your_token_here" > .env
```

Then run with the .env file:
```bash
docker run --rm \
  -v $(pwd)/tasks:/app/tasks \
  --env-file .env \
  ghcr.io/sinkitcom/tasks:latest
```

This will:
- Export your TickTick tasks to the `tasks/` folder in your current directory
- Create markdown files named by task ID (e.g., `687a0154945ded7741d79393.md`)
- Organize tasks by project in subdirectories

## Required Setup

1. **Get your access token** - Follow the [access token guide](getting-access-token.md)
2. **Create export directory** - `mkdir tasks`
3. **Set your token** - Either use `-e TICKTICK_ACCESS_TOKEN=your_token` or create a `.env` file
4. **Run the command above**

## Options

- Add `--title-in-filename` to include task titles in filenames (makes longer filenames)

## Volume Mount

The `-v $(pwd)/tasks:/app/tasks` part mounts your local `tasks/` directory to the container's `/app/tasks` directory where files are created.

You can change `$(pwd)/tasks` to any local path you want:
```bash
-v /path/to/your/folder:/app/tasks
```
