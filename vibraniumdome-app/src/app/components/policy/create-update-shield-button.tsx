//@ts-nocheck
"use client"

import { useRouter } from "next/navigation";
import { Button } from "~/app/components/ui/button";

import { useAtom, useAtomValue } from 'jotai'
import { inputShieldsAtom, outputShieldsAtom, lastShieldAtom, lastShieldMetadataAtom } from "~/app/state"

//@ts-ignore
export function CreateUpdateShieldButton({ policyId, category, basePolicy }) {
  const router = useRouter();

  const [inputShields, setInputShieldsAtom] = useAtom(inputShieldsAtom)
  const [outputShields, setOutputShieldsAtom] = useAtom(outputShieldsAtom)
  const lastShield = useAtomValue(lastShieldAtom)
  const lastShieldMetadata = useAtomValue(lastShieldMetadataAtom)

  const createUpdateShieldButton = async () => {
    if (category=="input") {
      var shieldToUpdate = inputShields.find(item => item.shield.toLowerCase() === lastShield.toLowerCase())
      const currArray = inputShields.filter(item => item.shield.toLowerCase() !== lastShield.toLowerCase())

      if (shieldToUpdate) {
        shieldToUpdate.metadata = JSON.parse(lastShieldMetadata)
      } else {
        const baseShield = basePolicy.input_shields.find(item => item.full_name.toLowerCase() === lastShield.toLowerCase())

        const { full_name, type } = baseShield;
        shieldToUpdate = { shield: full_name, type: type, metadata: JSON.parse(lastShieldMetadata) }
      }
      
      setInputShieldsAtom([...currArray, shieldToUpdate]);
    } else {
      var shieldToUpdate = outputShields.find(item => item.shield.toLowerCase() === lastShield.toLowerCase())
      const currArray = outputShields.filter(item => item.shield.toLowerCase() !== lastShield.toLowerCase())

      if (shieldToUpdate) {
        shieldToUpdate.metadata = JSON.parse(lastShieldMetadata)
      } else {
        const baseShield = basePolicy.output_shields.find(item => item.full_name.toLowerCase() === lastShield.toLowerCase())

        const { full_name, type } = baseShield;
        shieldToUpdate = { shield: full_name, type: type, metadata: JSON.parse(lastShieldMetadata) }
      }
      
      setOutputShieldsAtom([...currArray, shieldToUpdate]);
    }

    router.push(policyId ? `/policy/update?policyId=${policyId}` : "/policy/create");
    router.refresh();
  }

  return <>
        <Button type="submit" onClick={createUpdateShieldButton}>
            Update Shield
        </Button>
        </>
}