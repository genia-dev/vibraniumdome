/* eslint-disable @typescript-eslint/no-floating-promises */
"use client"

import * as React from "react"
import { signOut } from "next-auth/react";
import { Button } from "~/app/components/ui/button";

export function AuthButton() {
    return (
        <Button type="button"
            onClick={() => {
                signOut({ callbackUrl: "/" });
            }}      
        >
            Signout
        </Button>
    );
}
