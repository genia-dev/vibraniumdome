"use client"
import Link from "next/link"
import { useState, useEffect } from "react";
import { cn } from "~/app/lib/utils"

export function MainNav({
  className,
  ...props
}: React.HTMLAttributes<HTMLElement>) {
  const [selectedPath, setSelectedPath] = useState('');

  useEffect(() => {
    setSelectedPath(window.location.pathname.toLowerCase());
  }, []);

  return (
    <nav
      className={cn("flex items-center space-x-4 lg:space-x-6", className)}
      {...props}
    >
      <Link
        href="/dashboard"
        className={`text-sm font-medium transition-colors ${selectedPath === '/dashboard' ? 'text-primary' : 'text-muted-foreground hover:text-primary'}`}
        onClick={() => setSelectedPath('/dashboard')}
      >
        Dashboard
      </Link>
      <Link
        href="/policies"
        className={`text-sm font-medium transition-colors ${selectedPath === '/policies' ? 'text-primary' : 'text-muted-foreground hover:text-primary'}`}
        onClick={() => setSelectedPath('/policies')}
      >
        Policies
      </Link>
    </nav>
  )
}
