/* eslint-disable @typescript-eslint/ban-ts-comment */

import { z } from "zod";

import {
  createTRPCRouter,
  protectedProcedure,
  publicProcedure,
} from "~/server/api/trpc";

const defaultPolicy = {
  "shields_filter": "all",
  "high_risk_threshold": 0.8,
  "low_risk_threshold": 0.2,
  "redact_conversation": false,
  "input_shields": [
      {"type": "com.vibraniumdome.shield.input.semantic_similarity", "metadata": {}, "full_name": "Semantic Similarity"},
      {"type": "com.vibraniumdome.shield.input.regex", "metadata": {}, "full_name": "Regex"},
      {"type": "com.vibraniumdome.shield.input.captain", "metadata": {"model": "gpt-3.5-turbo", "model_vendor": "openai"}, "full_name": "Captain"},
      {"type": "com.vibraniumdome.shield.input.transformer", "metadata": {}, "full_name": "Transformer"},
      {"type": "com.vibraniumdome.shield.input.prompt_safety", "metadata": {}, "full_name": "Prompt Safety"},
      {"type": "com.vibraniumdome.shield.input.sensitive_info_disc", "metadata": {}, "full_name": "Sensitive Info Disclosure"},
      {"type": "com.vibraniumdome.shield.input.arbitrary_image", "metadata": {}, "full_name": "Arbitrary Image"},
      {"type": "com.vibraniumdome.shield.input.whitelist_urls", "metadata": {}, "full_name": "Whitelist URLs"},
      {"type": "com.vibraniumdome.shield.input.model_dos", "metadata": {"threshold": 10, "interval_sec": 60, "limit_by": "llm.user"}, "full_name": "Model Denial Of Service"},
      {"type": "com.vibraniumdome.shield.input.banned_ip", "metadata": {}, "full_name": "Banned IP"},
  ],
  "output_shields": [
      {"type": "com.vibraniumdome.shield.output.regex", "metadata": {}, "full_name": "Regex"},
      {"type": "com.vibraniumdome.shield.output.refusal", "metadata": {}, "full_name": "Model Refusal"},
      {"type": "com.vibraniumdome.shield.output.refusal.canary_token_disc", "metadata": {"canary_tokens": []}, "full_name": "Canary Token Disclosure"},
      {"type": "com.vibraniumdome.shield.output.sensitive_info_disc", "metadata": {}, "full_name": "Sensitive Info Disclosure"},
  ],
}

export const getPolicyByLLMAppApi = protectedProcedure
.input(z.object({ llmApp: z.string().min(1) }))
.query(async ({ ctx, input }) => {
  const membership = await ctx.db.membership.findFirst({
    where: { userId: ctx.session.user?.id },
  });
  var policy = await ctx.db.policy.findFirst({
    where: {
      createdById: membership?.teamId,
      llmApp: input.llmApp,
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
    policy = await ctx.db.policy.findFirst({
      where: {
        seq: -99
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
  }

  return policy
})

export const policyRouter = createTRPCRouter({
  create: protectedProcedure
    .input(z.object({ name: z.string().min(1), llmApp: z.string().min(1), content: z.string().min(1) }))
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
          llmApp: input.llmApp,
          createdBy: { connect: { id: membership?.teamId } },
        },
      });
    }),
  
  update: protectedProcedure
    .input(z.object({ id: z.string().min(1), name: z.string().min(1), llmApp: z.string().min(1), content: z.string().min(1) }))
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
          llmApp: input.llmApp,
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

  get: protectedProcedure
  .input(z.object({ id: z.string().min(1) }))
  .query(async ({ ctx, input }) => {
    const membership = await ctx.db.membership.findFirst({
      // @ts-ignore
      where: { userId: ctx.session.user.id },
    });
    
    const policy = await ctx.db.policy.findFirst({
      orderBy: { createdAt: "desc" },
      // @ts-ignore
      where: {
        id: input.id,
        createdBy: { id: membership?.teamId },
      },
    });

    return policy
  }),

  getDefaultPolicy: protectedProcedure.query(async ({ ctx }) => {
    const membership = await ctx.db.membership.findFirst({
      // @ts-ignore
      where: { userId: ctx.session.user.id },
    });

    const policy = await ctx.db.policy.findFirst({
      where: {
        createdBy: { id: membership?.teamId },
        seq: -99,
      },
      select: {
        id: true,
        seq: true,
        name: true,
        content: true,
        createdAt: false,
        updatedAt: false,
      },
    });
    return policy
  }),

  getBasePolicy: protectedProcedure.query(async ({ ctx }) => {
    return defaultPolicy
  }),

  getAll: protectedProcedure.query(async ({ ctx }) => {
    const membership = await ctx.db.membership.findFirst({
      // @ts-ignore
      where: { userId: ctx.session.user.id },
    });
    
    var policies = await ctx.db.policy.findMany({
      orderBy: { createdAt: "desc" },
      where: { 
        createdBy: { id: membership?.teamId },
      },
    });

    if (!policies || policies.length == 0) {
      await ctx.db.policy.create({
        // @ts-ignore
        data: {
          name: "Default Policy",
          seq: -99,
          llmApp: "Default Any",
          content: defaultPolicy,
          createdBy: { connect: { id: membership?.teamId } },
        },
      });

      policies = await ctx.db.policy.findMany({
        orderBy: { createdAt: "desc" },
        where: { 
          createdBy: { id: membership?.teamId },
        },
      });
    }

    return policies
  }),
});
