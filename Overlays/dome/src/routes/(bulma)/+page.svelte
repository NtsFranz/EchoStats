<section class="hero is-medium">
	<div class="hero-body" style="background-color: #0003;padding: 4rem 1.5rem;">
		<div class="container has-text-centered">
			<img style="float:left;width: 8em;" src="http://localhost:6724/img/ignite_logo.png" alt="" />
			<h1>DOME Ignite Overlays</h1>
			<img style="float:right;width: 8em;" src="/dome/dome_logo.webp" alt="" />
			<p class="subtitle" style="font-size: 1.2em;">
				The pages here are locally-hosted overlays built by Ignite specifically for DOME.<br />
				Using these overlays is only permitted for casts using DOME assets. If you're interested in your
				own overlay partnership with Ignite, contact NtsFranz.
			</p>
		</div>
	</div>
</section>
<div class="content" style="max-width: 60em; margin: auto;">
	<nav class="breadcrumb" aria-label="breadcrumbs">
		<ul>
			<li><a href="http://localhost:6724/">Home</a></li>
			<li class="is-active"><a href="#" aria-current="page">DOME</a></li>
		</ul>
	</nav>

	<h2>Pages hosted here:</h2>
	<div class="box">
		<ul>
			<li>
				<a href="/dome/match_setup">
					<h3>/dome/match_setup</h3>
				</a>
				Overlay configuration page.
			</li>
			<li>
				<a href="/dome/main">
					<h3>/dome/main</h3>
				</a>
				Main gameplay overlay
			</li>
			<li>
				<a href="/dome/bg">
					<h3>/dome/bg</h3>
				</a>
				Animated skybox for use with a greenscreen filter. Requires WriteAPI.
			</li>
			<li>
				<a href="/dome/waiting">
					<h3>/dome/waiting</h3>
				</a>
				Screen for before/after matches with customizable message and upcoming teams.
			</li>
			<li>
				<a href="/dome/replay_viewer">
					<h3>/dome/replay_viewer</h3>
				</a>
			</li>
			<li>
				<a href="/dome/scoreboard">
					<h3>/dome/scoreboard</h3>
				</a>
			</li>

		</ul>
	</div>
</div>

<svelte:head>
	<title>DOME Overlays</title>
</svelte:head>

<style>
	.content ul li {
		list-style: none;
		margin-top: 2em;
	}
</style>
