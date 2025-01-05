# Use Nginx base image
FROM nginx:stable-alpine

# Set working directory for Nginx
WORKDIR /usr/share/nginx/html

# Copy frontend files to container
COPY index.html ./  
COPY app.js ./      
COPY some_pdf.pdf ./ 
COPY styles.css ./  

# Expose port for Nginx
EXPOSE ${FRONTEND_PORT}

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
