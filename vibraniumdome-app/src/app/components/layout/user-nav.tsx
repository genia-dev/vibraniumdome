"use client";

import Link from "next/link";
import { signOut } from "next-auth/react";
import type { User } from "next-auth";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "~/app/components/ui/dropdown-menu";
import { Button } from "~/app/components/ui/button";
import { LogOut } from "lucide-react";

type Props = {
    user: Pick<User, "name" | "image" | "email">;
};

export function UserNav({ user }: Props) {
    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="outline" className="relative rounded">
                    <span className="text-base">{user.name}</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <div className="flex items-center justify-start gap-2 p-2">
                    <div className="flex flex-col space-y-1 leading-none">
                        {user.name && <p className="font-medium">{user.name}</p>}
                        {user.email && (
                            <p className="w-[200px] truncate text-sm text-muted-foreground">
                                {user.email}
                            </p>
                        )}
                    </div>
                </div>
                {/* <DropdownMenuSeparator /> */}
                {/* <DropdownMenuItem asChild>
                    <Link href="/profile">Profile</Link>
                </DropdownMenuItem> */}
                {/* <DropdownMenuSeparator /> */}
                <DropdownMenuItem asChild>
                    <Button
                        variant="secondary"
                        className="w-full"
                        onClick={() => {
                            void signOut();
                        }}
                    >
                        <LogOut className="mr-2 h-4 w-4" aria-hidden="true" />
                        Log Out
                    </Button>
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}