<script lang="ts">
	import type { Frame } from '../js/SparkConfig';

	export let frame: typeof Frame;
</script>

<div class="box">
	<div class="time">1.3 s</div>

	<div class="title">Joust Time</div>
</div>

<style type="text/scss">
	.box {
		font-size: 1.5rem;
		font-family: Arial, Helvetica, sans-serif;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;

		.title {
			font-size: 0.7rem;
			text-transform: uppercase;
		}
	}
</style>
