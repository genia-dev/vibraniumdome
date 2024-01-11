// @ts-nocheck
import { api } from "~/trpc/server";

import {
  Card,
  CardContent,
} from "~/app/components/ui/card";

import { Label } from "~/app/components/ui/label";

import * as React from "react";

import { CreateUpdateShieldButton } from "~/app/components/policy/create-update-shield-button";
import { ShieldsCombobox } from "~/app/components/policy/shields-combo";
import { ShieldMetadata } from "~/app/components/policy/shield-metadata";

import { useRouter } from "next/navigation";

type Props = {
  params?: {
    num?: string;
  };
  searchParams?: {
    search?: string;
  };
};

export default async function CreateShieldPage(props: Props) {
  const policyId = props.searchParams?.policyId
  const id = props.params?.id
  const category = props.searchParams?.category

  const basePolicy = await api.policy.getBasePolicy.query()
  
  const inputShieldsArray = basePolicy.input_shields.map(shield => {
    return { key: shield.type, value: shield.full_name };
  });
  
  const outputShieldsArray = basePolicy.output_shields.map(shield => {
    return { key: shield.type, value: shield.full_name };
  });
  
  return (
    <>
      <div className="flex-1 space-y-4 p-6 pt-6">
        <h2 className="text-2xl font-semibold">Shield Settings</h2>
        <Card className="w-full">
          <CardContent className="p-6">
            <div className="grid w-full grid-cols-3 items-start gap-4">
              <div className="col-span-1 items-start">
              <div className="pt-2 pb-4 space-y-2">
                  <Label htmlFor="shield-combobox">Shield:</Label>
                    <ShieldsCombobox shields={category === "input" ? inputShieldsArray : outputShieldsArray}
                                    policyMetadata={category === "input" ? basePolicy.input_shields : basePolicy.output_shields}
                                    policyId={policyId}
                    />
                </div>
                <div className="pt-2 pb-4 space-y-2">
                  <Label htmlFor="shield-metadata">Shield Metadata:</Label>
                  <ShieldMetadata/>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="mx-6 mb-6">
        <CreateUpdateShieldButton policyId={policyId} category={category} basePolicy={basePolicy}/>
      </div>
    </>
  );
}
