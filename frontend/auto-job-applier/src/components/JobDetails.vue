<template>
  <div
    class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center"
    @click.self="close"
  >
    <div
      class="bg-white p-6 rounded-lg shadow-lg max-w-2xl w-full max-h-[70%] flex flex-col"
    >
      <div class="flex-grow-0">
        <h3 class="text-2xl font-bold mb-4">{{ job.title }}</h3>
        <p class="text-lg mb-2"><strong>Type:</strong> {{ job.type }}</p>
        <p class="text-lg mb-2">
          <strong>Location:</strong> {{ job.location }}
        </p>
        <p class="text-lg mb-2">
          <strong>Listing Date:</strong>
          {{ new Date(job.listedDate).toLocaleDateString() }}
        </p>
      </div>
      <div class="flex-grow overflow-y-auto mb-4">
        <strong>Description:</strong>
        <pre class="whitespace-pre-wrap">{{ job.description }}</pre>
      </div>
      <div class="flex-grow-0 flex justify-between items-center">
        <a
          :href="job.url"
          target="_blank"
          class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
          >Apply Now</a
        >
        <button
          @click="close"
          class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { Job } from "@/models/Job";

export default defineComponent({
  name: "JobDetails",
  props: {
    job: {
      type: Object as PropType<Job>,
      required: true,
    },
  },
  methods: {
    close() {
      this.$emit("close");
    },
  },
});
</script>

<style scoped>
/* Add necessary styles here */
</style>
