FROM python:3.12

# Create a user to run the app
RUN useradd appuser && mkdir /code && chown appuser /code

WORKDIR /code

COPY . /code/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make the entrypoint script executable
RUN chmod +x /code/entrypoint.sh

# Switch to non-root user
USER appuser
