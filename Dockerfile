# Use a lightweight Python image as the base
FROM python:3.11-slim

# Set a working directory for the application
WORKDIR /Flask

# Copy the requirements.txt file
COPY requirements.txt ./

# Install dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port where the Flask app will run (default Flask port)
EXPOSE 5000

# Set the command to execute when the container starts
CMD ["flask", "--app", "Flask", "run", "-h", "0.0.0.0", "-p", "5000"]