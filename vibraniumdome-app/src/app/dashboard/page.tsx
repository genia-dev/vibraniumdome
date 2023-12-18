import { MainNav } from "~/app/dashboard/components/main-nav"
import { Search } from "~/app/dashboard/components/search"
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
            <div className="relative z-20 flex items-center text-lg font-medium">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="mr-2 h-6 w-6"
            >
              <path d="M15 6v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 0-3 3h12a3 3 0 1 0-3-3" />
            </svg>
            Vibranium
            </div>
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