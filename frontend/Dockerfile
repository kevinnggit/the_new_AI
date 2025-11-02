

# Stage 1: Build
# Node.js zum Bauen der Vue-App
FROM node:18-alpine as build-stage

WORKDIR /app

# Dependencies installieren
COPY package*.json ./
RUN npm install

# Code kopieren
COPY . .

# Für Production bauen
RUN npm run build

# Stage 2: Production
# Nginx zum Ausliefern der statischen Dateien
FROM nginx:stable-alpine as production-stage

# Gebaute Dateien aus der Build-Stage holen
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Port 80 freigeben
EXPOSE 80

# Nginx starten
CMD ["nginx", "-g", "daemon off;"]
