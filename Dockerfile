FROM frappe/erpnext-worker:version-15

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Copy your app into the container
COPY . /home/frappe/frappe-bench/apps/predictive_manufacturing

# Install the app into the bench
RUN bench get-app predictive_manufacturing /home/frappe/frappe-bench/apps/predictive_manufacturing \
    && bench --site site1.local install-app predictive_manufacturing

# Expose ERPNext default port
EXPOSE 8000

# Start bench when container runs
CMD ["bench", "start"]
