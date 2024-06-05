"use client";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import Dropdown from "./dropdown";
import Image from "next/image";
import { Input } from "./ui/input";
import { useState } from "react";
import DropFile from "./dropFile";
import Collapsible from "./collapsibleComp";
import CollapsibleComp from "./collapsibleComp";

const ConnectionModal = () => {
  const [url, setUrl] = useState("ftp://");
  const [userConfigs, setUserConfigs] = useState({
    protocol: 0,
    server: "",
    port: "",
    username: "",
    password: "",
  });

  const [images, setImages] = useState([]);
  const [files, setFiles] = useState([]);

  const handleDrop = (acceptedFiles) => {
    const newImages = acceptedFiles.map((file) => URL.createObjectURL(file));
    setImages((prev) => [...prev, ...newImages]);
    setFiles((prev) => [...prev, ...acceptedFiles]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    files.forEach((file) => formData.append("file", file));

    fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className="flex">
      <Dialog>
        <DialogTrigger className="flex flex-col justify-center items-center ml-2 mt-1 hover:bg-blue-300/30 transition-all ">
          <Image src={"/world.png"} width={50} height={50} alt="world logo" />
          <p className="text-xs font-semibold">Open Connection</p>
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="font-thin -mt-3 mb-5">
              Open Connection
            </DialogTitle>
            <DialogDescription>
              <Dropdown setUserConfigs={setUserConfigs} />
              <div>
                <section className="flex items-center mt-2 w-full justify-between  ">
                  <div className="flex w-full items-center">
                    <p className="mr-2 ">Server: </p>
                    <Input
                      className="h-7 w-52 border-0 border-b-2 focus-visible:ring-0 focus-visible:ring-offset-0  border-slate-400 focus:border-blue-700"
                      onChange={(e) =>
                        setUrl((prev) => "ftp://" + e.target.value)
                      }
                    />
                  </div>
                  <div className="flex gap-2 items-center">
                    <p>Port: </p>
                    <Input
                      className="h-7  w-20 border-0 border-b-2 focus-visible:ring-0 focus-visible:ring-offset-0  border-slate-400 focus:border-blue-700"
                      type="number"
                      defaultValue={21}
                    />
                  </div>
                </section>
                <section className="flex  mt-3 gap-3">
                  <p>URL:</p>
                  <p className="text-blue-600 underline ml-3">{url}</p>
                </section>
                <section className="flex items-center justify-center mt-2">
                  <p>Username: </p>
                  <Input className="ml-3 h-7 border-0 border-b-2 focus-visible:ring-0 focus-visible:ring-offset-0  border-slate-400 focus:border-blue-700" />
                </section>
                <section className="flex items-center justify-center mt-2">
                  <p>Password: </p>
                  <Input
                    type="password"
                    className="ml-3 h-7 border-0 border-b-2 focus-visible:ring-0 focus-visible:ring-offset-0  border-slate-400 focus:border-blue-700"
                  />
                </section>
                <section className="flex ">
                  <Input type="checkbox" name="anony" className="w-3 ml-20" />
                  <label htmlFor="anony" className="ml-2 mt-[10px]">
                    Anonymous Login
                  </label>
                </section>
                <section className="flex items-center justify-center mt-2">
                  <p className="text-xs w-32">
                    SSH <br />
                    Private Key:{" "}
                  </p>
                  <Input
                    defaultValue={"None"}
                    disabled
                    className="ml-3 h-7 border-0 border-b-2 focus-visible:ring-0 focus-visible:ring-offset-0  border-slate-400 focus:border-blue-700"
                  />
                  <button disabled className="border-2 p-1 rounded-sm ml-4">
                    Choose...
                  </button>
                </section>
                <section className="flex ">
                  <Input type="checkbox" name="anony" className="w-3 ml-20" />
                  <label htmlFor="anony" className="ml-2 mt-[10px]">
                    Save Password
                  </label>
                </section>
                <section className="flex justify-end gap-5">
                  <button className="border-2 border-blue-300 p-1 rounded-sm">
                    Connect
                  </button>
                  <button className="border-2 border-slate-300 p-1 rounded-sm">
                    Cancel
                  </button>
                </section>
                <section>
                  <CollapsibleComp
                    handleDrop={handleDrop}
                    handleUpload={handleUpload}
                    images={images}
                  />
                </section>
              </div>
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ConnectionModal;
