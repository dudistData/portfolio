FROM apache/airflow:2.9.1

# We switch to the root user to install some system-level packages if needed later,
# but for now it's just best practice to explicitly manage users.
USER root

# Install any system-level packages here, for example:
# RUN apt-get update \
#   && apt-get install -y --no-install-recommends \
#          vim \
#   && apt-get autoremove -yqq --purge \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user to install Python packages.
# Airflow runs as this user.
USER airflow

# Copy our requirements file into the image
COPY requirements.txt /requirements.txt

# Install the Python packages listed in requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
