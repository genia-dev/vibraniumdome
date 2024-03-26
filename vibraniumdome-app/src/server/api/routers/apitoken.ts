/* eslint-disable @typescript-eslint/ban-ts-comment */
import { z } from "zod";

import {
  createTRPCRouter,
  protectedProcedure,
  publicProcedure,
} from "~/server/api/trpc";

function generateApiKey(): string {
  const prefix = 'vibranium_';
  // @ts-ignore
  return prefix + [...Array(36)].map(() => Math.random().toString(36)[2] || '0').join('');
}


export const validateAPIToken = protectedProcedure
.query(async ({ ctx }) => {
   return ctx.db.aPIToken.findFirst({
    // @ts-ignore
    where: { user: { id: ctx.session.user.id } },
    select: {
      user: true,
    }
  });
})

export const apiTokenRouter = createTRPCRouter({
  createApiToken: protectedProcedure
    .input(z.object({ name: z.string().min(1) }))
    .mutation(async ({ ctx, input }) => {
      const token = generateApiKey()
      return ctx.db.aPIToken.create({
        data: {
          name: input.name,
          token: token,
          user: {
            // @ts-ignore
            connect: { id: ctx.session.user.id },
          },
        },
      });
    }),

  getAllByUser: protectedProcedure.query(async ({ ctx }) => {
    return ctx.db.aPIToken.findMany({
      orderBy: { createdAt: "desc" },
      // @ts-ignore
      where: { user: { id: ctx.session.user.id } },
    });
  }),
});
