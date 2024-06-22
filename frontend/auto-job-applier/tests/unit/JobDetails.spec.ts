import { shallowMount } from "@vue/test-utils";
import JobDetails from "@/components/JobDetails.vue";
import { Job } from "@/models/Job";

describe("JobDetails.vue", () => {
  it("renders job details correctly", () => {
    const job: Job = {
      id: 1,
      title: "Test Job",
      location: "Test Location",
      description: "Test Description",
      type: "Full-time",
      quickApplySupported: true,
      listedDate: "2023-01-01",
      url: "http://example.com/job/1",
    };
    const wrapper = shallowMount(JobDetails, {
      props: { job },
    });
    expect(wrapper.find("h3").text()).toBe(job.title);
    expect(wrapper.find("p:nth-of-type(1)").text()).toContain(
      `Type: ${job.type}`
    );
    expect(wrapper.find("p:nth-of-type(2)").text()).toContain(
      `Location: ${job.location}`
    );
    expect(wrapper.find("p:nth-of-type(3)").text()).toContain(
      `Listing Date: ${new Date(job.listedDate).toLocaleDateString()}`
    );
    expect(wrapper.find("pre").text()).toBe(job.description);
  });

  it("emits close event when close button is clicked", async () => {
    const job: Job = {
      id: 1,
      title: "Test Job",
      location: "Test Location",
      description: "Test Description",
      type: "Full-time",
      quickApplySupported: true,
      listedDate: "2023-01-01",
      url: "http://example.com/job/1",
    };
    const wrapper = shallowMount(JobDetails, {
      props: { job },
    });
    await wrapper.find("button").trigger("click");
    expect(wrapper.emitted().close).toBeTruthy();
  });
});
