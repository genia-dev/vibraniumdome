"use client";

import * as React from "react";

import { Button } from "~/app/components/ui/button";

import { useAtom, useSetAtom } from 'jotai'
import { lastShieldAtom, lastShieldMetadataAtom } from "~/app/state"

import { useRouter } from "next/navigation";

//@ts-ignore
export function CreateShield({ shieldCategory, title }) {
  const router = useRouter()
  const setLastShield = useSetAtom(lastShieldAtom)
  const setLastShieldMetadata = useSetAtom(lastShieldMetadataAtom)

  // {/* <a target="blank" href="https://docs.vibraniumdome.com/shields/introduction"><Info height={16} className="inline"/></a> */}
  const click = async () => {
    setLastShield('')
    setLastShieldMetadata('{}');
        
    router.push(`/shield/add?category=${shieldCategory}`);
    router.refresh();
  }
return (          
          <>
          <Button type="submit" onClick={click}>
            {title}
          </Button>
          </>
  );
}
