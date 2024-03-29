import { Metadata } from "next"
import Link from "next/link"
import Image from 'next/image'
import { Shield } from "lucide-react";

import { cn } from "~/app/lib/utils"
import { buttonVariants } from "~/app/components/ui/button"
import { UserAuthForm } from "~/app/components/user-auth-form"

import { getServerSession } from "next-auth/next";
import { authOptions } from "~/server/auth";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "Authentication",
  description: "Authentication",
}

export default async function AuthenticationPage() {
  const session = await getServerSession(authOptions);
  if (session) {
    redirect("/dashboard");
  }

  return (
    <>
      <div className="container relative hidden h-[1000px] flex-col items-center justify-center md:grid lg:max-w-none lg:grid-cols-2 lg:px-0">
        <Link
          href="/"
          className={cn(
            buttonVariants({ variant: "ghost" }),
            "absolute right-4 top-4 md:right-8 md:top-8"
          )}
        >
        
        </Link>
        <div className="relative hidden h-full flex-col bg-muted p-10 text-white dark:border-r lg:flex">
          <div className="absolute inset-0 bg-zinc-900" />
          {/* <Image
            priority
            src="/dark-logo.svg"
            width={100}
            height={100}
            alt="Logo"
          /> */}
          <Shield className="bg-primary h-6 w-6" />
          <div className="relative z-20 flex items-center text-lg font-medium">
            Vibranium Dome
          </div>
          <div className="relative z-20 mt-auto">
            <blockquote className="space-y-2">
              <p className="text-lg">
              </p>
            </blockquote>
          </div>
        </div>
        <div className="lg:p-8">
          <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
            <div className="flex flex-col space-y-2 text-center">
              <h1 className="text-2xl font-semibold tracking-tight">
                Login with account
              </h1>
              <p className="text-sm text-muted-foreground">
                Enter your email below to login your account
              </p>
            </div>
            <UserAuthForm />
            <p className="px-8 text-center text-sm text-muted-foreground">
              By clicking continue, you agree to our{" "}
              <Link
                href="/terms"
                className="underline underline-offset-4 hover:text-primary"
              >
                Terms of Service
              </Link>{" "}
              and{" "}
              <Link
                href="/privacy"
                className="underline underline-offset-4 hover:text-primary"
              >
                Privacy Policy
              </Link>
              .
            </p>
          </div>
        </div>
      </div>
    </>
  )
}