<template>
  <div class="bg-white p-4 rounded-lg shadow-md overflow-y-scroll h-96">
    <h3 class="text-xl font-bold mb-2 sticky top-0 bg-white">{{ title }}</h3>
    <div
      v-for="job in jobs"
      :key="job.title"
      class="border-b border-gray-300 py-2 cursor-pointer"
      @click="$emit('showJobDetails', job)"
    >
      {{ job.title }}
    </div>
  </div>
</template>

<script>
export default {
  name: "ResultFrame",
  props: {
    title: String,
    jobs: Array,
  },
};
</script>
