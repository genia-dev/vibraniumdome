"use client"

import { useAtom } from 'jotai'

import { Input } from "~/app/components/ui/input";
import { llmAppAtom } from "~/app/state"


//@ts-ignore
export function LLMAppInput({ state }) {
 const [llmApp, setLlmApp] = useAtom(llmAppAtom, state)

 return (<>
        <Input
          className="w-[180px]"
          id="name"
          value={llmApp}
          onChange={(e) => setLlmApp(e.target.value)}
        />
        </>)
}