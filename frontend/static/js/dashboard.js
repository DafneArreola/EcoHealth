import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';

// Get initial data passed from template
const { healthScore: initialHealthScore, ecoScore: initialEcoScore, modelPath } = window.INITIAL_DATA;

// Scene variables
let scene, renderer, camera;
let model, skeleton, mixer, clock;
let currentBaseAction = 'idle';
const allActions = [];

function init() {
    const container = document.getElementById('container');
    clock = new THREE.Clock();

    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xE8F5E9);
    scene.fog = new THREE.Fog(0xE8F5E9, 10, 1000);

    // Lighting
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x8d8d8d, 1);
    hemiLight.position.set(0, 20, 0);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0x4CAF50, 1);
    dirLight.position.set(3, 10, 10);
    dirLight.castShadow = true;
    scene.add(dirLight);

    // Ground
    const groundGeometry = new THREE.PlaneGeometry(100, 100);
    const groundMaterial = new THREE.MeshPhongMaterial({ 
        color: 0xC8E6C9,
        depthWrite: false 
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    // Load FBX model
    const loader = new FBXLoader();
    loader.load(modelPath, function(object) {
        model = object;
        model.scale.setScalar(0.01);
        scene.add(model);

        model.traverse(function(child) {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
                child.material = new THREE.MeshPhongMaterial({
                    color: getScoreColor(initialEcoScore),
                    emissive: getScoreColor(initialHealthScore),
                    emissiveIntensity: 0.2
                });
            }
        });

        // Setup animations
        mixer = new THREE.AnimationMixer(model);
        if (object.animations && object.animations.length) {
            object.animations.forEach((animation) => {
                const action = mixer.clipAction(animation);
                action.play();
                allActions.push(action);
            });
        }

        animate();
    });

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // Camera
    camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 1, 100);
    camera.position.set(-1, 2, 3);

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enablePan = false;
    controls.enableZoom = true;
    controls.target.set(0, 1, 0);
    controls.update();

    window.addEventListener('resize', onWindowResize);
}

function getScoreColor(score) {
    return new THREE.Color().setHSL((score / 100) * 0.3, 0.8, 0.5);
}

function updateScores(healthScore, ecoScore) {
    if (model) {
        model.traverse((object) => {
            if (object.isMesh) {
                object.material.emissive.copy(getScoreColor(healthScore));
                object.material.color.copy(getScoreColor(ecoScore));
            }
        });
    }
}

function onWindowResize() {
    const container = document.getElementById('container');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta();
    if (mixer) mixer.update(delta);
    renderer.render(scene, camera);
}

// Initialize the scene
init();

// Initial update with scores from template
updateScores(initialHealthScore, initialEcoScore);

// Handle simulation
document.querySelector('.simulation-button').addEventListener('click', async () => {
    const changeType = document.getElementById('change-type').value;
    const changeDescription = document.getElementById('change-description').value;
    
    try {
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: changeType,
                description: changeDescription
            })
        });
        
        const result = await response.json();
        
        // Update model
        updateScores(
            result.simulated_state.health.overall_score,
            result.simulated_state.environmental.overall_score
        );
        
        // Show results
        const resultsDiv = document.getElementById('simulation-results');
        resultsDiv.style.display = 'block';
        resultsDiv.innerHTML = `
            <h3>Simulation Results</h3>
            <div class="sub-scores">
                <li>Health Impact: ${result.analysis.health_impact.score_change}%</li>
                <li>Environmental Impact: ${result.analysis.environmental_impact.score_change}%</li>
                <li>Timeline: ${result.analysis.timeline}</li>
            </div>
        `;
    } catch (error) {
        console.error('Simulation failed:', error);
    }
});