import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const Menu = () => {
  return (
    <div className="ml-2 mt-2 flex gap-3">
      <DropdownMenu>
        <DropdownMenuTrigger>File</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>New Tab</DropdownMenuItem>
          <DropdownMenuItem>Open</DropdownMenuItem>
          <DropdownMenuItem>Open Recent</DropdownMenuItem>
          <DropdownMenuItem>Close Window</DropdownMenuItem>
          <DropdownMenuItem>Exit</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <DropdownMenu>
        <DropdownMenuTrigger>Edit</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Undo</DropdownMenuItem>
          <DropdownMenuItem>Redo</DropdownMenuItem>
          <DropdownMenuItem>Cut</DropdownMenuItem>
          <DropdownMenuItem>Copy</DropdownMenuItem>
          <DropdownMenuItem>Paste</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <DropdownMenu>
        <DropdownMenuTrigger>View</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Zoom In</DropdownMenuItem>
          <DropdownMenuItem>Zoom Out</DropdownMenuItem>
          <DropdownMenuItem>Full Screen</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <DropdownMenu>
        <DropdownMenuTrigger>Go</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Back</DropdownMenuItem>
          <DropdownMenuItem>Forward</DropdownMenuItem>
          <DropdownMenuItem>Reload</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <DropdownMenu>
        <DropdownMenuTrigger>Bookmark</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Add Bookmark</DropdownMenuItem>
          <DropdownMenuItem>Manage Bookmarks</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <DropdownMenu>
        <DropdownMenuTrigger>Window</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Minimize</DropdownMenuItem>
          <DropdownMenuItem>Zoom</DropdownMenuItem>
          <DropdownMenuItem>Bring All to Front</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <DropdownMenu>
        <DropdownMenuTrigger>Help</DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Help Center</DropdownMenuItem>
          <DropdownMenuItem>About</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};

export default Menu;
