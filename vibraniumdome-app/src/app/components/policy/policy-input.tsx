"use client"

import { useAtom } from 'jotai'

import { Input } from "~/app/components/ui/input";
import { policyNameAtom } from "~/app/state"

//@ts-ignore
export function PolicyInput({ state }) {
 const [policyName, setPolicyName] = useAtom(policyNameAtom, state)

 return (
        <>
        <Input
          className="w-[180px]"
          id="name"
          value={policyName}
          onChange={(e) => setPolicyName(e.target.value)}
        />
        </>
        )
}