"use client"

import { useAtom } from 'jotai'

import { Input } from "~/app/components/ui/input";
import { policyNameAtom } from "~/app/state"

//@ts-ignore
export function PolicyInput({ state }) {
 const [policyName, setPolicyName] = useAtom(policyNameAtom)
 var value = policyName !== '' ? policyName: state
 setPolicyName(value)

 return (
        <>
        <Input
          className="w-[180px]"
          id="policy-name"
          defaultValue={value}
          onChange={(e) => setPolicyName(e.target.value)}
        />
        </>
        )
}