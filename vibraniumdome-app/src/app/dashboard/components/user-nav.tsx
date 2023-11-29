import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "~/app/components/ui/avatar"
import { Button } from "~/app/components/ui/button"
import { DropdownMenuItemLogout } from "~/app/components/dropdown-menu-item-logout"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "~/app/components/ui/dropdown-menu"
import { getServerAuthSession } from "~/server/auth";


export async function UserNav() {
  const session = await getServerAuthSession();
  const name = session?.user?.name?? ""
  const email = session?.user?.email?? ""
  const image = session?.user.image?? ""

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-8 w-8 rounded-full">
          <Avatar className="h-8 w-8">
            <AvatarImage src={image} alt={name} />
            <AvatarFallback>SC</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">{name}</p>
            <p className="text-xs leading-none text-muted-foreground">
              {email}
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
          <DropdownMenuItemLogout/>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
