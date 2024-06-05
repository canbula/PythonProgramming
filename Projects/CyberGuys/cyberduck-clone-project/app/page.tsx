"use client";
import Footer from "@/components/footer";
import Header from "@/components/header";
import { SubHeader } from "@/components/subheader";
import { Button } from "@/components/ui/button";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";

export default function Home() {
  const [files, setFiles] = useState([]);
  const [selected, setSelected] = useState(150);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/getfiles");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setFiles(data.files); // Gelen dosyaları state'e kaydet
      } catch (error) {
        console.error("Error fetching files:", error);
      }
    };

    fetchFiles();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/download", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: selected }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = files[selected];
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      console.error("Error downloading file:", error);
    }
  };

  const handleDelete = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/delete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: selected }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const result = await response.json();
      if (result.success) {
        // Dosya başarıyla silindiyse dosyaları yeniden yükle
        setFiles(files.filter((_, index) => index !== selected));
        setSelected(null);
      } else {
        console.error("Error deleting file:", result.error);
      }
    } catch (error) {
      console.error("Error deleting file:", error);
    }
  };

  return (
    <div className="relative h-[95vh]">
      <Header />
      <SubHeader />
      <div className="ml-5 mt-5">
        <table className="">
          <thead>
            <tr>
              <th className="">id</th>
              <th className=" flex justify-start ml-5">File Name</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file, index) => (
              <tr
                key={index}
                className={`hover:bg-slate-200 cursor-pointer ${
                  selected === index ? "bg-slate-200" : ""
                }`}
                onClick={() => {
                  setSelected(index);
                  console.log(index);
                }}
              >
                <td className="">{index}</td>
                <td className="pl-5">{file}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div>
          <Button className="mt-5 " onClick={handleSubmit}>
            Request File
          </Button>
          <Button className="ml-5" variant="destructive" onClick={handleDelete}>
            Delete
          </Button>
        </div>
      </div>
      <Footer />
    </div>
  );
}
