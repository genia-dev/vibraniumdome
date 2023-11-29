import { policyRouter, getPolicyByLLMAppApi } from "~/server/api/routers/policy";
import { membershipRouter } from "~/server/api/routers/membership";
import { apiTokenRouter } from "~/server/api/routers/apitoken";
import { createTRPCRouter } from "~/server/api/trpc";

/**
 * This is the primary router for your server.
 *
 * All routers added in /api/routers should be manually added here.
 */
export const appRouter = createTRPCRouter({
  policy: policyRouter,
  membership: membershipRouter,
  apitoken: apiTokenRouter,
  policies: getPolicyByLLMAppApi,
});

// export type definition of API
export type AppRouter = typeof appRouter;
