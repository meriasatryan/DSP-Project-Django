# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /final_project

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# # Use the official Python 3.8 image as the base image
# FROM python:3.8

# # Set the working directory in the container
# WORKDIR /final_project

# # Copy the requirements.txt file to the container
# COPY requirements.txt .

# # Install the app's dependencies
# RUN pip install -r requirements.txt

# # Copy the rest of the app's source code to the container
# COPY . .

# # Collect the static files
# RUN python manage.py collectstatic --noinput