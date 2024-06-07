import { Minus, Pencil, Plus } from "lucide-react";
import React from "react";

const Footer = () => {
  return (
    <div className="w-full bg-[#F0F0F0] h-12 border-t-2 border-slate-400 absolute bottom-0">
      <div className="flex items-center h-9 pl-6 border-b-2 border-slate-300  ">
        <Plus className="border-2  border-slate-400 bg-white" />
        <Pencil className="border-2 border-l-0 border-r-0 text-slate-400 border-slate-400 bg-slate-200" />
        <Minus className="border-2 border-slate-400 bg-slate-200  text-slate-400" />
      </div>
      <div>
        <p className="text-sm pl-1">0 Bookmarks</p>
      </div>
    </div>
  );
};

export default Footer;
