<template>
  <div class="bg-white pr-0 p-4 rounded-lg shadow-md">
    <h3 class="text-xl font-bold mb-2 top-0 bg-white">{{ title }}</h3>
    <div class="overflow-y-scroll h-96">
      <div
        v-for="job in jobs"
        :key="job.id"
        class="border-b border-gray-300 py-2 cursor-pointer"
        @click="$emit('showJobDetails', job)"
      >
        {{ job.title }}
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { Job } from "@/models/Job";

export default defineComponent({
  name: "ResultFrame",
  props: {
    title: {
      type: String,
      required: true,
    },
    jobs: {
      type: Array as PropType<Job[]>,
      required: false,
    },
  },
});
</script>
