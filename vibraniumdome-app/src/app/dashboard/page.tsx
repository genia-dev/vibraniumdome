import { MainNav } from "~/app/dashboard/components/main-nav"
import { Search } from "~/app/dashboard/components/search"
import TeamSwitcher from "~/app/dashboard/components/team-switcher"
import { UserNav } from "~/app/dashboard/components/user-nav"

import { getServerSession } from "next-auth/next";
import { authOptions } from "~/server/auth";
import { redirect } from "next/navigation";

export default async function LogsTable() {
  const session = await getServerSession(authOptions);
  if (!session) {
    redirect("/");
  }  

  const token = session?.jwt ?? ""
  const opensearchDashboardUrl = process.env.OPENSEARCH_DASHBOARD_URL
  const iframesrc = opensearchDashboardUrl?.replace('<JWT>', token);
  return (
      <div className="hidden flex-col md:flex">
        <div className="border-b">
          <div className="flex h-16 items-center px-4">
            <TeamSwitcher />
            <MainNav className="mx-6" />
            <div className="ml-auto flex items-center space-x-4">
              <Search />
              <UserNav />
            </div>
          </div>
        </div>
        <iframe src={iframesrc} height="2000" width="100%"></iframe>
      </div>
  )
}