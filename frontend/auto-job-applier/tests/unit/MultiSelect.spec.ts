import { shallowMount, VueWrapper } from "@vue/test-utils";
import MultiSelect from "@/components/MultiSelect.vue";

describe("MultiSelect.vue", () => {
  it("renders the label correctly", () => {
    const label = "Test Label";
    const options = [{ value: "1", label: "Option 1" }];
    const modelValue: string[] = [];
    const wrapper = shallowMount(MultiSelect, {
      props: { label, options, modelValue },
    });
    expect(wrapper.find("label").text()).toContain(label);
  });

  it("updates the modelValue correctly when an option is selected", async () => {
    const options = [{ value: "1", label: "Option 1" }];
    const modelValue: string[] = [];
    const wrapper = shallowMount(MultiSelect, {
      props: { label: "Test Label", options, modelValue },
    });

    // Trigger the dropdown to show options
    await wrapper.find(".w-full.p-2").trigger("click");

    // Find the checkbox and simulate a click event to select the option
    const option = wrapper.find('input[type="checkbox"]');
    await option.trigger("click");

    // Check if the event was emitted and if the value was updated correctly
    expect(wrapper.emitted()["update:modelValue"]).toBeTruthy();
    expect(wrapper.emitted()["update:modelValue"][0]).toEqual([["1"]]);
  });

  it("closes the dropdown when clicking outside", async () => {
    const options = [{ value: "1", label: "Option 1" }];
    const modelValue: string[] = [];
    const wrapper = shallowMount(MultiSelect, {
      props: { label: "Test Label", options, modelValue },
    });

    // Trigger the dropdown to show options
    await wrapper.find(".w-full.p-2").trigger("click");
    expect(wrapper.vm.showDropdown).toBe(true);

    // Simulate clicking outside
    document.body.click();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.showDropdown).toBe(false);
  });

  it("displays hint and error messages", async () => {
    const label = "Test Label";
    const hint = "This is a hint";
    const error = "This is an error";
    const options = [{ value: "1", label: "Option 1" }];
    const modelValue: string[] = [];
    const wrapper = shallowMount(MultiSelect, {
      props: { label, hint, error, options, modelValue },
    });

    // Check hint visibility
    wrapper.vm.showHint = true;
    await wrapper.vm.$nextTick();
    expect(wrapper.find(".text-gray-600").text()).toBe(hint);

    // Check error visibility
    expect(wrapper.find(".text-red-600").text()).toBe(error);
  });
});
