<script lang="ts">
	import { browser } from '$app/env';
	import Chart from '$lib/Chart.svelte';
	import { read } from '$lib/dataReader';
</script>

<main class="flex flex-col items-center">
	{#if browser}
		{#await read()}
			Loading...
		{:then rows}
			<Chart {rows} />
		{:catch error}
			<pre>Oops. Something went wrong: {error.message}</pre>
		{/await}
	{/if}

	<section id="explanation" class="m-4 mb-6">
		<h2 class="text-xl font-bold">Methodology</h2>
		<p>
			My Senior Capstone project focuses on the trends of COVID-19 infections in the context of 2021&mdash;including emerging variants and vaccines.
			Daily confirmed COVID-19 cases for U.S. states has been well documented by both Johns Hopkins CSSE and the New York Times, but limited documentation
			exists for confirmed cases of prevalent COVID-19 Variants of Concern such as B.1.1.7 and P.1. To enable further research, I manually collected
			historical time-series data for these Variants of Concern grouped by U.S. states by downloading and interpreting CSVs from historical snapshots of 
			<a href="https://www.cdc.gov/coronavirus/2019-ncov/transmission/variant-cases.html">this CDC page</a> on the
			<a href="https://web.archive.org">Internet Archive</a>. You may find the raw data and Python processing code on
			<a href="https://github.com/broad-well/covid-variants-us-states">GitHub</a>.
		</p>
	</section>
</main>

