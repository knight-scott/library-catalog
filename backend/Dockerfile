# Use official Python base image
FROM python:3

# Set the working directory inside the container
WORKDIR /backend

#Copy the Flask app files into the container
COPY ./backend /backend

# Copy the requirements.txt file from the root directory to the container
COPY ../requirements.txt /backend/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /backend/requirements.txt

# Expose the Flask app port
EXPOSE 5001

# Run the Flask app
# Comment out for production
CMD ["python", "app.py"]

# Run Gunicorn to serve the app in production
# comment out Flask for development
# CMD ["gunicorn", "-b", "0.0.0.0:5001", "backend.app:app"]
