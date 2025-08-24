# syntax=docker/dockerfile:1.4
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json ./
RUN npm install

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
ENV NEXT_TELEMETRY_DISABLED 1

# Build the Next.js application
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Set non-root user for better security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Set the correct permissions
RUN mkdir -p /app/.next/cache && chown -R nextjs:nodejs /app

# Copy needed files for production
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/package.json ./package.json

# Copy standalone directory - optimized for containerization
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Set user to non-root for better security
USER nextjs

EXPOSE 6969

ENV PORT 6969
ENV HOSTNAME "0.0.0.0"

# Start the Next.js application using the standalone server.js
CMD ["node", "server.js"]
