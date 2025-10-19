# Stage 1: Build-Umgebung
# Verwendet ein Node.js Image, um die Vue-Anwendung zu bauen
FROM node:18-alpine as build-stage

WORKDIR /app

# Kopiert package.json und package-lock.json und installiert Abhängigkeiten
COPY package*.json ./
RUN npm install

# Kopiert den restlichen Quellcode
COPY . .

# Baut die Anwendung für die Produktion
RUN npm run build

# Stage 2: Produktions-Umgebung
# Verwendet einen schlanken Nginx-Server, um die statischen Dateien auszuliefern
FROM nginx:stable-alpine as production-stage

# Kopiert die gebauten Dateien aus der Build-Stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Gibt den Port 80 frei, den Nginx standardmäßig verwendet
EXPOSE 80

# Startet Nginx, wenn der Container läuft
CMD ["nginx", "-g", "daemon off;"]
