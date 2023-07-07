# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /workorders

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the project dependencies including the PostgreSQL client library
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt

# Copy the project code to the container
COPY . .

# Expose the port the Django app will run on
EXPOSE 8000

# Define the command to run the Django development server
CMD ["python", "workorders/manage.py", "runserver", "0.0.0.0:8000"]
