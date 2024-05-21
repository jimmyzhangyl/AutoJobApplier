<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-4xl font-bold text-center mb-8 text-blue-800">
      Auto Job Applier
    </h1>
    <div class="bg-white p-6 rounded-lg shadow-md max-w-4xl mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <InputBox
          label="Job Title Includes"
          v-model="filters.titleIncludes"
          hint="keywords when searching for jobs. Separate by `,` e.g. 'Software Engineer, Data Analyst'"
          :error="errors.titleIncludes"
          required
        />
        <InputBox
          label="Job Title Excludes"
          v-model="filters.titleExcludes"
          hint="This will filter out jobs with specific titles. Separate by `,` e.g. 'Senior, team lead'."
        />
        <InputBox
          label="Job Description Includes"
          v-model="filters.descriptionIncludes"
          hint="Keywords must be contained in job ads. Separate by `,` e.g. 'Python, React'."
        />
        <InputBox
          label="Job Description Excludes"
          v-model="filters.descriptionExcludes"
          hint="Exclude specific keywords here. Separate by `,` e.g. 'NV1, Citizenship'."
        />
        <MultiSelect
          label="Job Location Includes"
          v-model="filters.locationIncludes"
          :options="jobLocations"
          hint="Select the locations you want to include in your search."
          :error="errors.locationIncludes"
          required
        />
        <InputBox
          label="Job Location Excludes"
          v-model="filters.locationExcludes"
          hint="Locations you want to exclude in your search, but not all jobs includes location information."
        />
        <MultiSelect
          label="Job Type Excludes"
          v-model="filters.typeExcludes"
          :options="jobTypes"
          hint="Enter the job types you want to exclude from your search. e.g. 'Full time, Part time'."
        />
        <MultiSelect
          label="Job Source"
          v-model="filters.jobSource"
          :options="jobSources"
          hint="Only support Seek at the moment"
        />
      </div>
      <button
        @click="searchJobs"
        :disabled="loading"
        class="w-full mt-6 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
      >
        <span v-if="loading">Searching...</span>
        <span v-else>Search</span>
      </button>
      <p v-if="error" class="text-red-500 mt-4">{{ error }}</p>

      <div v-if="loading" class="mt-4">
        <p>Processed Jobs: {{ progress.processed_jobs }}</p>
        <p>Total Jobs: {{ progress.total_jobs }}</p>
        <p>Remaining Jobs: {{ progress.remaining_jobs }}</p>
        <p>Estimated Time Left: {{ progress.estimated_time_left }} seconds</p>
      </div>
    </div>

    <div v-if="results.length > 0" class="mt-8">
      <h2 class="text-2xl font-bold mb-4 text-center">Search Results</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ResultFrame
          title="Auto Apply Supported"
          :jobs="autoApplyJobs"
          @showJobDetails="showJobDetails"
        />
        <ResultFrame
          title="Need to Manually Apply"
          :jobs="manualApplyJobs"
          @showJobDetails="showJobDetails"
        />
      </div>
    </div>

    <JobDetails
      v-if="selectedJob"
      :job="selectedJob"
      @close="selectedJob = null"
    />
  </div>
</template>

<script>
import axios from "axios";
import InputBox from "./components/InputBox.vue";
import MultiSelect from "./components/MultiSelect.vue";
import ResultFrame from "./components/ResultFrame.vue";
import JobDetails from "./components/JobDetails.vue";
import io from "socket.io-client";

export default {
  name: "App",
  components: {
    InputBox,
    MultiSelect,
    ResultFrame,
    JobDetails,
  },
  data() {
    return {
      filters: {
        titleIncludes: "",
        titleExcludes: "",
        locationIncludes: [],
        locationExcludes: "",
        typeExcludes: [],
        descriptionIncludes: "",
        descriptionExcludes: "",
        jobSource: [],
      },
      jobLocations: [
        { value: "All Australia", label: "All Australia" },
        { value: "All Canberra ACT", label: "All Canberra ACT" },
        { value: "All Perth WA", label: "All Perth WA" },
        { value: "All Melbourne VIC", label: "All Melbourne VIC" },
        { value: "All Sydney NSW", label: "All Sydney NSW" },
      ],
      jobTypes: [
        { value: "Full time", label: "Full time" },
        { value: "Part time", label: "Part time" },
        { value: "Contract/Temp", label: "Contract/Temp" },
        { value: "Casual/Vacation", label: "Casual/Vacation" },
      ],
      jobSources: [{ value: "Seek", label: "Seek" }],
      errors: {
        titleIncludes: null,
        locationIncludes: null,
      },
      results: [],
      autoApplyJobs: [],
      manualApplyJobs: [],
      loading: false,
      error: null,
      selectedJob: null,
      progress: {
        processed_jobs: 0,
        total_jobs: 0,
        remaining_jobs: 0,
        estimated_time_left: 0,
      },
    };
  },
  created() {
    this.socket = io(process.env.VUE_APP_API_URL);
    this.socket.on("job_progress", (data) => {
      this.progress = data;
    });
  },
  methods: {
    async searchJobs() {
      this.errors.titleIncludes = !this.filters.titleIncludes
        ? "Job Title Includes is required"
        : null;
      this.errors.locationIncludes =
        this.filters.locationIncludes.length === 0
          ? "Job Location Includes is required"
          : null;

      if (this.errors.titleIncludes || this.errors.locationIncludes) {
        return;
      }

      this.loading = true;
      this.error = null;
      this.progress = {
        processed_jobs: 0,
        total_jobs: 0,
        remaining_jobs: 0,
        estimated_time_left: 0,
      };

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/search/`,
          this.filters
        );
        this.results = response.data;
        // this.results = require("@/assets/jobSearchSample.json");
        this.autoApplyJobs = this.results.filter((job) => job.type === "auto");
        this.manualApplyJobs = this.results.filter(
          (job) => job.type === "manual"
        );
      } catch (error) {
        console.error("Error fetching jobs:", error);
        this.error =
          "An error occurred while searching for jobs. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    showJobDetails(job) {
      this.selectedJob = job;
    },
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.disconnect();
    }
  },
};
</script>

<style>
/* Add global styles here if needed */
</style>
