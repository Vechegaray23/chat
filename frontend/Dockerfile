FROM node:18-alpine
WORKDIR /app
COPY package.json vite.config.js tailwind.config.js postcss.config.js index.html /app/
COPY src /app/src
ARG VITE_API_URL=http://backend:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm install && npm run build
RUN mkdir -p /var/log
CMD npx vite preview --host 0.0.0.0 --port 5173 | tee /var/log/frontend.log
