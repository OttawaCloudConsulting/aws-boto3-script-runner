# Use the official Python 3.10 image as the base image
FROM python:3.10

# Install boto3
RUN pip install boto3

# Set the default CMD to the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

CMD ["/usr/local/bin/entrypoint.sh"]
