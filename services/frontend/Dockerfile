FROM oven/bun:alpine

WORKDIR /app

# Install curl for container healthcheck routines
RUN apk add --no-cache curl

# Install app dependencies using Bun
COPY package.json ./
RUN bun install

# Copy frontend source code
COPY . .

# Expose Vite development server port
EXPOSE 3000

# Start Vue development server bound to internal docker routing
CMD ["bun", "run", "dev", "--host", "0.0.0.0", "--port", "3000"]
