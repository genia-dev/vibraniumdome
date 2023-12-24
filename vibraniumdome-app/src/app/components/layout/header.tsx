"use client"
// import { ThemeToggle } from "~/app/components/layout/theme-toggle";
import { cn } from "~/app/lib/utils";
import { MobileSidebar } from "~/app/components/layout/mobile-sidebar";
import Link from "next/link";
import { Shield } from "lucide-react";
import { UserNav } from "~/app/components/layout/user-nav";
import { signIn, useSession } from "next-auth/react";
import { Button } from "~/app/components/ui/button";
import Image from 'next/image'

export default function Header() {
    const { data: sessionData } = useSession();
    return (
        <div className="supports-backdrop-blur:bg-background/60 fixed left-0 right-0 top-0 z-20 border-b bg-background/95 backdrop-blur">
            <nav className="flex h-16 items-center justify-between px-4">
                <Link
                    href={"/dashboard"}
                    className="hidden items-center justify-between gap-2 md:flex"
                >
                    {/* <Image
                        priority
                        src="/dark-logo.svg"
                        width={100}
                        height={100}
                        alt="Logo"
                    /> */}
                    <Shield className="bg-primary h-6 w-6" />
                    <h1 className="text-lg font-semibold">Vibranium Dome</h1>
                </Link>
                <div className={cn("block md:!hidden")}>
                    <MobileSidebar />
                </div>

                <div className="flex items-center gap-2">
                    {/* <ThemeToggle /> */}
                    {sessionData?.user ? (
                        <UserNav user={sessionData.user} />
                    ) : (
                        <Button
                            variant="default"
                            className="text-sm"
                            onClick={() => {
                                void signIn();
                            }}
                        >
                            Sign In
                        </Button>
                    )}
                </div>
            </nav>
        </div>
    );
}