// @ts-nocheck
import {
  Card,
  CardContent,
} from "~/app/components/ui/card";

import { Label } from "~/app/components/ui/label";

import { api } from "~/trpc/server";

import * as React from "react";

import { ShieldsDataTable } from "~/app/components/policy/shields-data-table";
import { ShieldsFilter } from "~/app/components/policy/shields-filter";
import { RedactConversation } from "~/app/components/policy/redact-conversation";
import { LowRiskThreshold } from "~/app/components/policy/low-risk-threshold";
import { HighRiskThreshold } from "~/app/components/policy/high-risk-threshold";
import { CreateShieldDialog } from "~/app/components/policy/create-policy-dialog";
import { LLMAppInput } from "~/app/components/policy/llm-app-input";
import { PolicyInput } from "~/app/components/policy/policy-input";
import { CreateUpdatePolicyButton } from "~/app/components/policy/create-update-policy-button";

import { v4 as uuidv4 } from 'uuid';

type Props = {
  params?: {
    num?: string;
  };
  searchParams?: {
    search?: string;
  };
};

export default async function CreatePolicyPage(props: Props) {
  const policyId = props.searchParams?.policyId
  
  const basePolicy = await api.policy.getBasePolicy.query()
  
  const inputShieldsArray = basePolicy.input_shields.map(shield => {
    return { key: shield.type, value: shield.full_name };
  });
  
  const outputShieldsArray = basePolicy.output_shields.map(shield => {
    return { key: shield.type, value: shield.full_name };
  });

  const defaultPolicy = await api.policy.getDefaultPolicy.query()
  var currentPolicy = defaultPolicy
  
  if (policyId) {
    currentPolicy = await api.policy.get.query({id: policyId})
  }

  var policyName = currentPolicy?.name
  var llmApp = currentPolicy?.llmApp
  var lowRiskThreshold = currentPolicy?.content?.low_risk_threshold
  var highRiskThreshold = currentPolicy?.content?.high_risk_threshold
  var shieldsFilter = currentPolicy?.content?.shields_filter
  var redactConversation = currentPolicy?.content?.redact_conversation
  
  const input = currentPolicy?.content?.input_shields.map((shield) => {
    return {key: uuidv4(), shield: shield.full_name }
  });
  
  const output = currentPolicy?.content?.output_shields.map((shield) => {
    return {key: uuidv4(), shield: shield.full_name }
  });

  return (
    <>
      <div className="flex-1 space-y-4 p-6 pt-6">
        <h2 className="text-2xl font-semibold">Policy Settings</h2>
        <Card className="w-full">
          <CardContent className="p-6">
            <div className="grid w-full grid-cols-3 items-start gap-4">
              <div className="col-span-1 items-start">
              <div className="pt-2 pb-4 space-y-2">
                  <Label htmlFor="policyName">Policy Name:</Label>
                  <PolicyInput state={policyName} />
                </div>
                <div className="pt-2 pb-4 space-y-2">
                  <Label htmlFor="llmAppName">LLM App Name:</Label>
                  <LLMAppInput state={llmApp}/>
                </div>
              </div>
              <div className="col-span-1 items-start">
                <div className="pt-2 pb-4 space-y-2">
                  <HighRiskThreshold state={highRiskThreshold}
                  />
                </div>
                <div className="pt-2 pb-4 space-y-2">
                  <LowRiskThreshold state={lowRiskThreshold}
                  />
                </div>
              </div>
              <div className="col-span-1 items-start">
              <div className="pt-2 pb-4 space-y-2">
                  <Label htmlFor="shields-filter">Shields Filter:</Label>
                  <ShieldsFilter state={shieldsFilter}
                  />
                </div>
                <div className="pt-2 pb-4 space-y-2">
                  <Label htmlFor="redact-conversation">
                    Redact conversation:
                  </Label>
                  <RedactConversation state={redactConversation}
                  />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid w-full grid-cols-2 gap-4 p-6 pt-0">
        <div className="col-span-1 flex-1 space-y-4">
          <Card className="p-2">
            <div className="m-4 flex items-center justify-between space-y-2">
              <h2 className="text-xl font-semibold">Input Shields</h2>
              <div className="flex items-center space-x-2">
                <CreateShieldDialog
                  isinput={true}
                  title="Add Input Shield"
                  shields={inputShieldsArray}
                  policyMetadata={basePolicy?.input_shields}
                />
              </div>
            </div>
            <div className="hidden h-full flex-1 flex-col p-4 pt-0 md:flex">
              <ShieldsDataTable data={input} isinput={true}/>
            </div>
          </Card>
        </div>
        <div className="col-span-1 flex-1 space-y-4">
          <Card className="p-2">
            <div className="m-4 flex items-center justify-between space-y-2">
              <h2 className="text-xl font-semibold">Output Shields</h2>
              <div className="flex items-center space-x-2">
                <CreateShieldDialog
                  isinput={false}
                  title="Add Output Shield"
                  shields={outputShieldsArray}
                  policyMetadata={basePolicy?.output_shields}
                />
              </div>
            </div>
            <div className="hidden h-full flex-1 flex-col p-4 pt-0 md:flex">
              <ShieldsDataTable data={output} isinput={false}/>
            </div>
          </Card>
        </div>
      </div>
      <div className="mx-6 mb-6">
        <CreateUpdatePolicyButton policyId={policyId} policyMetadata={basePolicy}/>
      </div>
    </>
  );
}
