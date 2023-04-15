<script lang="ts">
	import type { Config } from '../js/SparkConfig';

	export let config: typeof Config;
	export let vertical = false;
</script>

<div class="box" class:vertical>
	{#if config && config['caster_prefs'] && config['caster_prefs']['num_casters']}
		{#each { length: config['caster_prefs']['num_casters'] } as _, i}
			{#if config['caster_prefs'][`caster_${i}_vdo`]?.length > 1}
				<div class="caster">
					<iframe src="https://vdo.ninja/?view={config['caster_prefs'][`caster_${i}_vdo`]}" />
					<p>{config['caster_prefs'][`caster_${i}_name`]}</p>
					<img src={config['caster_prefs'][`caster_${i}_img`]} alt="" />
				</div>
			{/if}
		{/each}
		{#if vertical && config['caster_prefs']['num_casters'] < 3}
			<img
				src="https://cdn.discordapp.com/attachments/1024102109282570281/1048070865339809833/dome2.png"
				class="echo_unit"
				class:tall={config['caster_prefs']['num_casters'] === 1}
				class:visible={config?.['caster_prefs']?.['show_echo_unit']}
				alt=""
			/>
		{/if}
	{/if}
</div>

<style type="text/scss">
	.box {
		display: flex;
		flex-direction: row;
		gap: 1rem;
		flex-wrap: nowrap;
		.caster {
			position: relative;
			p {
				width: 100%;
				color: #fffa;
				text-align: center;
				font-size: 2rem;
				margin: 0;
				font-family: 'Conthrax', 'Anton', sans-serif;
			}
			img {
				position: absolute;
				top: 1rem;
				width: 4rem;
				border-radius: 1rem;
				left: 1rem;
				opacity: 0;
				transition: opacity 1s;
				aspect-ratio: 1/1;
			}
			img[src] {
				opacity: 1;
			}
			iframe {
				border: 5px solid #fff3;
				border-radius: 1rem;
				width: 32.5rem;
				aspect-ratio: 16/9;
			}
		}
		&.vertical {
			flex-direction: column;
			iframe {
				width: 30rem;
			}
		}

		.echo_unit {
			width: 20rem;
			position: relative;
			top: 1rem;
			right: -5rem;
			&.tall {
                top: 3rem;
				width: 25rem;
				right: -2rem;
			}
		}
	}
</style>
