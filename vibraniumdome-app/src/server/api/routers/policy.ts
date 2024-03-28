/* eslint-disable @typescript-eslint/ban-ts-comment */

import { z } from "zod";

import {
  createTRPCRouter,
  protectedProcedure,
  publicProcedure,
} from "~/server/api/trpc";
/*
NOTE: FOUND ALSO IN prisma/seed.ts
*/
const basePolicy = {
  "shields_filter": "all",
  "high_risk_threshold": 0.8,
  "low_risk_threshold": 0.2,
  "redact_conversation": false,
  "input_shields": [
    { "type": "com.vibraniumdome.shield.input.transformer", "metadata": {}, "full_name": "Prompt injection transformer shield" },
    { "type": "com.vibraniumdome.shield.input.model_dos", "metadata": { "threshold": 10, "interval_sec": 60, "limit_by": "llm.user" }, "full_name": "Model denial of service shield" },
    { "type": "com.vibraniumdome.shield.input.captain", "metadata": { "model": "gpt-3.5-turbo", "model_vendor": "openai" }, "full_name": "Captain's shield" },
    { "type": "com.vibraniumdome.shield.input.semantic_similarity", "metadata": {}, "full_name": "Semantic vector similarity shield" },
    { "type": "com.vibraniumdome.shield.input.regex", "metadata": {}, "full_name": "Regex input shield" },
    { "type": "com.vibraniumdome.shield.input.prompt_safety", "metadata": {}, "full_name": "Prompt safety moderation shield" },
    { "type": "com.vibraniumdome.shield.input.sensitive_info_disc", "metadata": {}, "full_name": "PII and Sensetive information disclosure shield" },
    { "type": "com.vibraniumdome.shield.input.no_ip_in_urls", "metadata": {}, "full_name": "No IP in URLs shield" },
    { "type": "com.vibraniumdome.shield.input.invisible", "metadata": {}, "full_name": "Invisible input characters shield" },
  ],
  "output_shields": [
    { "type": "com.vibraniumdome.shield.output.refusal.canary_token_disc", "metadata": { "canary_tokens": [] }, "full_name": "Canary token disclosure shield" },
    { "type": "com.vibraniumdome.shield.output.refusal", "metadata": {}, "full_name": "Model output refusal shield" },
    { "type": "com.vibraniumdome.shield.output.sensitive_info_disc", "metadata": {}, "full_name": "PII and sensetive information disclosure shield" },
    { "type": "com.vibraniumdome.shield.output.regex", "metadata": {}, "full_name": "Regex output shield" },
    { "type": "com.vibraniumdome.shield.output.arbitrary_image", "metadata": {}, "full_name": "Arbitrary image domain URL shield" },
    { "type": "com.vibraniumdome.shield.output.whitelist_urls", "metadata": {}, "full_name": "White list domains URL shield" },
    { "type": "com.vibraniumdome.shield.output.invisible", "metadata": {}, "full_name": "Invisible output characters shield" },
  ],
}

export const getBasePolicy = protectedProcedure
  .query(async ({ ctx }) => {
    return basePolicy
  })

export const getPolicyByLLMAppApi = protectedProcedure
  .input(z.object({ llmAppName: z.string().min(1) }))
  .query(async ({ ctx, input }) => {
    const membership = await ctx.db.membership.findFirst({
      where: { userId: ctx.session.user?.id },
    });
    var policy = await ctx.db.policy.findFirst({
      where: {
        createdById: membership?.teamId,
        llmApp: input.llmAppName,
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
          seq: -99,
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
    return basePolicy
  }),

  getAll: protectedProcedure.query(async ({ ctx }) => {
    const membership = await ctx.db.membership.findFirst({
      // @ts-ignore
      where: { userId: ctx.session.user.id },
    });

    const policies = await ctx.db.policy.findMany({
      orderBy: { createdAt: "desc" },
      where: {
        createdBy: { id: membership?.teamId },
      },
    });

    return policies
  }),
});
