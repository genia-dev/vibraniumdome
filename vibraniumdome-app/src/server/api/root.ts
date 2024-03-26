import { policyRouter, getPolicyByLLMAppApi, getBasePolicy } from "~/server/api/routers/policy";
import { membershipRouter } from "~/server/api/routers/membership";
import { apiTokenRouter, validateAPIToken } from "~/server/api/routers/apitoken";
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
  base_policy: getBasePolicy,
  validateAPIToken: validateAPIToken,
});

// export type definition of API
export type AppRouter = typeof appRouter;
