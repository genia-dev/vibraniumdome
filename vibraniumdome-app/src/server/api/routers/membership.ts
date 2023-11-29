/* eslint-disable @typescript-eslint/ban-ts-comment */

import { z } from "zod";

import {
  createTRPCRouter,
  protectedProcedure,
  publicProcedure,
} from "~/server/api/trpc";

export const membershipRouter = createTRPCRouter({
  getOrCreate: protectedProcedure
    .input(z.object({ name: z.string().min(1) }))
    .mutation(async ({ ctx, input }) => {
  })
});
