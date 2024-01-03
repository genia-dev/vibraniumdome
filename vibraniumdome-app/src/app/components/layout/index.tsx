"use client"

import React from "react";
import Header from "~/app/components/layout/header";
import Sidebar from "~/app/components/layout/sidebar";
import { SessionProvider, useSession } from "next-auth/react";
import { ThemeProvider } from "next-themes";
import { store } from '~/app/store/store';


export const Layout = ({ children }: { children: React.ReactNode }) => {
    return (
        <>
            <SessionProvider>
                <AuthCheck children={children}/>
            </SessionProvider>
        </>
    );
};

const AuthCheck = ({ children }: { children: React.ReactNode }) => {
 const { data: session, status } = useSession();
 return !session ? (
   <>
   {children}
   </>
 ) : (
  <>
     <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
     <Header />
     <div className="flex h-screen border-collapse overflow-hidden">
         <Sidebar />
         <main className="flex-1 overflow-y-auto overflow-x-hidden pt-16 bg-secondary/10 pb-1">
             {children}
         </main>
     </div>
     </ThemeProvider>
  </>
 );
};