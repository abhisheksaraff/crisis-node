FROM node:20-alpine

WORKDIR /app

# Copy dependency files
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Vite needs port 5173 by default
EXPOSE 5173

# IMPORTANT: --host is required to access Vite from outside the container
CMD ["npm", "run", "dev", "--", "--host"]