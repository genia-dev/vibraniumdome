/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-return */
/* eslint-disable @typescript-eslint/no-unnecessary-type-assertion */
/* eslint-disable @typescript-eslint/ban-ts-comment */
import { PrismaAdapter } from "@next-auth/prisma-adapter";
import {
  getServerSession,
  type DefaultSession,
  type NextAuthOptions,
} from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";

import { env } from "~/env.mjs";
import { db } from "~/server/db";

import jwt from "jsonwebtoken"
const { compareSync } = require('bcryptjs');

/**
 * Module augmentation for `next-auth` types. Allows us to add custom properties to the `session`
 * object and keep type safety.
 *
 * @see https://next-auth.js.org/getting-started/typescript#module-augmentation
 */
declare module "next-auth" {
  interface Session extends DefaultSession {
    jwt: string,
    user: {
      id: string;
      // ...other properties
      // role: UserRole;
    } & DefaultSession["user"];
  }

  // interface User {
  //   // ...other properties
  //   // role: UserRole;
  // }
}

function generateOpenSearchJWT() {
  const payload = {
    sub: 'admin',
    iat: Math.floor(Date.now() / 1000),
  };

  const secretKey = process.env.OPENSEARCH_JWT_HMAC_SIGNING_KEY;
  // @ts-ignore
  const token = jwt.sign(payload, secretKey, { algorithm: 'HS256' });
  return token
}

/**
 * Options for NextAuth.js used to configure adapters, providers, callbacks, etc.
 *
 * @see https://next-auth.js.org/configuration/options
 */
export const authOptions: NextAuthOptions = {
  callbacks: {
    async session({ session, user, token }) {
      const currUser = await db.user.findUnique({
        //@ts-ignore
        where: { email: session.user.email.toLowerCase() },
      });

      return {
        ...session,
        user: {
          ...session.user,
          id: currUser?.id,
        },
        jwt: session.jwt || generateOpenSearchJWT(),
      }
    },
  },
  adapter: PrismaAdapter(db),
  debug: process.env.NODE_ENV === "development",
  session: {
		strategy: "jwt",
		// Seconds - How long until an idle session expires and is no longer valid.
		maxAge: 30 * 24 * 60 * 60 // 30 days
	},
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text", placeholder: "admin" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials, req) {
        const currUser = await db.user.findUnique({
          //@ts-ignore
          where: { email: credentials.email.toLowerCase() },
        });
        //@ts-ignore
        const isValid = await compareSync(credentials.password, currUser.password);
        //@ts-ignore
        if (!currUser || !isValid) {
          return null;
        }
        return currUser
      }
    }),
    GoogleProvider({
      clientId: env.GOOGLE_CLIENT_ID!,
      clientSecret: env.GOOGLE_CLIENT_SECRET!,
      allowDangerousEmailAccountLinking: true,
    }),
    /**
     * ...add more providers here.
     *
     * Most other providers require a bit more work than the Discord provider. For example, the
     * GitHub provider requires you to add the `refresh_token_expires_in` field to the Account
     * model. Refer to the NextAuth.js docs for the provider you want to use. Example:
     *
     * @see https://next-auth.js.org/providers/github
     */
  ],
};

/**
 * Wrapper for `getServerSession` so that you don't need to import the `authOptions` in every file.
 *
 * @see https://next-auth.js.org/configuration/nextjs
 */
export const getServerAuthSession = () => getServerSession(authOptions);
