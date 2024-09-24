# Node.js Dockerfile
FROM node:20

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the app code
COPY . .

# Expose port
EXPOSE 8000

# Start Node.js server
CMD ["node", "server.js"]
