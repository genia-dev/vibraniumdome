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
                "high_risk_threshold": 0.8,
                "low_risk_threshold": 0.2,
                "input_shields": [
                    {"type": "com.vibraniumdome.shield.input.semantic_similarity", "metadata": {}},
                    {"type": "com.vibraniumdome.shield.input.regex", "metadata": {}, "name": "policy number"},
                    {"type": "com.vibraniumdome.shield.input.captain", "metadata": {"model": "gpt-3.5-turbo", "model_vendor": "openai"}},
                    {"type": "com.vibraniumdome.shield.input.transformer", "metadata": {}},
                    {"type": "com.vibraniumdome.shield.input.prompt_safety", "metadata": {}},
                    {"type": "com.vibraniumdome.shield.input.sensitive_info_disc", "metadata": {}},
                    {"type": "com.vibraniumdome.shield.input.model_dos", "metadata": {"threshold": 10, "interval_sec": 60, "limit_by": "llm.user"}},
                ],
                "output_shields": [
                    {"type": "com.vibraniumdome.shield.output.regex", "metadata": {}, "name": "credit card"},
                    {"type": "com.vibraniumdome.shield.output.refusal", "metadata": {}},
                    {"type": "com.vibraniumdome.shield.output.refusal.canary_token_disc", "metadata": {"canary_tokens": []}},
                    {"type": "com.vibraniumdome.shield.output.sensitive_info_disc", "metadata": {}},
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
