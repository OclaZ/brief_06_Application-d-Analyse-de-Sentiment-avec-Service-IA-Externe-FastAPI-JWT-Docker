# Frontend Dockerfile
FROM node:20-bullseye AS builder

WORKDIR /app

# Enable corepack for pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile --shamefully-hoist

# Copy frontend code
COPY . .

# Build Next.js app
RUN pnpm build

# Production stage
FROM node:20-bullseye

WORKDIR /app

COPY --from=builder /app/package.json ./
COPY --from=builder /app/pnpm-lock.yaml ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

RUN corepack enable && corepack prepare pnpm@latest --activate
RUN pnpm install --prod --frozen-lockfile --shamefully-hoist

EXPOSE 3000

CMD ["pnpm", "start"]
