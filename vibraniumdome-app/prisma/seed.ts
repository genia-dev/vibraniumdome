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