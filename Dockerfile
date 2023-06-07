# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /prototype

# Copy the current directory contents into the container at /app
COPY . /prototype

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 8000 for Gunicorn
EXPOSE 8000


# Run deploy.sh script & Start Gunicorn
CMD ["sh", "deploy.sh"]