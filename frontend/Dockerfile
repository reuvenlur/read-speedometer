# Use Nginx as the base image for serving static files
FROM nginx:stable-alpine

# Set the working directory inside the container
WORKDIR /usr/share/nginx/html

# Copy the frontend files (HTML, JS, CSS, PDF) to the container
COPY index.html ./
COPY app.js ./
COPY example.pdf ./
COPY styles.css ./

# Expose the port for Nginx
EXPOSE ${FRONTEND_PORT}

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
