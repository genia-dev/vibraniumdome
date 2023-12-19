"use client"

import { api } from "~/trpc/react";
import { Button } from "~/app/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "~/app/components/ui/dialog"
import { Input } from "~/app/components/ui/input"
import { Label } from "~/app/components/ui/label"
import { Textarea } from "~/app/components/ui/textarea"
import * as React from "react"
import { useRouter } from "next/navigation";
import { defaultPolicy } from "~/model/default-policy";

export type Policy = {
    id: string
    name: string
    llmAppName: number
    content: string
    createdAt: string
  }

export function CreatePolicyDialog() {
    const [open, setOpen] = React.useState(false);
    const router = useRouter();

    const [policyName, setPolicyName] = React.useState('');
    const [llmAppName, setLlmAppName] = React.useState('');
    const textareaRef = React.useRef(null);

    const createPolicy = api.policy.create.useMutation({
        onSuccess: () => {
          router.refresh();
        },
      });

    const saveChanges = async () => {
        setOpen(false);
        await createPolicy.mutate({name: policyName,
                                    llmAppName: llmAppName,
                                    // @ts-ignore
                                    content: textareaRef.current?.value,
                                })
    };

    return (
    <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild>
            <Button>Create Policy</Button>
        </DialogTrigger>
        
        <DialogContent className="sm:max-w-[825px]">
            <DialogHeader>
            <DialogTitle>Create policy</DialogTitle>
            <DialogDescription>
                Make policy changes. Click save when you're done.
            </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="policyName" className="text-right">
                Policy Name
                </Label>
                <Input
                id="name"
                defaultValue=""
                className="col-span-3"
                onChange={(e) => setPolicyName(e.target.value)}
                />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="llmAppName" className="text-right">
                LLM App Name
                </Label>
                <Input
                id="llmAppName"
                defaultValue=""
                className="col-span-3"
                onChange={(e) => setLlmAppName(e.target.value)}
                />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="llmAppName" className="text-right">
                Policy Content
                </Label>
                <Textarea className="col-span-3" 
                            ref={textareaRef}
                            defaultValue={JSON.stringify(defaultPolicy, null, 4)}
                            placeholder=""
                            />
            </div>
            </div>
            <DialogFooter>
                <Button type="submit" onClick={saveChanges}>Save changes</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
    )

}