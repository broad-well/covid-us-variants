<script lang="ts">
    import '../index.css';
</script>

<svelte:head>
    <title>COVID-19 Variant Tracker</title>
</svelte:head>

<header>
    <h2 class="text-3xl flex align-middle my-12 mx-4 font-bold">COVID-19 Variant Tracker</h2>
</header>

<slot></slot>

<footer class="text-gray-600 p-6 flex justify-between flex-col sm:flex-row">
	<div>
		Made by <a href="https://broaderator.com">Michael Peng</a>
		for <a href="https://www.notion.so/broadwell2021/Capstone-ea0edab3a4284b80a3d6c17a15b3055d">Senior Capstone</a>
    </div>
	<div>
		<a href="https://github.com/broad-well/covid-variants-us-states" class="mr-3">GitHub</a>
		&copy; 2021
    </div>
</footer>

<style lang="scss">
	:global(a) {
		@apply underline;
	}
</style>