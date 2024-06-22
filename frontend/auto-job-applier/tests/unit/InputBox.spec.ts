import { shallowMount } from "@vue/test-utils";
import InputBox from "@/components/InputBox.vue";

describe("InputBox.vue", () => {
  it("renders the label correctly", () => {
    const label = "Test Label";
    const wrapper = shallowMount(InputBox, {
      props: { label, modelValue: "" },
    });
    expect(wrapper.find("label").text()).toContain(label);
  });

  it("emits an update event with the correct value", async () => {
    const wrapper = shallowMount(InputBox, {
      props: { label: "Test Label", modelValue: "" },
    });
    const input = wrapper.find("input");
    await input.setValue("New Value");
    expect(wrapper.emitted()["update:modelValue"][0]).toEqual(["New Value"]);
  });
});
