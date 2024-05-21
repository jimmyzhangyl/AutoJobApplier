<template>
  <div ref="dropdownContainer">
    <div class="flex items-center">
      <label class="block text-gray-700">
        {{ label }}
        <span v-if="required" class="text-red-500">*</span>
      </label>
      <div
        @mouseover="showHint = true"
        @mouseleave="showHint = false"
        class="ml-2 cursor-pointer"
      >
        <QuestionMarkCircleIcon class="w-4 h-4 text-gray-500" />
      </div>
    </div>
    <div class="relative mt-2">
      <div
        @click="toggleDropdown"
        class="w-full p-2 border border-gray-300 rounded cursor-pointer bg-white"
      >
        <span>{{ selectedLabels.join(", ") || "Select options" }}</span>
        <span class="float-right">▼</span>
      </div>
      <div
        v-if="showDropdown"
        class="absolute z-10 w-full bg-white border border-gray-300 rounded mt-1"
      >
        <div
          v-for="option in options"
          :key="option.value"
          class="flex items-center p-2 hover:bg-gray-100 cursor-pointer"
          @click="selectOption(option.value)"
        >
          <input
            type="checkbox"
            class="mr-2"
            :checked="isSelected(option.value)"
          />
          <span>{{ option.label }}</span>
        </div>
      </div>
    </div>
    <div v-if="showHint" class="mt-2 text-sm text-gray-600">{{ hint }}</div>
    <div v-if="error" class="mt-2 text-sm text-red-600">{{ error }}</div>
  </div>
</template>

<script>
import { QuestionMarkCircleIcon } from "@heroicons/vue/24/solid";

export default {
  name: "MultiSelect",
  props: {
    label: String,
    hint: String,
    options: Array,
    modelValue: Array,
    error: String,
    required: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    QuestionMarkCircleIcon,
  },
  data() {
    return {
      showDropdown: false,
      showHint: false,
    };
  },
  computed: {
    selectedLabels() {
      return this.options
        .filter((option) => this.modelValue.includes(option.value))
        .map((option) => option.label);
    },
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    selectOption(value) {
      let newValue;
      if (value === "All Australia") {
        newValue = this.modelValue.includes("All Australia")
          ? []
          : ["All Australia"];
      } else {
        newValue = this.modelValue.filter((v) => v !== "All Australia");
        if (newValue.includes(value)) {
          newValue = newValue.filter((v) => v !== value);
        } else {
          newValue.push(value);
        }
      }
      this.$emit("update:modelValue", newValue);
    },
    isSelected(value) {
      return this.modelValue.includes(value);
    },
    handleClickOutside(event) {
      const dropdownContainer = this.$refs.dropdownContainer;
      if (dropdownContainer && !dropdownContainer.contains(event.target)) {
        this.showDropdown = false;
      }
    },
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>

<style scoped>
/* Add necessary styles here */
</style>
