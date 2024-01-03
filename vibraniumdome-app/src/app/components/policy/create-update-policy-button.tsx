"use client"

import { useRouter } from "next/navigation";
import { api } from "~/trpc/react";

import { Button } from "~/app/components/ui/button";

import { useAtomValue } from 'jotai'

import { policyNameAtom, 
         llmAppAtom, 
         lowRiskThresholdAtom, 
         highRiskThresholdAtom, 
         shieldsFilterAtom,
         redactConversationAtom,
         inputShieldsAtom, 
         outputShieldsAtom,
        } from "~/app/state"

//@ts-ignore
export function CreateUpdatePolicyButton({ policyId, policyMetadata }) {
 const router = useRouter();

 const policyName = useAtomValue(policyNameAtom)
 const llmApp = useAtomValue(llmAppAtom)
 const lowRiskThreshold = useAtomValue(lowRiskThresholdAtom)
 const highRiskThreshold = useAtomValue(highRiskThresholdAtom)
 const shieldsFilter = useAtomValue(shieldsFilterAtom)
 const redactConversation = useAtomValue(redactConversationAtom)
 const inputShields = useAtomValue(inputShieldsAtom)
 const outputShields = useAtomValue(outputShieldsAtom)
 
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

  const createUpdatePolicyButton = async () => {

    const inputShieldsArray = inputShields.map(item => {
      const shield = policyMetadata.input_shields.find(
        (shield) => {
          return shield.full_name.toLowerCase() == item.shield.toLowerCase()
        })
      if (item['metadata'] !== undefined) {
        //@ts-ignore
        shield.metadata = JSON.parse(item.metadata)
      }
      return shield;
    });

    const outputShieldsArray = outputShields.map(item => {
      const shield = policyMetadata.output_shields.find(
        (shield) => {
          return shield.full_name.toLowerCase() === item.shield.toLowerCase()
        })
      return shield;
    });

    const basePolicy = {
      shields_filter: shieldsFilter,
      high_risk_threshold: highRiskThreshold,
      low_risk_threshold: lowRiskThreshold,
      redact_conversation: redactConversation,
      input_shields: inputShieldsArray,
      output_shields: outputShieldsArray,
    };

    if (!policyId) {
      await createPolicy.mutate({
        name: policyName,
        llmApp: llmApp,
        content: JSON.stringify(basePolicy),
      });
    } else {
      await updatePolicy.mutate({
        id: policyId,
        name: policyName,
        llmApp: llmApp,
        content: JSON.stringify(basePolicy),
      });
    }
};


 return <>
        <Button type="submit" onClick={createUpdatePolicyButton}>
            {policyId ? "Update" : "Create"} Policy
        </Button>
        </>
}