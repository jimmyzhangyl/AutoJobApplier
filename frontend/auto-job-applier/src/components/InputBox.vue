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

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import { QuestionMarkCircleIcon } from "@heroicons/vue/24/solid";

export default defineComponent({
  name: "InputBox",
  components: {
    QuestionMarkCircleIcon,
  },
  props: {
    label: {
      type: String,
      required: true,
    },
    hint: {
      type: String,
      required: false,
    },
    modelValue: {
      type: String,
      required: true,
    },
    error: {
      type: String,
      required: false,
    },
    required: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { emit }) {
    const showHint = ref(false);

    const value = computed({
      get: () => props.modelValue,
      set: (val: string) => {
        emit("update:modelValue", val);
      },
    });

    return {
      showHint,
      value,
    };
  },
});
</script>

<style scoped>
/* Add necessary styles here */
</style>
