# Vibranium-App

## Stack
- [T3 Stack](https://create.t3.gg/)
- [Next.js](https://nextjs.org)
- [NextAuth.js](https://next-auth.js.org)
- [Prisma](https://prisma.io)
- [Tailwind CSS](https://tailwindcss.com)
- [tRPC](https://trpc.io)

## Installation

### Docker-Compose
```
docker-compose up --build
```

### Local

- Node v20.8.1 (+)
```
brew install node
```

- MySQL

```
brew install mysql
brew services start mysql
```

#### Run Vibranium-App
```
git clone git@github.com:genia-dev/vibraniumdome.git
cd vibraniumdome/vibraniumdome-app
yarn
npx prisma db seed
yarn dev
```

#### To connect the local MySQL:
```
mysql -u root vibraniumdome
```

## Usage Operations

### To reset the database:
```
npx prisma db push --force-reset
```

### To initialize the database:
```
npx prisma db seed
```

### To get browser db viewer client:
```
npx prisma studio
```

### To reset the database & seed:
```
yarn db:reset
```

### Get the current policy for LLM app
```
curl -v "http://localhost:3000/api/trpc/policies?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22llmAppId%22%3A%22clolkhhq10009n0nes7kj68jz%22%7D%7D%7D" -H "Authorization: Bearer vibranium_hvencwoacfzmon003ltkyfce6wugf5w7pt9l"
```
