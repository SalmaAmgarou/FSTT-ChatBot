# Use Node.js image as base
FROM node:14-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Stage 2: Production Environment
FROM nginx:alpine

# Copy the build files to Nginx server
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 to the outer world
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
