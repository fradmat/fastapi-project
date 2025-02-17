# Use a lightweight Python base image
FROM continuumio/miniconda3:latest

# Set a working directory in the container
WORKDIR /app

# Copy requirements first (for better caching)
COPY environment_app.yaml /app/environment_app.yaml

# Install dependencies
RUN conda env create -f environment_app.yaml

# This approach changes the default shell in Docker to always run in the conda env
SHELL ["conda", "run", "-n", "control", "/bin/bash", "-c"]

# Copy the rest of project
COPY local.py webapp.py /app/

# Expose the default FastAPI port
EXPOSE 8000

CMD ["conda", "run", "-n", "control", "uvicorn", "webapp:app", "--host", "0.0.0.0", "--port", "8000"]

