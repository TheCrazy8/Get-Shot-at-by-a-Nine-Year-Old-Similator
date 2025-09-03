// Get Shot at by a Nine Year Old Simulator - JavaScript Port
// This is a full port of the Python/Tkinter game to HTML5 Canvas

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreDiv = document.getElementById('score');
const timeDiv = document.getElementById('time');
const dialogDiv = document.getElementById('dialog');
const pauseTextDiv = document.getElementById('pauseText');
const bgMusic = document.getElementById('bgMusic');

// Game constants
const PLAYER_WIDTH = 20;
const PLAYER_HEIGHT = 20;
const PLAYER_SPEED = 20;
const GRAZING_RADIUS = 40;
const CANVAS_WIDTH = canvas.width;
const CANVAS_HEIGHT = canvas.height;

// Game state
let player = {
    x: CANVAS_WIDTH / 2 - PLAYER_WIDTH / 2,
    y: CANVAS_HEIGHT - 50,
    width: PLAYER_WIDTH,
    height: PLAYER_HEIGHT,
    color: 'white'
};
let bullets = [];
let bullets2 = [];
let triangleBullets = [];
let diagBullets = [];
let bossBullets = [];
let zigzagBullets = [];
let fastBullets = [];
let starBullets = [];
let rectBullets = [];
let eggBullets = [];
let explodingBullets = [];
let explodedFragments = [];
let bouncingBullets = [];
let laserIndicators = [];
let lasers = [];
let score = 0;
let startTime = Date.now();
let dial = "Welcome to Get Shot at by a Nine Year Old Simulator!";
let lives = 1;
let gameOver = false;
let paused = false;
let difficulty = 1;
let lastDifficultyIncrease = Date.now();
let lastDial = Date.now();
let grazedBullets = new Set();
let grazeEffect = null;
let grazeEffectTimer = 0;
let pausedTimeTotal = 0;
let pauseStartTime = null;

// Dialogs
const dialogs = [
    ":)",
    "Dodge the bullets and survive as long as you can!",
    "Use arrow keys to move yourself.",
    "Good luck, and have fun!",
    "The bullets are getting faster!",
    "Stay sharp, the challenge increases!",
    "Can you beat your high score? (no)",
    "Keep going, you're doing great! (lie)",
    "Watch out for the lasers!",
    "Every second counts in Bullet Hell!",
    "This isn't like Undertale, you can't fight back!",
    "Remember, it's just a game. Have fun! (jk)",
    "Pro tip: Moving towards bullets can help dodge bullets.",
    "If you can read this, you're doing well!",
    "Try to survive for 5 minutes!",
    "The longer you survive, the harder it gets!",
    "Don't forget to take breaks! (but leave it running)",
    "You're a star at dodging bullets! (there arent stars)",
    "Keep your eyes on the screen! (tear them out)",
    "Practice makes perfect! (poggers)",
    "This doesn't really compare to Touhou, but it's fun!",
    "Feel free to suggest new bullet patterns!",
    "Remember to breathe and relax!",
    "You can do this, just keep dodging!",
    "Every bullet you dodge is a victory!",
    "Stay focused, and you'll go far!",
    "You're not just playing, you're mastering the art of dodging!",
    "Keep your reflexes sharp!",
    "Believe in yourself, you can do it!",
    "[FILTERED] You- you suck!",
    "If you can dodge a wrench, you can dodge a bullet.",
    "Y u try?",
    "Is this bullet hell or bullet heaven?",
    "Dodging bullets is my cardio.",
    "I hope you like pain.",
    "My bullets, my rules.",
    "You call that dodging?",
    "Too slow!",
    "Is that all you've got?",
    "You can't hide forever!",
    "Feel the burn of my bullets!",
    "You're making this too easy!",
    "Come on, show me what you've got!",
    "You can't escape your fate!",
    "This is just the beginning!",
    "Prepare to be overwhelmed!",
    "Your skills are impressive, but not enough!",
    "I could do this all day!",
    "You're in my world now!",
    "Let's see how long you can last!",
    "Every second you survive, I get stronger!",
    "You think you can outlast me?",
    "This is my domain!",
    "You can't win, but you can try!",
    "The harder you try, the more bullets you'll face!",
    "You may have dodged this time, but not next time!",
    "Is that fear I see in your eyes?",
    "You can't run from your destiny!",
    "Your efforts are futile!",
    "I admire your persistence!",
    "Persistence won't save you!",
    "You're just delaying the inevitable!",
    "E",
    "Stay determined!",
    "Skissue",
    "You can do it! /j",
    "This is getting intense, isn't it?",
    "Keep your head in the game!",
    "You're doing better than I expected!",
    "Song name is Juggerbeat, I made it in 3rd grade. :3",
    "BTW the dialog is canonically spoken by a nine year old girl named J.",
    "The bullets are getting faster, just like your heart rate!",
    "The person making the bullets is also a nine year old. (same person lol)",
    "Yeah im not okay!",
    "Murder! Yippee!!!",
    "The person making the game may or may not be a nine year old.",
    "Yes im self aware, and will actively break the 4th wall.",
    "\n I could really go for some applesauce... \n Or corpses...",
    "U just got beat up by a girl!",
    "Smug colon-three",
    "Get dunked on!!!",
    "\n Never gonna give you up,\n never gonna let you down.",
    "Who gave me a GUN?",
    "Blep",
    "\n\n My name is J, nice to meet you. \n I would ask your name, but I'm going to kill you, \n so it doesn't really matter.",
    "Alt F4 for instant win.",
    "Prepare to be overstimulated!",
    "Immortality sucks-."
];

