FROM node:18-alpine
WORKDIR /app
COPY package.json vite.config.js tailwind.config.js postcss.config.js index.html /app/
COPY src /app/src
RUN npm install && npm run build
CMD ["npx", "vite", "preview", "--host", "0.0.0.0", "--port", "5173"]
