export interface JobFilter {
  titleIncludes: string[];
  titleExcludes: string[];
  locationIncludes: string[];
  locationExcludes: string[];
  typeExcludes: string[];
  descriptionIncludes: string[];
  descriptionExcludes: string[];
  jobSource: string[];
  daysListed: number;
}

export function isJobFilter(data: any): data is JobFilter {
  const isStringArray = (arr: any): arr is string[] =>
    Array.isArray(arr) && arr.every((item) => typeof item === "string");

  return (
    typeof data === "object" &&
    data !== null &&
    isStringArray(data.titleIncludes) &&
    isStringArray(data.titleExcludes) &&
    isStringArray(data.locationIncludes) &&
    isStringArray(data.locationExcludes) &&
    isStringArray(data.typeExcludes) &&
    isStringArray(data.descriptionIncludes) &&
    isStringArray(data.descriptionExcludes) &&
    isStringArray(data.jobSource) &&
    typeof data.daysListed === "number"
  );
}

export function formatJobFilter(data: any): JobFilter {
  return {
    titleIncludes:
      data.titleIncludes
        .split(",")
        .map((item: string) => item.trim())
        .filter((item: string) => item) || [],
    titleExcludes:
      data.titleExcludes
        .split(",")
        .map((item: string) => item.trim())
        .filter((item: string) => item) || [],
    locationIncludes: data.locationIncludes || [],
    locationExcludes:
      data.locationExcludes
        .split(",")
        .map((item: string) => item.trim())
        .filter((item: string) => item) || [],
    typeExcludes: data.typeExcludes || [],
    descriptionIncludes:
      data.descriptionIncludes
        .split(",")
        .map((item: string) => item.trim())
        .filter((item: string) => item) || [],
    descriptionExcludes:
      data.descriptionExcludes
        .split(",")
        .map((item: string) => item.trim())
        .filter((item: string) => item) || [],
    jobSource: data.jobSource || [],
    daysListed: data.daysListed ? parseInt(data.daysListed, 10) : 1,
  };
}
