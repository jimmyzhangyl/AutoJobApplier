<template>
  <div>
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
    <input
      type="text"
      class="w-full mt-2 p-2 border border-gray-300 rounded"
      v-model="value"
    />
    <div v-if="showHint" class="mt-2 text-sm text-gray-600">{{ hint }}</div>
    <div v-if="error" class="mt-2 text-sm text-red-600">{{ error }}</div>
  </div>
</template>

<script>
import { QuestionMarkCircleIcon } from "@heroicons/vue/24/solid";

export default {
  name: "InputBox",
  props: {
    label: String,
    hint: String,
    modelValue: String,
    error: String,
    required: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      showHint: false,
    };
  },
  components: {
    QuestionMarkCircleIcon,
  },
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
};
</script>

<style scoped>
/* Add necessary styles here */
</style>
