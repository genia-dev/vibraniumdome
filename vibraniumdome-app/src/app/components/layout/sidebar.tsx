"use client"

import React, { useState } from "react";
import { SideNav } from "~/app/components/layout/side-nav";
import { NavItems } from "~/app/components/constants/side-nav";

import { cn } from "~/app/lib/utils";
import { useSidebar } from "~/app/hooks/useSidebar";
import { Separator } from "~/app/components/ui/separator";
import { Button } from "~/app/components/ui/button";
import { ChevronRight } from "lucide-react";

interface SidebarProps {
    className?: string;
}

export default function Sidebar({ className }: SidebarProps) {
    const { isOpen, toggle } = useSidebar();
    const [swith, setSwitch] = useState(false);

    const handleToggle = () => {
        setSwitch(true);
        toggle();
        setTimeout(() => setSwitch(false), 500);
    };
    return (
        <nav
            className={cn(
                `relative hidden h-screen border-r pt-16 md:block`,
                swith && "duration-500",
                isOpen ? "w-56" : "w-[78px]",
                className
            )}
        >
            <div className="space-y-4 py-4">
                <div className="px-3 py-2">
                    <div className="mt-3 space-y-1">
                        <SideNav
                            className="text-background opacity-0 transition-all duration-300 group-hover:z-50 group-hover:ml-4 group-hover:rounded group-hover:bg-foreground group-hover:p-2 group-hover:opacity-100"
                            items={NavItems}
                        />
                    </div>
                </div>
            </div>
            <div className="mt-30 absolute bottom-2 w-full space-y-2">
                <Separator />
                <div className="w-full flex justify-end">
                    <Button
                        variant="outline" size="icon"
                        onClick={handleToggle}
                        className={cn("bg-background h-10 w-10 mx-2 px-2", isOpen && "rotate-180")}
                    >
                        <ChevronRight className="h-4 w-4" />
                    </Button>
                </div>
            </div>
        </nav>
    );
}