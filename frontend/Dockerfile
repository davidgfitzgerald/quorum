# Use a lightweight Node.js image
FROM node:23.7-alpine3.21

WORKDIR /app

# Install dependencies (for efficient caching)
COPY package.json ./
RUN npm install

# Copy the rest of the project files
COPY . .

# Expose the port svelte runs on
EXPOSE 5173

# Run the svelte dev server
CMD npm run dev
