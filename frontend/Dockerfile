# Use a lightweight Node.js image
FROM node:23.7-alpine3.21

WORKDIR /app

# Install dependencies (for efficient caching)
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the project files
COPY . .

# Build the svelte app
RUN npm run build

# Expose the port svelte runs on
EXPOSE 4173

# Run the svelte server
CMD npm run preview -- --host