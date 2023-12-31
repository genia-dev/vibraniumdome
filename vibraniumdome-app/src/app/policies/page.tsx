"use client";

import { api } from "~/trpc/react";
import { Button } from "~/app/components/ui/button";
import { Card, CardContent } from "~/app/components/ui/card";
import { DataTable, Policy } from "~/app/components/policy/data-table";

import * as React from "react";
import { useRouter } from "next/navigation";


function transformToPolicyArray(jsonData: any[]): Policy[] {
  const policyArray: Policy[] = [];
  for (const item of jsonData) {
    const policy: Policy = {
      id: item.id,
      seq: item.seq,
      name: item.name,
      llmAppName: item.llmApp,
      content: JSON.stringify(item.content),
      createdAt: item.createdAt,
    };
    policyArray.push(policy);
  }

  return policyArray;
}

export default function PoliciesTable() {
  const policies = api.policy.getAll.useQuery().data;
  const policiesData = policies ? transformToPolicyArray(policies) : [];

  const router = useRouter();
  const handleClick = () => {
    router.push("/policy/create");
  };

  return (
    <>
      <div className="flex-1 space-y-4 p-8">
        <div className="flex items-center justify-between space-y-2">
          <h2 className="text-2xl font-semibold">Policies</h2>
          <div className="flex items-center space-x-2">
            <Button onClick={handleClick}>Create Policy</Button>
          </div>
        </div>
        <Card>
          <CardContent className="px-4 py-0">
            <div className="hidden h-full flex-1 flex-col space-y-4 p-4 md:flex">
              <DataTable data={policiesData} />
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
