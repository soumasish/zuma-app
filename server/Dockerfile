FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and install Python dependencies
COPY pyproject.toml ./
RUN pip install uv && uv pip install --system -e .

# Copy source code
COPY . .

# Make the run script executable
RUN chmod +x scripts/run.sh

# Expose port 9000
EXPOSE 9000

# Start the server using the run script
CMD ["./scripts/run.sh"] 