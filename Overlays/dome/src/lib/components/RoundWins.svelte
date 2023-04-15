<script lang="ts">
	import type { Frame } from '../js/SparkConfig';

	export let frame: typeof Frame;
</script>

<div class="container">
	{#each { length: frame['total_round_count'] } as r}
		<div />
	{/each}
</div>

<style type="text/scss">
	.container {
		height: 0.4rem;
		margin: 0 0.5rem;
		display: flex;
		flex-direction: row;
		flex-wrap: nowrap;

		& div {
			margin: 0.1rem;
			background-color: #fff8;
			border: .1rem solid #fffa;
			flex-grow: 1;
		}

		& div.orange {
			background: rgb(170, 118, 21);
		}
		& div.blue {
			background: rgb(16, 127, 206);
		}
	}
</style>
