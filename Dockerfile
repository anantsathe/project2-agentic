# Use a lightweight Python image
FROM python:3.12-slim

# Use `uv` for fast package installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Set working directory
WORKDIR /app


ENV AIPROXY_TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjEwMDE2NzlAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.nYcjVkKm_z6CXHHtGFbRTZ9lY2NS-9rWqtUGaRLjE0k"

# Copy only required files (excluding files in .dockerignore)
COPY . /app


RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt



# Expose the FastAPI app's port
EXPOSE 8000

# Use uvicorn to run the FastAPI app
CMD ["/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]