FROM node

WORKDIR /frontend

COPY . .

RUN npm install
# RUN npm run build
EXPOSE 3000
# Todo マルチステージビルド採用して軽量化
CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]