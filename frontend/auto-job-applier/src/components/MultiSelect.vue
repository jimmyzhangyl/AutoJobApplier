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

<script lang="ts">
import {
  defineComponent,
  ref,
  computed,
  onMounted,
  onBeforeUnmount,
} from "vue";
import { QuestionMarkCircleIcon } from "@heroicons/vue/24/solid";

export default defineComponent({
  name: "MultiSelect",
  props: {
    label: {
      type: String,
      required: true,
    },
    hint: {
      type: String,
      required: false,
    },
    options: {
      type: Array as () => Array<{ value: string; label: string }>,
      required: true,
    },
    modelValue: {
      type: Array as () => string[],
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
  components: {
    QuestionMarkCircleIcon,
  },
  setup(props, { emit }) {
    const showDropdown = ref(false);
    const showHint = ref(false);
    const dropdownContainer = ref<HTMLElement | null>(null);

    const selectedLabels = computed(() => {
      return props.options
        .filter((option) => props.modelValue.includes(option.value))
        .map((option) => option.label);
    });

    const toggleDropdown = () => {
      showDropdown.value = !showDropdown.value;
    };

    const selectOption = (value: string) => {
      let newValue = [...props.modelValue];
      if (value === "All Australia") {
        newValue = props.modelValue.includes("All Australia")
          ? []
          : ["All Australia"];
      } else {
        newValue = newValue.filter((v) => v !== "All Australia");
        if (newValue.includes(value)) {
          newValue = newValue.filter((v) => v !== value);
        } else {
          newValue.push(value);
        }
      }
      emit("update:modelValue", newValue);
    };

    const isSelected = (value: string) => {
      return props.modelValue.includes(value);
    };

    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownContainer.value &&
        !dropdownContainer.value.contains(event.target as Node)
      ) {
        showDropdown.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener("click", handleClickOutside);
    });

    onBeforeUnmount(() => {
      document.removeEventListener("click", handleClickOutside);
    });

    return {
      showDropdown,
      showHint,
      dropdownContainer,
      selectedLabels,
      toggleDropdown,
      selectOption,
      isSelected,
    };
  },
});
</script>

<style scoped>
/* Add necessary styles here */
</style>
