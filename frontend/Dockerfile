FROM public.ecr.aws/bitnami/node:14.17.0-prod as builder

ARG REACT_APP_API_URL

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json
RUN npm install --silent --unsafe-perm node-sass
RUN npm install --silent    
RUN npm install react-scripts@3.0.1 -g --silent
COPY . /app
RUN npm run build

# production environment

FROM public.ecr.aws/nginx/nginx:1.21-alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY --from=builder /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
