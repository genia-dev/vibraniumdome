"use client";

import { useSearchParams, useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/app/components/ui/card";
import { Input } from "~/app/components/ui/input";
import { Label } from "~/app/components/ui/label";
import { Tabs, TabsContent } from "~/app/components/ui/tabs";

import { Button } from "~/app/components/ui/button";

import { api } from "~/trpc/react";

import * as React from "react";

import { ShieldsDataTable } from "~/app/components/policy/shields-data-table";
import { ShieldsFilter } from "~/app/components/policy/shields-filter";
import { RedactConversation } from "~/app/components/policy/redact-conversation";
import { LowRiskThreshold } from "~/app/components/policy/low-risk-threshold";
import { HighRiskThreshold } from "~/app/components/policy/high-risk-threshold";
import { CreateShieldDialog } from "~/app/components/policy/create-policy-dialog";

import { useSelector, useDispatch } from "react-redux";
import {
  resetInputShield,
  resetOutputShield,
  addInputShield,
  addOutputShield,
} from "~/app/store/actions";

//@ts-ignore
function extractShieldsInfo(shields) {
  //@ts-ignore
  const resultArray = shields.map((shield) => {
    return { key: shield.type, value: shield.type };
  });
  return resultArray;
}

export default function CreatePolicyPage() {
  const router = useRouter();
  const dispatch = useDispatch();
  const searchParams = useSearchParams();

  const policyId = searchParams.get("policyId");

  const [policyName, setPolicyName] = React.useState();
  const [llmAppName, setLlmAppName] = React.useState();
  const [lowRiskThreshold, setLowRiskThreshold] = React.useState();
  const [highRiskThreshold, setHighRiskThreshold] = React.useState();
  const [shieldsFilter, setShieldsFilter] = React.useState();
  const [redactConversation, setRedactConversation] = React.useState();

  const inputShieldsState = useSelector((state: any) => state.inputShields);
  const outputShieldsState = useSelector((state: any) => state.outputShields);
  //@ts-ignore
  const inputShieldsData = inputShieldsState.map((item) => ({
    id: item,
    shield: item,
  }));
  //@ts-ignore
  const outputShieldsData = outputShieldsState.map((item) => ({
    id: item,
    shield: item,
  }));

  const createPolicy = api.policy.create.useMutation({
    onSuccess: () => {
      router.push("/policies");
      router.refresh();
    },
  });

  const updatePolicy = api.policy.update.useMutation({
    onSuccess: () => {
      router.push("/policies");
      router.refresh();
    },
  });

  const { data: currentPolicy, isSuccess } = api.policy.get.useQuery(
    { id: policyId },
    {
      enabled: !!policyId,
    },
  );

  React.useEffect(() => {
    if (isSuccess && currentPolicy) {
      setPolicyName(currentPolicy.name);
      setLlmAppName(currentPolicy.llmApp);
      //@ts-ignore
      setLowRiskThreshold(currentPolicy.content?.low_risk_threshold);
      //@ts-ignore
      setHighRiskThreshold(currentPolicy.content?.high_risk_threshold);
      //@ts-ignore
      setShieldsFilter(currentPolicy.content?.shields_filter);
      //@ts-ignore
      setRedactConversation(currentPolicy.content?.redact_conversation);

      //@ts-ignore
      currentPolicy?.content?.input_shields.forEach((element) => {
        dispatch(addInputShield(element.type));
      });

      //@ts-ignore
      currentPolicy?.content?.output_shields.forEach((element) => {
        dispatch(addOutputShield(element.type));
      });
    }
  }, [currentPolicy, isSuccess]);

  const defaultPolicy = api.policy.getDefaultPolicy.useQuery().data;
  if (!defaultPolicy) {
    return;
  }

  //@ts-ignore
  const inputShields = extractShieldsInfo(
    defaultPolicy?.content?.input_shields,
  );
  //@ts-ignore
  const outputShields = extractShieldsInfo(
    defaultPolicy?.content?.output_shields,
  );

  const createPolicyButton = async () => {
    //@ts-ignore
    const createShieldsMap = (shieldsArray) => {
      //@ts-ignore
      return shieldsArray.reduce((acc, shield) => {
        acc[shield.type] = shield;
        return acc;
      }, {});
    };

    //@ts-ignore
    const inputShieldsMap = createShieldsMap(
      defaultPolicy?.content?.input_shields,
    );
    //@ts-ignore
    const outputShieldsMap = createShieldsMap(
      defaultPolicy?.content?.output_shields,
    );

    const basePolicy = {
      shields_filter: shieldsFilter,
      high_risk_threshold: highRiskThreshold,
      low_risk_threshold: lowRiskThreshold,
      redact_conversation: redactConversation,
      input_shields: [],
      output_shields: [],
    };

    //@ts-ignore
    inputShieldsState.forEach((shieldKey) => {
      const shieldValue = inputShieldsMap[shieldKey];
      if (shieldValue) {
        //@ts-ignore
        basePolicy.input_shields.push(shieldValue);
      }
    });

    //@ts-ignore
    outputShieldsState.forEach((shieldKey) => {
      const shieldValue = outputShieldsMap[shieldKey];
      if (shieldValue) {
        //@ts-ignore
        basePolicy.output_shields.push(shieldValue);
      }
    });

    if (!policyId) {
      await createPolicy.mutate({
        name: policyName,
        llmAppName: llmAppName,
        // @ts-ignore
        content: JSON.stringify(basePolicy),
      });
    } else {
      await updatePolicy.mutate({
        id: policyId,
        name: policyName,
        llmAppName: llmAppName,
        // @ts-ignore
        content: JSON.stringify(basePolicy),
      });
    }

    dispatch(resetInputShield());
    dispatch(resetOutputShield());
  };

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
                  <Input
                    className="w-[180px]"
                    id="name"
                    defaultValue={policyName}
                    onChange={(e) => setPolicyName(e.target.value)}
                  />
                </div>
                <div className="pt-2 pb-4 space-y-2">
                  <Label htmlFor="llmAppName">LLM App Name:</Label>
                  <Input
                    className="w-[180px]"
                    id="llmAppName"
                    defaultValue={llmAppName}
                    onChange={(e) => setLlmAppName(e.target.value)}
                  />
                </div>
              </div>
              <div className="col-span-1 items-start">
                <div className="pt-2 pb-4 space-y-2">
                  <HighRiskThreshold
                    setState={setHighRiskThreshold}
                    defaultValue={highRiskThreshold}
                  />
                </div>
                <div className="pt-2 pb-4 space-y-2">
                  <LowRiskThreshold
                    setState={setLowRiskThreshold}
                    defaultValue={lowRiskThreshold}
                  />
                </div>
              </div>
              <div className="col-span-1 items-start">
              <div className="pt-2 pb-4 space-y-2">
                  <Label htmlFor="shields-filter">Shields Filter:</Label>
                  <ShieldsFilter
                    setState={setShieldsFilter}
                    defaultValue={shieldsFilter}
                  />
                </div>
                <div className="pt-2 pb-4 space-y-2">
                  <Label htmlFor="redact-conversation">
                    Redact conversation:
                  </Label>
                  <RedactConversation
                    setState={setRedactConversation}
                    defaultValue={redactConversation}
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
                  shields={inputShields}
                />
              </div>
            </div>
            <div className="hidden h-full flex-1 flex-col p-4 pt-0 md:flex">
              <ShieldsDataTable data={inputShieldsData} />
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
                  shields={outputShields}
                />
              </div>
            </div>
            <div className="hidden h-full flex-1 flex-col p-4 pt-0 md:flex">
              <ShieldsDataTable data={outputShieldsData} />
            </div>
          </Card>
        </div>
      </div>
      <div className="mx-6 mb-6">
        <Button type="submit" onClick={createPolicyButton}>
              {policyId ? "Update" : "Create"} Policy
        </Button>
      </div>
    </>
  );
}
