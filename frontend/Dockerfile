# Base image
FROM node:14-alpine as build-stage

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the application files
COPY . .

# Build the React app
RUN npm run build

FROM nginx:alpine as production-stage

RUN rm /etc/nginx/conf.d/default.conf

# Copy the NGINX configuration file
COPY --from=build-stage /app/nginx.conf /etc/nginx/conf.d

# Copy the built React app from the build-stage to the NGINX container
COPY --from=build-stage /app/build /usr/share/nginx/html

# Copy the SSL certificate and key to the NGINX container
COPY ./certs/localhost.crt /etc/ssl/certs/localhost.crt
COPY ./certs/localhost.key /etc/ssl/private/localhost.key



# EXPOSE 443
EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]