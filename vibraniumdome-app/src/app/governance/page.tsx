import { getServerSession } from "next-auth/next";
import { authOptions } from "~/server/auth";
import { redirect } from "next/navigation";

export default async function LogsTable() {
  const session = await getServerSession(authOptions);
  if (!session) {
    redirect("/");
  }  

  const token = session?.jwt ?? ""
  const opensearchDashboardUrl = process.env.OPENSEARCH_GOVERNANCE_URL
  const iframesrc = opensearchDashboardUrl?.replace('<JWT>', token);
  return <iframe className="bg-background" src={iframesrc} height="100%" width="100%"/>
}