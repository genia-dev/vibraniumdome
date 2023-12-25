import {
  Card,
  CardContent,
} from "~/app/components/ui/card"
import {
  Tabs,
  TabsContent,
} from "~/app/components/ui/tabs"
import { getServerSession } from "next-auth/next";
import { authOptions } from "~/server/auth";
import { redirect } from "next/navigation";
import * as React from "react"


export default async function UsersTable() {
  const session = await getServerSession(authOptions);
  if (!session) {
    redirect("/");
  }
  
  return (
    <>
      <div className="hidden flex-col md:flex">
        <div className="flex-1 space-y-4 p-8 pt-6">
          <div className="flex items-center justify-between space-y-2">
            <h2 className="text-2xl font-semibold">Users</h2>
            <div className="flex items-center space-x-2">
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