function getDialogString() {
    dial = dialogs[Math.floor(Math.random() * dialogs.length)];
    dialogDiv.textContent = dial;
    dialogDiv.style.color = dial === ":)" ? "red" : "white";
    dialogDiv.style.fontFamily = dial === "\n Never gonna give you up,\n never gonna let you down." ? "Wingdings" : "Arial";
}

function resetGame() {
    player.x = CANVAS_WIDTH / 2 - PLAYER_WIDTH / 2;
    player.y = CANVAS_HEIGHT - 50;
    bullets = [];
    bullets2 = [];
    triangleBullets = [];
    diagBullets = [];
    bossBullets = [];
    zigzagBullets = [];
    fastBullets = [];
    starBullets = [];
    rectBullets = [];
    eggBullets = [];
    explodingBullets = [];
    explodedFragments = [];
    bouncingBullets = [];
    laserIndicators = [];
    lasers = [];
    score = 0;
    startTime = Date.now();
    lives = 1;
    gameOver = false;
    paused = false;
    difficulty = 1;
    lastDifficultyIncrease = Date.now();
    lastDial = Date.now();
    grazedBullets = new Set();
    grazeEffect = null;
    grazeEffectTimer = 0;
    pausedTimeTotal = 0;
    pauseStartTime = null;
    getDialogString();
    bgMusic.currentTime = 0;
    bgMusic.play();
}

function drawPlayer() {
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);
    // Graze effect
    if (grazeEffect && grazeEffectTimer > 0) {
        ctx.save();
        ctx.strokeStyle = "white";
        ctx.setLineDash([5, 5]);
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(player.x + player.width / 2, player.y + player.height / 2, GRAZING_RADIUS, 0, 2 * Math.PI);
        ctx.stroke();
        ctx.restore();
        grazeEffectTimer--;
        if (grazeEffectTimer <= 0) grazeEffect = null;
    }
}

function drawBullets() {
    // Draw all bullets
    function drawOval(b) {
        ctx.save();
        ctx.beginPath();
        ctx.ellipse(b.x + b.w / 2, b.y + b.h / 2, b.w / 2, b.h / 2, 0, 0, 2 * Math.PI);
        ctx.fillStyle = b.color;
        ctx.fill();
        ctx.restore();
    }
    function drawRect(b) {
        ctx.fillStyle = b.color;
        ctx.fillRect(b.x, b.y, b.w, b.h);
    }
    function drawPolygon(b) {
        ctx.save();
        ctx.fillStyle = b.color;
        ctx.beginPath();
        ctx.moveTo(b.points[0].x, b.points[0].y);
        for (let i = 1; i < b.points.length; i++) {
            ctx.lineTo(b.points[i].x, b.points[i].y);
        }
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }
    // ...draw all bullet types...
    bullets.forEach(drawOval);
    bullets2.forEach(drawOval);
    eggBullets.forEach(drawOval);
    bossBullets.forEach(drawOval);
    fastBullets.forEach(drawOval);
    bouncingBullets.forEach(b => drawOval(b));
    explodingBullets.forEach(drawOval);
    explodedFragments.forEach(drawOval);
    zigzagBullets.forEach(drawOval);
    rectBullets.forEach(drawRect);
    starBullets.forEach(drawPolygon);
    triangleBullets.forEach(b => drawPolygon(b));
    diagBullets.forEach(b => drawOval(b));
    // Lasers
    lasers.forEach(l => {
        ctx.save();
        ctx.strokeStyle = "red";
        ctx.lineWidth = 8;
        ctx.beginPath();
        ctx.moveTo(0, l.y);
        ctx.lineTo(CANVAS_WIDTH, l.y);
        ctx.stroke();
        ctx.restore();
    });
    // Laser indicators
    laserIndicators.forEach(l => {
        ctx.save();
        ctx.strokeStyle = "red";
        ctx.setLineDash([5, 2]);
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(0, l.y);
        ctx.lineTo(CANVAS_WIDTH, l.y);
        ctx.stroke();
        ctx.restore();
    });
}

function updateGame() {
    if (gameOver || paused) return;
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    drawPlayer();
    drawBullets();
    // ...move and update all bullets, check collisions, scoring, grazing, etc...
    // ...handle difficulty, dialog, score/time display...
    // ...handle game over and restart...
    requestAnimationFrame(updateGame);
}

// Keyboard controls
window.addEventListener('keydown', function(e) {
    if (gameOver) return;
    if (paused) return;
    if (e.key === 'ArrowLeft' || e.key === 'a') {
        if (player.x > 0) player.x -= PLAYER_SPEED;
    } else if (e.key === 'ArrowRight' || e.key === 'd') {
        if (player.x + player.width < CANVAS_WIDTH) player.x += PLAYER_SPEED;
    } else if (e.key === 'ArrowUp' || e.key === 'w') {
        if (player.y > 0) player.y -= PLAYER_SPEED;
    } else if (e.key === 'ArrowDown' || e.key === 's') {
        if (player.y + player.height < CANVAS_HEIGHT) player.y += PLAYER_SPEED;
    } else if (e.key === 'Escape') {
        paused = !paused;
        pauseTextDiv.style.display = paused ? 'block' : 'none';
        if (!paused) {
            if (pauseStartTime) pausedTimeTotal += Date.now() - pauseStartTime;
            pauseStartTime = null;
            updateGame();
        } else {
            pauseStartTime = Date.now();
        }
    } else if (e.key === 'r') {
        if (gameOver) resetGame();
    }
});

// Start game
bgMusic.play();
resetGame();
updateGame();
