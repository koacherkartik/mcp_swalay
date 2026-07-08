# mcp_swalay

## Create the conda environment

From the project root, run:

```bash
conda env create -f environment.yml
conda activate mcp-drdo
```

## Run the project

```bash
python main.py
```

## Run with Docker Compose

```bash
docker compose up --build -d
docker compose logs -f mcp_server
docker compose down
```

## Export environment for sharing

```bash
conda env export --name mcp-drdo --no-builds > environment.lock.yml
```
