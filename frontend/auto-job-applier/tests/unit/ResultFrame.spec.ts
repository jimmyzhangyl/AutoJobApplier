import { shallowMount } from "@vue/test-utils";
import ResultFrame from "@/components/ResultFrame.vue";
import { Job } from "@/models/Job";

describe("ResultFrame.vue", () => {
  it("renders the title correctly", () => {
    const title = "Test Title";
    const wrapper = shallowMount(ResultFrame, {
      props: { title },
    });
    expect(wrapper.find("h3").text()).toBe(title);
  });

  it("renders the job list correctly", () => {
    const title = "Test Title";
    const jobs: Job[] = [
      {
        id: 1,
        title: "Job 1",
        location: "Location 1",
        description: "Description 1",
        type: "Full-time",
        quickApplySupported: true,
        listedDate: "2023-01-01",
        url: "http://example.com/job/1",
      },
      {
        id: 2,
        title: "Job 2",
        location: "Location 2",
        description: "Description 2",
        type: "Part-time",
        quickApplySupported: false,
        listedDate: "2023-01-01",
        url: "http://example.com/job/2",
      },
    ];
    const wrapper = shallowMount(ResultFrame, {
      props: { title, jobs },
    });

    const jobElements = wrapper.findAll(
      ".border-b.border-gray-300.py-2.cursor-pointer"
    );
    expect(jobElements.length).toBe(jobs.length);
    jobElements.forEach((jobElement, index) => {
      expect(jobElement.text()).toBe(jobs[index].title);
    });
  });

  it("emits showJobDetails event when a job is clicked", async () => {
    const title = "Test Title";
    const jobs: Job[] = [
      {
        id: 1,
        title: "Job 1",
        location: "Location 1",
        description: "Description 1",
        type: "Full-time",
        quickApplySupported: true,
        listedDate: "2023-01-01",
        url: "http://example.com/job/1",
      },
    ];
    const wrapper = shallowMount(ResultFrame, {
      props: { title, jobs },
    });

    await wrapper
      .find(".border-b.border-gray-300.py-2.cursor-pointer")
      .trigger("click");
    expect(wrapper.emitted().showJobDetails).toBeTruthy();
    expect(wrapper.emitted().showJobDetails[0]).toEqual([jobs[0]]);
  });
});
