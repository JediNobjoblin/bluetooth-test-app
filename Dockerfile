# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Install the necessary Bluetooth Libraries
RUN apt-get update && apt-get install -y \
bluez \
libbluetooth-dev \
build-essential \
pkg-config \
libglib2.0-dev \
&& apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=BluetoothTestApp

# Run bluetooth_test.py when the container launches
CMD ["python3", "src/main.py"]
