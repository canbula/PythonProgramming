import { NextRequest, NextResponse } from "next/server";
import { promises as fs } from "fs";
import path from "path";

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get("file") as File;

    if (!file || typeof file === "string") {
      return NextResponse.json(
        { message: "No file uploaded" },
        { status: 400 }
      );
    }

    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    const newImagesDir = path.join(process.cwd(), "newImages");
    const filePath = path.join(newImagesDir, file.name);

    await fs.mkdir(newImagesDir, { recursive: true });

    await fs.writeFile(filePath, buffer);

    return NextResponse.json({
      message: "Image uploaded and saved successfully!",
    });
  } catch (error) {
    console.error("Error:", error);
    return NextResponse.json(
      { message: "Error uploading file" },
      { status: 500 }
    );
  }
}
