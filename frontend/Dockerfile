FROM node

WORKDIR /frontend

COPY . .

RUN npm install
RUN npm run build
EXPOSE 3000
# Todo マルチステージビルド採用して軽量化