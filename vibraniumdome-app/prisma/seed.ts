const { PrismaClient, UserRole } = require('@prisma/client');
const { genSaltSync, hashSync } = require('bcryptjs');

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