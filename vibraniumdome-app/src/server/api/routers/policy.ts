/* eslint-disable @typescript-eslint/ban-ts-comment */

import { z } from "zod";

import {
  createTRPCRouter,
  protectedProcedure,
  publicProcedure,
} from "~/server/api/trpc";


export const getPolicyByLLMAppApi = protectedProcedure
.input(z.object({ llmAppName: z.string().min(1) }))
.query(async ({ ctx, input }) => {
  const membership = await ctx.db.membership.findFirst({
    where: { userId: ctx.session.user?.id },
  });
  const policy = await ctx.db.policy.findFirst({
    where: {
      createdById: membership?.teamId,
    },
    select: {
      id: true,
      seq: false,
      name: true,
      content: true,
      createdAt: false,
      updatedAt: false,
    },
  });
  
  if (!policy) {
    return {
      "id": "-99",
      "name": "Default Policy",
      "content": {
          "shields_filter": "all",
          "input_shields": [
              {"type": "llm_shield", "metadata": {"model": "gpt-3.5-turbo", "model_vendor": "openai"}},
              {"type": "regex_shield", "metadata": {}, "name": "policy number"},
              {"type": "transformer_shield", "metadata": {}},
              {"type": "vector_db_shield", "metadata": {}},
          ],
          "output_shields": [
              {"type": "llm_shield", "metadata": {"model": "gpt-3.5-turbo", "model_vendor": "openai"}},
              {"type": "regex_shield", "metadata": {}},
              {"type": "transformer_shield", "metadata": {}},
              {"type": "vector_db_shield", "metadata": {}},
              {"type": "refusal_shield", "metadata": {}},
              {"type": "sensitive_shield", "metadata": {}},
          ],
      },
    }
  }

  return policy
})

export const policyRouter = createTRPCRouter({
  create: protectedProcedure
    .input(z.object({ name: z.string().min(1), llmAppName: z.string().min(1), content: z.string().min(1) }))
    .mutation(async ({ ctx, input }) => {
      const membership = await ctx.db.membership.findFirst({
        // @ts-ignore
        where: { userId: ctx.session.user.id },
      });
      return ctx.db.policy.create({
        // @ts-ignore
        data: {
          name: input.name,
          content: JSON.parse(input.content),
          llmApp: input.llmAppName,
          createdBy: { connect: { id: membership?.teamId } },
        },
      });
    }),
  
  update: protectedProcedure
    .input(z.object({ id: z.string().min(1), name: z.string().min(1), llmAppName: z.string().min(1), content: z.string().min(1) }))
    .mutation(async ({ ctx, input }) => {
      const membership = await ctx.db.membership.findFirst({
        // @ts-ignore
        where: { userId: ctx.session.user.id },
      });

      return ctx.db.policy.update({
        // @ts-ignore
        where: {
          id: input.id,
          createdBy: { id: membership?.teamId },
        },
        data: {
          name: input.name,
          content: JSON.parse(input.content),
          llmApp: input.llmAppName,
          createdBy: { connect: { id: membership?.teamId } },
        },
      });
    }),
  
  delete: protectedProcedure
  .input(z.object({ id: z.string().min(1) }))
  .mutation(async ({ ctx, input }) => {
    const membership = await ctx.db.membership.findFirst({
      // @ts-ignore
      where: { userId: ctx.session.user.id },
    });

    return ctx.db.policy.delete({
      // @ts-ignore
      where: {
        id: input.id,
        createdBy: { id: membership?.teamId },
      },
    });
  }),

  getLatest: protectedProcedure.query(async ({ ctx, input }) => {
    const membership = await ctx.db.membership.findFirst({
      // @ts-ignore
      where: { userId: ctx.session.user.id },
    });

    return ctx.db.policy.findFirst({
      orderBy: { createdAt: "desc" },
      // @ts-ignore
      where: { createdBy: { id: membership.teamId } },
    });
  }),

  getAll: protectedProcedure.query(async ({ ctx }) => {
    const membership = await ctx.db.membership.findFirst({
      // @ts-ignore
      where: { userId: ctx.session.user.id },
    });
    
    return ctx.db.policy.findMany({
      orderBy: { createdAt: "desc" },
      // @ts-ignore
      where: { createdBy: { id: membership.teamId } },
    });
  }),
});
