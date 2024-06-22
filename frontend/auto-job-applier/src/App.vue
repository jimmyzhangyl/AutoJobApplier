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
        <InputBox
          label="Job listed in the last __ days"
          v-model="filters.daysListed"
          type="number"
          min="1"
          max="7"
          hint="input should be an number, min 1, max 7."
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

      <!-- FIXME: adding logic of also if the processed Jobs etc has actual value -->
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
      @close="selectedJob = undefined"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import axios from "axios";
import InputBox from "./components/InputBox.vue";
import MultiSelect from "./components/MultiSelect.vue";
import ResultFrame from "./components/ResultFrame.vue";
import JobDetails from "./components/JobDetails.vue";
import io, { Socket } from "socket.io-client";
import { Job, isJob } from "@/models/Job";
import { isJobFilter, formatJobFilter } from "@/models/JobFilter";

export default defineComponent({
  name: "App",
  components: {
    InputBox,
    MultiSelect,
    ResultFrame,
    JobDetails,
  },
  data() {
    return {
      // FIXME: rename the filters to form values
      filters: {
        titleIncludes: "",
        titleExcludes: "",
        locationIncludes: [] as string[],
        locationExcludes: "",
        typeExcludes: [] as string[],
        descriptionIncludes: "",
        descriptionExcludes: "",
        jobSource: [] as string[],
        daysListed: "",
      },

      // TODO: declear the supported type value into seprate class. can iterate its value and assign to the options
      jobLocations: [
        { value: "All Australia", label: "All Australia" },
        { value: "All Canberra ACT", label: "All Canberra ACT" },
        { value: "All Perth WA", label: "All Perth WA" },
        { value: "All Melbourne VIC", label: "All Melbourne VIC" },
        { value: "All Sydney NSW", label: "All Sydney NSW" },
      ],
      // TODO: declear the supported type value into seprate class. can iterate its value and assign to the options
      jobTypes: [
        { value: "Full time", label: "Full time" },
        { value: "Part time", label: "Part time" },
        { value: "Contract/Temp", label: "Contract/Temp" },
        { value: "Casual/Vacation", label: "Casual/Vacation" },
      ],
      // TODO: declear the supported type value into seprate class. can iterate its value and assign to the options
      jobSources: [{ value: "Seek", label: "Seek" }],
      // FIXME: integrate the error types
      errors: {
        titleIncludes: undefined as string | undefined,
        locationIncludes: undefined as string | undefined,
      },
      connectionError: undefined as string | undefined,
      error: undefined as string | undefined,

      // FIXME: integrate the result types
      results: [] as Job[],
      autoApplyJobs: [] as Job[],
      manualApplyJobs: [] as Job[],

      selectedJob: undefined as Job | undefined,

      // FIXME: integrate types
      loading: false,
      progress: {
        processed_jobs: undefined as number | undefined,
        total_jobs: undefined as number | undefined,
        remaining_jobs: undefined as number | undefined,
        estimated_time_left: undefined as number | undefined,
      },
      socket: undefined as Socket | undefined,
    };
  },
  created() {
    const apiUrl = process.env.VUE_APP_API_URL;
    if (apiUrl) {
      this.socket = io(apiUrl);
      console.log("Connecting to socket.io server...", apiUrl); // DELETE ME
      this.socket.on("job_progress", (data) => {
        this.progress = data;
      });
      this.socket.on("connect_error", (error) => {
        this.connectionError = "Connection error. Please try again later.";
        console.error("Socket connection error:", error);
      });
    } else {
      this.connectionError =
        "API URL is not defined. Please check your configuration.";
    }
  },
  methods: {
    async searchJobs() {
      this.errors.titleIncludes = !this.filters.titleIncludes
        ? "Job Title Includes is required"
        : undefined;
      this.errors.locationIncludes =
        this.filters.locationIncludes.length === 0
          ? "Job Location Includes is required"
          : undefined;

      if (this.errors.titleIncludes || this.errors.locationIncludes) {
        return;
      }

      let processedFilters = formatJobFilter(this.filters);
      if (!isJobFilter(processedFilters)) {
        this.error = "Invalid filters. Please check your input and try again.";
        return;
      }

      // TODO: optimise this huge chunck of if else nests
      try {
        this.loading = true;
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/search/`,
          processedFilters
        );

        if (response.status === 200) {
          const data = response.data;
          // Check if data is an array and if its elements have the required properties
          if (Array.isArray(data) && data.every(isJob)) {
            const jobs = data as Job[];
            if (jobs.length === 0) {
              this.error =
                "No jobs found. Please try again with different filters.";
            } else {
              this.autoApplyJobs = jobs.filter(
                (job: Job) => job.quickApplySupported
              );
              this.manualApplyJobs = jobs.filter(
                (job: Job) => !job.quickApplySupported
              );
            }
          } else {
            this.error = `Unexpected response format:"${response.data}"`;
          }
        } else {
          this.error =
            response.data || `Unexpected response status: ${response.status}`;
        }
      } catch (error: any) {
        console.error("Error fetching jobs:", error);
        this.error =
          error ||
          "An error occurred while searching for jobs. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    showJobDetails(job: Job) {
      this.selectedJob = job;
    },
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.disconnect();
    }
  },
});
</script>

<style>
/* Add global styles here if needed */
</style>
