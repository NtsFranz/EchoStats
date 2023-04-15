<script>
	import * as THREE from 'three';
	import * as SC from 'svelte-cubed';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { onMount } from 'svelte';

	let model;

	export let frame;
	export let camera_transform = {
		position: {
			X: 0,
			Y: 0,
			Z: 0
		},
		rotation: {
			X: 0.0,
			Y: 0.0,
			Z: 0.0,
			W: 1
		}
	};

	function loadGLTF() {
		const loader = new GLTFLoader();
		return loader.loadAsync('/dome/models/Arena1.glb');
	}

	// $: if (camera_transform) updateCamera();

	let camPos = [];
	let camRot = [];
	let lookPos = [];
	let camPosBehind = [];

	function updateCamera() {
		// let pos = [
		// 	-frame['player']['vr_position'][2],
		// 	frame['player']['vr_position'][1],
		// 	frame['player']['vr_position'][0]
		// ];
		//
		// // camPos = [pos[0] * 5, pos[1] * 5, pos[2] * 5];
		//
		// lookPos = new THREE.Vector3(
		// 	pos[0] - frame['player']['vr_forward'][2],
		// 	pos[1] + frame['player']['vr_forward'][1],
		// 	pos[2] + frame['player']['vr_forward'][0]
		// );

		// just rotation copy
		// camPos = [
		// 	-frame['player']['vr_forward'][2] * 250,
		// 	Math.max(Math.min(-frame['player']['vr_forward'][1] * 250, 2000), 100),
		// 	frame['player']['vr_forward'][0] * 250
		// ];

		// method 3

		// using game api
		// let pos = frame['player']['vr_position'];
		// let forward = frame['player']['vr_forward'];

		// using writeapi
		let pos = [
			camera_transform['position']['X'],
			camera_transform['position']['Y'],
			camera_transform['position']['Z']
		];
		let rot = new THREE.Quaternion(
			camera_transform['rotation']['X'],
			camera_transform['rotation']['Y'],
			camera_transform['rotation']['Z'],
			camera_transform['rotation']['W']
		);
		let forward = new THREE.Vector3(0, 0, 1).applyQuaternion(rot).toArray();

		camPosBehind = [
			-(pos[2] - forward[2] * 200),
			Math.max(Math.min(pos[1] - forward[1] * 200, 2000), 50),
			pos[0] - forward[0] * 200
		];
		camPos = [-pos[2], pos[1], pos[0]];
	}

	onMount(() => {
		loadGLTF().then((_model) => (model = _model));
	});
</script>

<SC.Canvas alpha={true} antialias shadows>
	<SC.PerspectiveCamera position={[0,100,100]} fov={20} target={[0,0,0]} />
	<!-- <SC.OrbitControls enableZoom={false} maxPolarAngle={Math.PI * 1.2} /> -->
	<SC.AmbientLight intensity={0.2} />

	<SC.PointLight position={[25, 5, 0]} color={new THREE.Color(0x73a5d1)} />
	<SC.PointLight position={[-25, 5, 0]} color={new THREE.Color(0xad5400)} />

	{#if model}
		<SC.Primitive object={model.scene} rotation={[0, 0, 0]} />
	{/if}

	{#if frame}
		{#if frame['teams'][0]['players']}
			{#each frame['teams'][0]['players'] as p}
				<SC.Mesh
					geometry={new THREE.SphereGeometry()}
					position={[-p['head']['position'][2], p['head']['position'][1], p['head']['position'][0]]}
					material={new THREE.MeshBasicMaterial({ color: 0x299bff })}
					scale={[1, 1, 1]}
				/>
			{/each}
		{/if}

		{#if frame['teams'][1]['players']}
			{#each frame['teams'][1]['players'] as p}
				<SC.Mesh
					geometry={new THREE.SphereGeometry()}
					position={[-p['head']['position'][2], p['head']['position'][1], p['head']['position'][0]]}
					material={new THREE.MeshBasicMaterial({ color: 0xff7d03 })}
					scale={[1, 1, 1]}
				/>
			{/each}
		{/if}

		<SC.Mesh
			geometry={new THREE.SphereGeometry()}
			position={[
				-frame['disc']['position'][2],
				frame['disc']['position'][1],
				frame['disc']['position'][0]
			]}
			material={new THREE.MeshBasicMaterial({ color: 0xffffff })}
			scale={[1, 1, 1]}
		/>
	{/if}
</SC.Canvas>
