<script lang="ts">
    import type {Config, Frame} from '../js/SparkConfig';
    import JoustTime from './JoustTime.svelte';
    import RoundWins from './RoundWins.svelte';
    import ScoreView from './ScoreView.svelte';

    export let frame: typeof Frame | null = null;
    export let config: typeof Config | null = null;
</script>

{#if frame}
	<div class="main-box">
		<div class="team orange">
			<div class="default-view">
				<p class="team-name">{frame['teams'][1]['team']}</p>
				<div class="score orange">
					{frame['orange_points']}
				</div>
				<!--				<div class="joust score orange"><JoustTime {frame} /></div>-->
			</div>
		</div>
<!--		<div>-->
<!--			<img src="/dome_logo_square.webp" style="width:3rem;margin: 0 .3rem;"/>-->
<!--		</div>-->
		<div class="team blue">
			<div class="default-view">
				<div class="score blue">{frame['blue_points']}</div>
				<p class="team-name">{frame['teams'][0]['team']}</p>
			</div>
		</div>

		<div class="score-view">
			<ScoreView {frame}/>
		</div>

    
		<div class="clock-box">
			<div class="clock">{frame['game_clock_display'].substring(0, 5)}</div>
						<div class="round-wins"><RoundWins {frame} /></div>
		</div>
  
	</div>
{/if}

<style type="text/scss">
  :root {
    --primary: #6f61e9;
    --secondary: #5ea5ec;
    --primary-dark: #4255e6;
    --secondary-dark: #3a75e5;
    --text: #c5c8d4;
  }

  @font-face {
    font-family: 'Conthrax';
    src: url('$lib/fonts/conthrax-sb.ttf') format('truetype');
  }

  .main-box {
    //background: linear-gradient(var(--primary), var(--primary-dark));
    // background: linear-gradient(#fffd, #aaad);
    color: #fff;
    -webkit-text-stroke: .1px white;
    border-radius: 1rem;
    height: 4rem;
    position: relative;
    display: flex;
    flex-wrap: nowrap;
    width: 40rem;
    //box-shadow: 0 1rem 1rem #000a;
    //opacity: .9;
    overflow: hidden;
  }

  .clock-box {
    //background: linear-gradient(var(--secondary-dark), var(--secondary));
    background: linear-gradient(var(--primary), var(--primary-dark));
    height: 100%;
    flex-grow: 0;
    width: 10rem;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text);
    font-size: 2rem;
    font-family: 'Conthrax', 'Anton', sans-serif;
    text-shadow: 0 0 .5rem #0008;

    .round-wins {
      position: absolute;
      bottom: 0.3rem;
      width: 100%;
      height: 0.5rem;
    }
  }

  .team {
    flex-grow: 1;
    flex-shrink: 1;
    flex-basis: 0;
    position: relative;
  }

  .team > div {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  .default-view {
    display: flex;

    .score {
      height: 4rem;
      flex-grow: 0;
      flex-shrink: 0;
      flex-basis: 5rem;
      display: flex;
      align-items: center;
      justify-content: center;
      
      font-family: 'Conthrax', 'Anton', sans-serif;
      color: var(--text);
      font-size: 2.5rem;
      text-shadow: 0 0 .5rem #0008;

      &.orange {
        background: linear-gradient(orange, rgb(143, 65, 17));
        // background: rgb(143, 65, 17);
        
        border-radius: .5rem 0 0 .5rem;
      }

      &.blue {
        background: linear-gradient(rgb(0, 149, 255), rgb(22, 85, 119));
        // background: rgb(22, 85, 119);

        border-radius: 0 .5rem .5rem 0;
      }
    }

    .team-name {
      flex-grow: 1;
      flex-shrink: 1;
      display: flex;
      align-items: center;
      text-align: center;
      justify-content: center;
      //color: var(--text);
      font-size: 1.6rem;
      padding: 0 1rem;
      font-family: 'Conthrax', 'Anton', sans-serif;
    }

    .joust {
      position: absolute;
      width: 5rem;
    }
  }

  .score-view {
    position: absolute;
    top: 0;
    left: 0;
    width: 30rem;
    height: 100%;
  }
</style>
