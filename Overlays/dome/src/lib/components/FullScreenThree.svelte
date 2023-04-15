<script>
    import * as THREE from 'three';
    import * as SC from 'svelte-cubed';
    import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
    import {onMount} from 'svelte';
    import {MeshLine, MeshLineMaterial, MeshLineRaycast} from 'three.meshline';

    let model;
    let goalImg;
    const discLineGeo = new THREE.BufferGeometry();
    let discPositions = [];

    export let frame;
    export let camera_transform = {
        "position": {
            "X": 0,
            "Y": 0,
            "Z": 0
        },
        "rotation": {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0,
            "W": 1
        }
    };

    function loadGLTF() {
        const loader = new GLTFLoader();
        return loader.loadAsync('/dome/models/Arena1.glb');
    }

    $: if (frame) updateFrame();

    $: if (camera_transform) updateCamera();

    let camPos = [];
    let camPosFront = [];

    function updateCamera() {
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
        camPosFront = [
            -(pos[2] + forward[2] * 200),
            pos[1] + forward[1] * 200,
            pos[0] + forward[0] * 200
        ];
        camPos = [
            -pos[2],
            pos[1],
            pos[0]
        ];
    }

    function updateFrame() {
        discPositions.push(new THREE.Vector3(
            -frame['disc']['position'][2],
            frame['disc']['position'][1],
            frame['disc']['position'][0]
        ));
        if (discPositions.length > 100){
            discPositions.shift();
        }
        discLineGeo.setFromPoints(discPositions);
    }

    function drawGoalLogo() {
        let loader = new THREE.TextureLoader();
        loader.crossOrigin = "";
        let texture = loader.load(
            "https://enterthedome.com//img/dome_logo_white_square.png"
        );
        goalImg = new THREE.MeshBasicMaterial({
            opacity: .5,
            side: THREE.DoubleSide,
            map: texture,
            transparent: true,
        });
    }

    onMount(() => {
        loadGLTF().then((_model) => (model = _model));
        drawGoalLogo();
    });
</script>

<SC.Canvas alpha={true} antialias shadows>
	<SC.PerspectiveCamera position={camPos} fov={75} target={camPosFront}/>
	<!-- <SC.OrbitControls enableZoom={false} maxPolarAngle={Math.PI * 1.2} /> -->
	<SC.AmbientLight intensity={0.4}/>

	<SC.PointLight position={[25, 5, 0]} color={new THREE.Color(0x73a5d1)}/>
	<SC.PointLight position={[-25, 5, 0]} color={new THREE.Color(0xad5400)}/>

	{#if model}
		<!--		<SC.Primitive object={model.scene} rotation={[0, 0, 0]}/>-->
	{/if}

	<SC.Line
			geometry={discLineGeo}
			material={new MeshLineMaterial({lineWidth: .04})}
	/>

	{#if goalImg}
		<SC.Mesh
				geometry={new THREE.PlaneGeometry(1.5,1.5)}
				position={[36.05, 0, 0]}
				rotation={[0, -0.785398 * 2, 0]}
				material={goalImg}
		/>
		<SC.Mesh
				geometry={new THREE.PlaneGeometry(1.5,1.5)}
				position={[-36.05, 0, 0]}
				rotation={[0, 0.785398 * 2, 0]}
				material={goalImg}
		/>
	{/if}

	{#if frame}
		{#if frame['teams'][0]['players']}
			{#each frame['teams'][0]['players'] as p}
				<SC.Mesh
						geometry={new THREE.SphereGeometry()}
						position={[-p['head']['position'][2], p['head']['position'][1], p['head']['position'][0]]}
						material={new THREE.MeshBasicMaterial({ color: 0x299bff })}
						scale={[.1, .1, .1]}
				/>
			{/each}
		{/if}

		{#if frame['teams'][1]['players']}
			{#each frame['teams'][1]['players'] as p}
				<SC.Mesh
						geometry={new THREE.SphereGeometry()}
						position={[-p['head']['position'][2], p['head']['position'][1], p['head']['position'][0]]}
						material={new THREE.MeshBasicMaterial({ color: 0xff7d03 })}
						scale={[.1, .1, .1]}
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
				scale={[.1, .1, .1]}
		/>
	{/if}
</SC.Canvas>
