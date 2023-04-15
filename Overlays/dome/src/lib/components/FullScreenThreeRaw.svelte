<script lang="ts">
    import * as THREE from 'three';
    import {onDestroy, onMount} from 'svelte';
    import {GLTFLoader} from "three/examples/jsm/loaders/GLTFLoader.js";
    import {MeshLine, MeshLineMaterial} from "three.meshline";
	import { SparkWebsocket } from '$lib/js/spark_websocket';
import { dirty_components } from 'svelte/internal';
    // import {CameraTransform} from "$lib/js/CameraTransform";
    // import {Frame} from "$lib/js/Frame";

    let canvas: HTMLCanvasElement;
    let model;
    let goalImg;
    export let free_cam_fov = 85;
    
    // explosion
    let movementSpeed = .02;
    let totalObjects = 5000;
    let pointSize = .2;
    let explosions: any[] = [];
    let dirs: {}[] = [];

    let discPositions = [];
    const lineMaterial = new MeshLineMaterial({lineWidth: .02, opacity: .5});
    const discLine = new MeshLine();
    const discLineGeo = new THREE.BufferGeometry();

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

        if (camera) {
            camera.position.x = camPos[0];
            camera.position.y = camPos[1];
            camera.position.z = camPos[2];

            camera.lookAt(camPosFront[0], camPosFront[1], camPosFront[2]);

            if (free_cam_fov != camera.fov) {
                camera.fov = free_cam_fov;
                camera.updateProjectionMatrix();
            }

            manual_render();
        }
    }

    let goalFrame = 0;
    let goalExp1;

    function updateFrame() {
        if (frame['game_status'] !== 'score') {
            discPositions.push(new THREE.Vector3(
                -frame['disc']['position'][2],
                frame['disc']['position'][1],
                frame['disc']['position'][0]
            ));
            if (discPositions.length > 60) {
                discPositions.shift();
            }
            discLineGeo.setFromPoints(discPositions);
            discLine.setGeometry(discLineGeo);
        }

        if (frame['game_status'] === 'score') {
            goalFrame++;
        } else {
            goalFrame = 0;
        }

        // if (goalExp1) {
        //     goalExp1.scale.x = goalFrame / 100;
        //     goalExp1.scale.y = goalFrame / 100;
        //     goalExp1.scale.z = goalFrame / 100;
        // }
    }

    function drawGoalLogo() {
        let loader = new THREE.TextureLoader();
        loader.crossOrigin = "";
        let texture = loader.load(
            "https://enterthedome.com/img/dome_logo_white_square.png"
        );
        goalImg = new THREE.MeshBasicMaterial({
            opacity: .5,
            side: THREE.DoubleSide,
            map: texture,
            transparent: true,
        });
        let blueGoal = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.5), goalImg);
        // goalMesh.rotateX(0.785398);	// 45 deg
        blueGoal.rotateY(-0.785398 * 2); // 90 deg
        blueGoal.position.x = 36.05;
        blueGoal.position.y = 0;
        blueGoal.position.z = 0;
        scene.add(blueGoal);

        let orangeGoal = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.5), goalImg);
        // goalMesh.rotateX(0.785398);	// 45 deg
        orangeGoal.rotateY(0.785398 * 2); // 90 deg
        orangeGoal.position.x = -36.05;
        orangeGoal.position.y = 0;
        orangeGoal.position.z = 0;
        scene.add(orangeGoal);
    }

    function ExplodeAnimation(isOrange:boolean)
    {
        this.last_time = Date.now();
        this.elapsed = 0;
        this.duration = 5000;
        this.vertices = [];
        let movementMultiplier = .997;

        for (let i = 0; i < totalObjects; i ++) 
        {
            this.vertices.push(isOrange ? -36 : 36,0,0);
            let dirVector = new THREE.Vector3(
                (Math.random()-.5)*2,
                (Math.random()-.5)*2,
                Math.random()
            )
            let length = Math.sqrt(dirVector.x * dirVector.x + dirVector.y * dirVector.y + dirVector.z * dirVector.z);
            const clamp = (num, min, max) => Math.min(Math.max(num, min), max);

            dirVector.x = (dirVector.x / length) * (movementSpeed) * clamp(Math.random() * 2, 0, 1);
            dirVector.y = (dirVector.y / length) * (movementSpeed) * clamp(Math.random() * 2, 0, 1);
            dirVector.z = (dirVector.z / length) * (movementSpeed) * clamp(Math.random() * 2, 0, 1)-.0075;

            

            dirs.push(dirVector);

        }
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute( 'position', new THREE.Float32BufferAttribute( this.vertices, 3 ) );

        // Create material for particles
        // var alphaTexture = new THREE.TextureLoader().load('/dome/img/PointAlpha.jpg'); // Simple circle alpha map
        var alphaTexture = new THREE.TextureLoader().load('/dome/img/DomeLogoAlpha.jpg'); // dome logo alpha map

        const material = new THREE.PointsMaterial( { alphaMap: alphaTexture, transparent:true, alphaTest:0.5, color: isOrange?0x3da8ff:0xff5e00, size:pointSize } );
        const points = new THREE.Points( geometry, material );
        
        this.object = points;
        this.status = true;
        
        scene.add( this.object ); 
        
        let upVector = new THREE.Vector3(0,0,1);
        this.update = function(){
            let new_time = Date.now();
            let delta_time = new_time - this.last_time;
            this.elapsed += new_time - this.last_time;
            this.last_time = new_time;
            if (this.elapsed > this.duration) {
                this.status = false;
                scene.remove(this.object);
            }
            if (this.status == true){
                for (let i=0;i<this.vertices.length;i+=3) {
                    // Update Vertex Positions
                    this.vertices[i-3] += dirs[i/3].x * delta_time * Math.pow(movementMultiplier, this.elapsed);
                    this.vertices[i-1] += dirs[i/3].y * delta_time * Math.pow(movementMultiplier, this.elapsed);
                    this.vertices[i-2] += dirs[i/3].z * delta_time * Math.pow(movementMultiplier, this.elapsed);

                    let reversePoint = .5;
                    if(this.elapsed > this.duration * reversePoint ) {
                        let backwardsTime = 2 * reversePoint * (this.duration - this.elapsed);
                        this.vertices[i-3] += dirs[i/3].x * delta_time * -1*Math.pow(movementMultiplier, backwardsTime);
                        this.vertices[i-1] += dirs[i/3].y * delta_time * -1*Math.pow(movementMultiplier, backwardsTime);
                        this.vertices[i-2] += dirs[i/3].z * delta_time * -1*Math.pow(movementMultiplier, backwardsTime);
                    }
                }
                this.vertices.length = Math.round((this.duration - this.elapsed) / this.duration * totalObjects/3)*3;
                this.object.geometry.setAttribute( 'position', new THREE.Float32BufferAttribute( this.vertices, 3 ) );
            }
        }
    
    }

    const scene = new THREE.Scene();
    let camera: THREE.PerspectiveCamera;
    let renderer: THREE.WebGLRenderer;

    function manual_render() {
        
        let pCount = explosions.length;
        while(pCount--) {
            explosions[pCount].update();
        }

        renderer.render(scene, camera);
    }

    onMount(() => {
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;

        camera = new THREE.PerspectiveCamera(free_cam_fov, canvas.width / canvas.height, 0.1, 1000);
        renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            alpha: true,
            antialias: true,
            shadows: true,
        });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(canvas.width, canvas.height);

        const lineMesh = new THREE.Mesh(discLine, lineMaterial);
        scene.add(lineMesh);


        // ad
        // let loader = new THREE.TextureLoader();
        // loader.crossOrigin = "";
        // let texture = loader.load(
        //     "https://enterthedome.com/img/dome_logo_square.webp"
        // );
        // let img = new THREE.MeshBasicMaterial({
        //     opacity: .5,
        //     side: THREE.DoubleSide,
        //     map: texture,
        //     transparent: true,
        // });

        // let geom1 = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.5), img);
        // // goalMesh.rotateX(0.785398);	// 45 deg
        // geom1.rotateY(-0.785398 * 2); // 90 deg
        // geom1.rotateX(-0.6 * 2); // 90 deg
        // geom1.position.x = 36.8;
        // geom1.position.y = -6;
        // geom1.position.z = -3.4;
        // scene.add(geom1);
        // let geom2 = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.5), img);
        // // goalMesh.rotateX(0.785398);	// 45 deg
        // geom2.rotateY(-0.785398 * 2); // 90 deg
        // geom2.rotateX(-0.6 * 2); // 90 deg
        // geom2.position.x = 36.05;
        // geom2.position.y = -6.08;
        // geom2.position.z = 3.4;
        // scene.add(geom2);


        let light = new THREE.AmbientLight(0xffffff, 10);
        scene.add(light);

        // const mat = new THREE.MeshStandardMaterial({color: 0xffffff, wireframe: true, opacity: .1});
        // goalExp1 = new THREE.Mesh(new THREE.IcosahedronGeometry(8.2, 5), mat);
        // goalExp1.position.x = 36.8;
        // goalExp1.position.y = 0;
        // goalExp1.position.z = 0;
        // scene.add(goalExp1);


        // animate();

        loadGLTF().then((_model) => (model = _model));
        drawGoalLogo();
        

        sw.subscribe('goal', (data) => {
            explosions.push(new ExplodeAnimation(data['goal_color'] === 'orange'));
        });

        // ONLY FOR TESTING
        // triggers a goal explosion on blue goal any time mouse is clicked
        /*let element = document.querySelector("#element");
        element.addEventListener('click', (event: MouseEvent) => {
            explosions.push(new ExplodeAnimation(false));
        });*/
    });

    onDestroy(()=>{
        sw.close();
    });
    let sw = new SparkWebsocket();
</script>

<div style="position:absolute; top:0;left:0;width:100%;height:100%; overflow:hidden;" id="element">
	<canvas bind:this={canvas}></canvas>
</div>