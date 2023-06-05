# Use an official Python runtime as a parent image
FROM python:3.11.3-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 for the Django application
EXPOSE 8000

RUN python manage.py makemigrations

RUN python manage.py migrate

# Start the Django application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "prototype.wsgi:application"]