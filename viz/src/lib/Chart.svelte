<script lang="ts">
    import { allStates, kAllVariants, read } from './dataReader';
    import type { DataRow } from './dataReader';
    import { onMount } from 'svelte';

    let container: HTMLElement;
    export let rows: DataRow[] = [];
    let selectedState = 'all';
    let selectedVariant: keyof typeof kAllVariants = 'b117';
    let uplot: any;

    function pivotData(rows: DataRow[], variant: keyof typeof kAllVariants, stateFilter?: string) {
        const sums = {};
        for (const row of rows) {
            const key = Date.parse(row.date);
            if (stateFilter != undefined && stateFilter !== 'all' && row.state !== stateFilter) continue;
            if (key in sums)
                sums[key] += parseInt(row[variant]);
            else
                sums[key] = parseInt(row[variant]);
        }
        const keys = Object.keys(sums);
        return [
            keys.map(it => parseInt(it) / 1000),
            keys.map(it => sums[it])
        ];
    }

    function chartTitle(variant: keyof typeof kAllVariants, _filter?: string): string {
        return `Cumulative Confirmed ${kAllVariants[variant]} Cases in ${_filter === undefined || _filter === 'all' ? 'the U.S.' : _filter}`;
    }

    function drawChart(uPlot, data: DataRow[], variant: keyof typeof kAllVariants, stateFilter?: string) {
        const title = chartTitle(variant, stateFilter);
        const width = Math.min(window.innerWidth - 32, 600);
        const opts = {
            title,
            id: `chart-${variant}-${stateFilter ?? 'all'}`,
            width,
            height: 400,
            series: [
                {},
                {
                    show: true,
                    spanGaps: true,
                    label: 'Cases',
                    stroke: '#B45309',
                    width: 2,
                    fill: 'rgba(180, 83, 9, 0.2)',
                }
            ]
        };
        const a = pivotData(data, variant, stateFilter);
        uplot = new uPlot(opts, a, container);
    }

    const updateChart = (rows: DataRow[], selectedVariant: keyof typeof kAllVariants, selectedState?: string) => {
        if ('uPlot' in window && rows.length > 0) {
            if (uplot !== undefined) uplot.destroy();
            drawChart(window['uPlot'], rows, selectedVariant, selectedState);
        }
    };

    onMount(() => updateChart(rows, selectedVariant, selectedState));
    $: updateChart(rows, selectedVariant, selectedState);
</script>

<figure id="chart-container" class="mx-auto flex p-4" bind:this={container}>
</figure>

<fieldset>
    <label for="state-selector">Select State:</label>
    <select name="state-selector" id="state-selector" bind:value={selectedState}>
        <option value="all">(all)</option>
        {#each allStates(rows) as state}
            <option value={state}>{state}</option>
        {/each}
    </select>
    <label for="variant-selector">Select Variant:</label>
    <select name="variant-selector" id="variant-selector" bind:value={selectedVariant}>
        {#each Object.keys(kAllVariants) as varKey}
            <option value={varKey}>{kAllVariants[varKey]}</option>
        {/each}
    </select>
</fieldset>