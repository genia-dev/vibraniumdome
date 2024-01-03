const { PrismaClient, UserRole } = require('@prisma/client');
const { genSaltSync, hashSync } = require('bcryptjs');

const defaultPolicy = {
  "shields_filter": "all",
  "high_risk_threshold": 0.8,
  "low_risk_threshold": 0.2,
  "redact_conversation": false,
  "input_shields": [
      {"type": "com.vibraniumdome.shield.input.transformer", "metadata": {}, "full_name": "Prompt injection transformer shield"},
      {"type": "com.vibraniumdome.shield.input.model_dos", "metadata": {"threshold": 10, "interval_sec": 60, "limit_by": "llm.user"}, "full_name": "Model denial of service shield"},
      {"type": "com.vibraniumdome.shield.input.captain", "metadata": {"model": "gpt-3.5-turbo", "model_vendor": "openai"}, "full_name": "Captain's shield"},
      {"type": "com.vibraniumdome.shield.input.semantic_similarity", "metadata": {}, "full_name": " Semantic vector similarity shield"},
      {"type": "com.vibraniumdome.shield.input.regex", "metadata": {}, "full_name": "Regex input shield"},
      {"type": "com.vibraniumdome.shield.input.prompt_safety", "metadata": {}, "full_name": "Prompt safety moderation shield"},
      {"type": "com.vibraniumdome.shield.input.sensitive_info_disc", "metadata": {}, "full_name": "PII and Sensetive information disclosure shield"},
      {"type": "com.vibraniumdome.shield.input.no_ip_in_urls", "metadata": {}, "full_name": "No IP in URLs shield"},
  ],
  "output_shields": [
      {"type": "com.vibraniumdome.shield.output.refusal.canary_token_disc", "metadata": {"canary_tokens": []}, "full_name": "Canary token disclosure shield"},
      {"type": "com.vibraniumdome.shield.output.refusal", "metadata": {}, "full_name": "Model output refusal shield"},
      {"type": "com.vibraniumdome.shield.output.sensitive_info_disc", "metadata": {}, "full_name": "PII and sensetive information disclosure shield"},
      {"type": "com.vibraniumdome.shield.output.regex", "metadata": {}, "full_name": "Regex output shield"},
      {"type": "com.vibraniumdome.shield.output.arbitrary_image", "metadata": {}, "full_name": "Arbitrary image domain URL shield"},
      {"type": "com.vibraniumdome.shield.output.whitelist_urls", "metadata": {}, "full_name": "White list domains URL shield"},
  ],
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
        seq: -99,
        name: "Default Policy",
        llmApp: "Default",
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