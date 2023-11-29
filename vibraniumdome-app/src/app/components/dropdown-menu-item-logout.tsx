/* eslint-disable @typescript-eslint/no-floating-promises */
"use client"

import * as React from "react"
import { signOut } from "next-auth/react";
import {
    DropdownMenuItem,
    DropdownMenuShortcut,
  } from "~/app/components/ui/dropdown-menu"

export function DropdownMenuItemLogout() {
    return (
        <DropdownMenuItem onClick={() => {
            signOut({ callbackUrl: "/" });
        }}      >
          Log out
          <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
        </DropdownMenuItem>
    );
}