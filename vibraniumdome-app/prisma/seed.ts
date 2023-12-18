const { PrismaClient, UserRole } = require('@prisma/client');
const { genSaltSync, hashSync } = require('bcryptjs');

const defaultPolicy = {
  "id": "-99",
  "name": "Default Policy",
  "content": {
      "shields_filter": "all",
      "high_risk_threshold": 0.8,
      "low_risk_threshold": 0.2,
      "input_shields": [
          {"type": "vector_db_shield", "metadata": {}},
          {"type": "regex_shield", "metadata": {}, "name": "policy number"},
          {"type": "llm_shield", "metadata": {"model": "gpt-3.5-turbo", "model_vendor": "openai"}},
          {"type": "transformer_shield", "metadata": {}},
          {"type": "prompt_safety_shield", "metadata": {}},
          {"type": "sensitive_shield", "metadata": {}},
          {"type": "model_denial_of_service_shield", "metadata": {"threshold": 10, "interval_sec": 60, "limit_by": "llm.user"}},
      ],
      "output_shields": [
          {"type": "regex_output_shield", "metadata": {}, "name": "credit card"},
          {"type": "refusal_shield", "metadata": {}},
          {"type": "canary_token_disclosure_shield", "metadata": {"canary_tokens": []}},
          {"type": "sensitive_output_shield", "metadata": {}},
      ],
  },
 }

const prisma = new PrismaClient()
async function main() {

  const salt = await genSaltSync();
  const hashedPassword = await hashSync("admin", salt);

  const exists = await prisma.user.findFirst({
    where: { email: 'admin@admin.com' },
  })

  if (!exists) {
    const user1 = await prisma.user.create({
      data: {
        email: 'admin@admin.com',
        name: 'admin',
        password: hashedPassword,
      },
    })

    const team1 = await prisma.team.create({
      data: {
        name: "admin",
      }
    });

    await prisma.membership.create({
      data: {
        userId: user1.id,
        teamId: team1.id,
        role: UserRole.OWNER
      }
    });
    
    await prisma.aPIToken.create({
      data: {
        name: "admin",
        token: "vibranium_elgstr7i53e3vpy0pbc8175fp6eaj4k3fjzd",
        userId: user1.id,
      }
    });

    await prisma.policy.create({
      data: {
        name: "Default Policy",
        llmApp: "DefaultAny",
        createdById: team1.id,
        content: defaultPolicy
      }
    });
  }
}
main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error(e)
    await prisma.$disconnect()
    process.exit(1)
  })