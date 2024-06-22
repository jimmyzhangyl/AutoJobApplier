export interface Job {
  id: number;
  title: string;
  location: string;
  description: string;
  listedDate: string;
  type: string;
  quickApplySupported: boolean;
  url: string;
}

export function isJob(data: any): data is Job {
  return (
    typeof data === "object" &&
    data !== null &&
    typeof data.id === "number" &&
    typeof data.title === "string" &&
    typeof data.location === "string" &&
    typeof data.description === "string" &&
    typeof data.listedDate === "string" &&
    typeof data.type === "string" &&
    typeof data.quickApplySupported === "boolean" &&
    typeof data.url === "string"
  );
}
