# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV  APP_SETTINGS=config.DevelopmentConfig

# Remove the existing migrations directory, if any
RUN rm -rf migrations
# Initialize the database
RUN flask db init

# Perform the database migrations
RUN flask db migrate
RUN flask db upgrade



# Run app.py when the container launches
CMD ["python", "app.py"]