import { api } from "~/trpc/server";
import { Button } from "~/app/components/ui/button"
import {
  Card,
  CardContent,
} from "~/app/components/ui/card"
import {
  Tabs,
  TabsContent,
} from "~/app/components/ui/tabs"
import { MainNav } from "~/app/dashboard/components/main-nav"
import { Search } from "~/app/dashboard/components/search"
import TeamSwitcher from "~/app/dashboard/components/team-switcher"
import { UserNav } from "~/app/dashboard/components/user-nav"
import { getServerSession } from "next-auth/next";
import { authOptions } from "~/server/auth";
import { redirect } from "next/navigation";
import { DataTable, Policy } from "~/app/policies/components/data-table"
import { CreatePolicyDialog } from "~/app/policies/components/create-policy-dialog"
import * as React from "react"

function transformToPolicyArray(jsonData: any[]): Policy[] {
  const policyArray: Policy[] = [];
  for (const item of jsonData) {
    const policy: Policy = {
      id: item.id,
      name: item.name,
      llmAppName: item.llmApp,
      content: JSON.stringify(item.content),
      createdAt: item.createdAt
    };
    policyArray.push(policy);
  }

  return policyArray;
}

export default async function PoliciesTable() {
  const session = await getServerSession(authOptions);
  if (!session) {
    redirect("/");
  }

  const policies = await api.policy.getAll.query();

  const policiesData = transformToPolicyArray(policies)
  
  return (
    <>
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
        <div className="flex-1 space-y-4 p-8 pt-6">
          <div className="flex items-center justify-between space-y-2">
            <h2 className="text-3xl font-bold tracking-tight">Policies</h2>
            <div className="flex items-center space-x-2">
              <CreatePolicyDialog/>
            </div>
          </div>
          <Tabs defaultValue="overview" className="space-y-4">
            <TabsContent value="overview" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-8">
                  <CardContent className="pl-2">
                  <div className="hidden h-full flex-1 flex-col space-y-8 p-8 md:flex">
                    <div className="flex items-center justify-between space-y-2">
                    </div>
                    <DataTable data={policiesData} />
                  </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </>
  )
}
