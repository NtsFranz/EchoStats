<script lang="ts">
	import type { Config } from '../js/SparkConfig';

	export let config: typeof Config;
</script>

<div class="box">
	<div>
		<img src={config?.['teams'][1]['team_logo']} />
		<p>{config?.['teams'][1]['team_name']}</p>
	</div>
	<div class="vs">
		<hr />
		<p>vs</p>
		<hr />
	</div>
	<div>
		<img src={config?.['teams'][0]['team_logo']} />
		<p>{config?.['teams'][0]['team_name']}</p>
	</div>
</div>

<style type="text/scss">
	.box {
		background-color: #fff1;
		border-radius: 1rem;
		border: 1px solid #fff3;
		color: white;
		font-family: 'Conthrax', 'Anton', sans-serif;
		transform: scale(0.7);
		& > div {
			justify-content: center;
			align-items: center;
			gap: 1rem;
			padding: 1rem;
			display: flex;
			flex-wrap: nowrap;
			flex-direction: row;
		}
		p {
			min-width: 20rem;
			text-align: center;
			font-size: 1.8rem;
		}
		.vs {
			font-family: sans-serif;
			font-weight: 900;
			display: flex;
			flex-direction: row;
			margin: -3rem 0;
			hr {
				width: 8rem;
				opacity: 0.3;
			}
			p {
				min-width: 1rem;
			}
		}
		img[src] {
			opacity: 1;
		}
		img {
			opacity: 0;
			width: 10rem;
			aspect-ratio: 1/1;
			transition: opacity 1s;
		}
	}
</style>
