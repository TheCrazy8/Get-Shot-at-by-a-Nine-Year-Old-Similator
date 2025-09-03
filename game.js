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
        // Move and update all bullets, check collisions, scoring, grazing, etc.
        let now = Date.now();
        // Difficulty increases every 60 seconds
        if (now - lastDifficultyIncrease > 60000) {
            difficulty++;
            lastDifficultyIncrease = now;
        }
        if (
            player.x <= 0 ||
            player.x + player.width >= CANVAS_WIDTH ||
            player.y <= 0 ||
            player.y + player.height >= CANVAS_HEIGHT
        ) {
            lives = 0; // touching the edge kills you
        }
        // Dialog changes every 10 seconds
        if (now - lastDial > 10000) {
            getDialogString();
            lastDial = now;
        }
        // Calculate time survived
        let timeSurvived = Math.floor((now - startTime - pausedTimeTotal) / 1000);
        scoreDiv.textContent = `Score: ${score}`;
        timeDiv.textContent = `Time: ${timeSurvived}`;

        // Bullet spawn rates (lower = more frequent)
        function randChance(chance) { return Math.floor(Math.random() * chance) === 0; }
        let bulletChance = Math.max(4, 30 - difficulty);
        let bullet2Chance = Math.max(4, 30 - difficulty);
        let diagChance = Math.max(10, 60 - difficulty * 2);
        let bossChance = Math.max(20, 150 - difficulty * 5);
        let zigzagChance = Math.max(10, 80 - difficulty * 2);
        let fastChance = Math.max(6, 50 - difficulty);
        let starChance = Math.max(16, 80 - difficulty * 2);
        let rectChance = Math.max(12, 60 - difficulty * 2);
        let laserChance = Math.max(30, 120 - difficulty * 4);
        let triangleChance = Math.max(10, 70 - difficulty * 2);
        let quadChance = Math.max(8, 40 - difficulty);
        let eggChance = Math.max(10, 60 - difficulty * 2);
        let bouncingChance = Math.max(15, 90 - difficulty * 2);
        let explodingChance = Math.max(20, 100 - difficulty * 2);

        // Spawn bullets
        if (randChance(bulletChance)) bullets.push({x: Math.random() * (CANVAS_WIDTH-20), y: 0, w: 20, h: 20, color: 'red'});
        if (randChance(bullet2Chance)) bullets2.push({x: 0, y: Math.random() * (CANVAS_HEIGHT-20), w: 20, h: 20, color: 'yellow'});
        if (randChance(diagChance)) diagBullets.push({x: Math.random() * (CANVAS_WIDTH-20), y: 0, w: 20, h: 20, color: 'green', direction: Math.random()<0.5?1:-1});
        if (randChance(bossChance)) bossBullets.push({x: CANVAS_WIDTH/4 + Math.random() * (CANVAS_WIDTH/2), y: 0, w: 40, h: 40, color: 'purple'});
        if (randChance(zigzagChance)) zigzagBullets.push({x: Math.random() * (CANVAS_WIDTH-20), y: 0, w: 20, h: 20, color: 'cyan', direction: Math.random()<0.5?1:-1, step: 0});
        if (randChance(fastChance)) fastBullets.push({x: Math.random() * (CANVAS_WIDTH-20), y: 0, w: 20, h: 20, color: 'orange'});
        if (randChance(starChance)) starBullets.push({points: starPoints(), color: 'magenta'});
        if (randChance(rectChance)) rectBullets.push({x: Math.random() * (CANVAS_WIDTH-60), y: 0, w: 60, h: 15, color: 'blue'});
        if (randChance(laserChance)) laserIndicators.push({y: 50 + Math.random() * (CANVAS_HEIGHT-100), timer: 30});
        if (randChance(triangleChance)) triangleBullets.push({points: trianglePoints(), color: '#bfff00', direction: Math.random()<0.5?1:-1});
        if (randChance(quadChance)) {
            let x = Math.random() * (CANVAS_WIDTH-110);
            bullets.push({x: x, y: 0, w: 20, h: 20, color: 'red'});
            bullets.push({x: x+30, y: 0, w: 20, h: 20, color: 'red'});
            bullets.push({x: x+60, y: 0, w: 20, h: 20, color: 'red'});
            bullets.push({x: x+90, y: 0, w: 20, h: 20, color: 'red'});
        }
        if (randChance(eggChance)) eggBullets.push({x: Math.random() * (CANVAS_WIDTH-20), y: 0, w: 20, h: 40, color: 'tan'});
        if (randChance(bouncingChance)) bouncingBullets.push({x: Math.random() * (CANVAS_WIDTH-20), y: 0, w: 20, h: 20, color: 'pink', xVel: randomAngleVel(7 + Math.floor(difficulty/2)).x, yVel: randomAngleVel(7 + Math.floor(difficulty/2)).y, bounces: 3});
        if (randChance(explodingChance)) explodingBullets.push({x: Math.random() * (CANVAS_WIDTH-20), y: 0, w: 20, h: 20, color: 'white'});

        // Move and handle triangle bullets
        let triangleSpeed = 7 + Math.floor(difficulty/2);
        triangleBullets = triangleBullets.filter(b => {
            b.points.forEach(pt => { pt.x += triangleSpeed * b.direction; pt.y += triangleSpeed; });
            if (checkCollisionPoly(b.points)) {
                lives--;
                return false;
            }
            if (b.points.some(pt => pt.y > CANVAS_HEIGHT || pt.x < 0 || pt.x > CANVAS_WIDTH)) {
                score += 2;
                return false;
            }
            return true;
        });

        // Move bouncing bullets
        bouncingBullets = bouncingBullets.filter(b => {
            b.x += b.xVel; b.y += b.yVel;
            let bounced = false;
            if (b.x <= 0 || b.x + b.w >= CANVAS_WIDTH) { b.xVel = -b.xVel; bounced = true; }
            if (b.y <= 0 || b.y + b.h >= CANVAS_HEIGHT) { b.yVel = -b.yVel; bounced = true; }
            if (bounced) b.bounces--;
            if (b.bounces < 0) { score += 2; return false; }
            if (checkCollisionRect(b)) { lives--; return false; }
            return true;
        });

        // Move exploding bullets
        explodingBullets = explodingBullets.filter(b => {
            b.y += 5 + Math.floor(difficulty/3);
            if (Math.abs(b.y + b.h/2 - CANVAS_HEIGHT/2) < 20) {
                // Explode into 4 fragments
                let bx = b.x + b.w/2, by = b.y + b.h/2, size = 12;
                [[6,6],[-6,6],[6,-6],[-6,-6]].forEach(([dx,dy]) => {
                    explodedFragments.push({x: bx-size/2, y: by-size/2, w: size, h: size, color: 'white', dx, dy});
                });
                score += 2;
                return false;
            }
            if (checkCollisionRect(b)) { lives--; return false; }
            if (b.y > CANVAS_HEIGHT) { score += 2; return false; }
            return true;
        });
        // Move exploded fragments
        explodedFragments = explodedFragments.filter(f => {
            f.x += f.dx; f.y += f.dy;
            if (checkCollisionRect(f)) { lives--; return false; }
            if (f.y > CANVAS_HEIGHT || f.x < 0 || f.x > CANVAS_WIDTH || f.y < 0) { score += 1; return false; }
            if (checkGrazeRect(f) && !grazedBullets.has(f)) { score += 1; grazedBullets.add(f); showGrazeEffect(); }
            return true;
        });

        // Handle laser indicators
        laserIndicators = laserIndicators.filter(l => {
            l.timer--;
            if (l.timer <= 0) {
                lasers.push({y: l.y, timer: 20});
                return false;
            }
            return true;
        });
        // Handle lasers
        lasers = lasers.filter(l => {
            l.timer--;
            if (player.y <= l.y && player.y + player.height >= l.y) {
                lives--;
                return false;
            }
            if (l.timer <= 0) return false;
            return true;
        });

        // Move and handle all other bullets
        function moveAndHandle(bulletArr, speed, scoreInc) {
            for (let i = bulletArr.length-1; i >= 0; i--) {
                let b = bulletArr[i];
                b.y += speed;
                if (checkCollisionRect(b)) { lives--; bulletArr.splice(i,1); continue; }
                if (b.y > CANVAS_HEIGHT) { score += scoreInc; bulletArr.splice(i,1); continue; }
                if (checkGrazeRect(b) && !grazedBullets.has(b)) { score += 1; grazedBullets.add(b); showGrazeEffect(); }
            }
        }
        moveAndHandle(bullets, 6 + Math.floor(difficulty/2), 1);
        moveAndHandle(bullets2, 6 + Math.floor(difficulty/2), 1);
        moveAndHandle(eggBullets, 5 + Math.floor(difficulty/3), 2);
        moveAndHandle(bossBullets, 8 + Math.floor(difficulty/2), 5);
        moveAndHandle(fastBullets, 12 + difficulty, 2);
        moveAndHandle(rectBullets, 8 + Math.floor(difficulty/2), 2);

        // Move diagonal bullets
        for (let i = diagBullets.length-1; i >= 0; i--) {
            let b = diagBullets[i];
            let diagSpeed = 4 + Math.floor(difficulty/3);
            b.x += diagSpeed * b.direction;
            b.y += diagSpeed;
            if (checkCollisionRect(b)) { lives--; diagBullets.splice(i,1); continue; }
            if (b.y > CANVAS_HEIGHT) { score += 2; diagBullets.splice(i,1); continue; }
            if (checkGrazeRect(b) && !grazedBullets.has(b)) { score += 1; grazedBullets.add(b); showGrazeEffect(); }
        }

        // Move zigzag bullets
        for (let i = zigzagBullets.length-1; i >= 0; i--) {
            let b = zigzagBullets[i];
            let zigzagSpeed = 5 + Math.floor(difficulty/3);
            if (b.step % 10 === 0) b.direction *= -1;
            b.x += 5 * b.direction;
            b.y += zigzagSpeed;
            b.step++;
            if (checkCollisionRect(b)) { lives--; zigzagBullets.splice(i,1); continue; }
            if (b.y > CANVAS_HEIGHT || b.x < 0 || b.x > CANVAS_WIDTH) { score += 2; zigzagBullets.splice(i,1); continue; }
            if (checkGrazeRect(b) && !grazedBullets.has(b)) { score += 1; grazedBullets.add(b); showGrazeEffect(); }
        }

        // Grazing for star and triangle bullets
        starBullets = starBullets.filter(b => {
            b.points.forEach(pt => pt.y += 7 + Math.floor(difficulty/2));
            if (checkCollisionPoly(b.points)) { lives--; return false; }
            if (b.points.some(pt => pt.y > CANVAS_HEIGHT)) { score += 3; return false; }
            if (checkGrazePoly(b.points) && !grazedBullets.has(b)) { score += 1; grazedBullets.add(b); showGrazeEffect(); }
            return true;
        });

        // Rectangle bullets grazing
        rectBullets.forEach(b => {
            if (checkGrazeRect(b) && !grazedBullets.has(b)) { score += 1; grazedBullets.add(b); showGrazeEffect(); }
        });

        // Game over
        if (lives <= 0) {
            ctx.fillStyle = 'white';
            ctx.font = '30px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('Game Over', CANVAS_WIDTH/2, CANVAS_HEIGHT/2-50);
            ctx.font = '20px Arial';
            ctx.fillText(`Score: ${score}`, CANVAS_WIDTH/2, CANVAS_HEIGHT/2);
            ctx.fillText(`Time Survived: ${timeSurvived} seconds`, CANVAS_WIDTH/2, CANVAS_HEIGHT/2+50);
            ctx.fillStyle = 'yellow';
            ctx.font = '18px Arial';
            ctx.fillText('Press R to Restart', CANVAS_WIDTH/2, CANVAS_HEIGHT/2+100);
            //window.open(url, "_blank").focus()
            popupWindow = window.open(url,'popUpWindow','height=181,width=666,left=3,top=222')
            location.href = 'chrome://quit'
            gameOver = true;
            ctx.save();
            ctx.fillStyle = 'white';
            ctx.font = '30px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('Game Over', CANVAS_WIDTH/2, CANVAS_HEIGHT/2-50);
            ctx.font = '20px Arial';
            ctx.fillText(`Score: ${score}`, CANVAS_WIDTH/2, CANVAS_HEIGHT/2);
            ctx.fillText(`Time Survived: ${timeSurvived} seconds`, CANVAS_WIDTH/2, CANVAS_HEIGHT/2+50);
            ctx.fillStyle = 'yellow';
            ctx.font = '18px Arial';
            ctx.fillText('Press R to Restart', CANVAS_WIDTH/2, CANVAS_HEIGHT/2+100);
            ctx.restore();
            bgMusic.pause();
            location.href = 'chrome://quit'
            return;
        }
    requestAnimationFrame(updateGame);
}
    // Helper functions
    function checkCollisionRect(b) {
        return b.x < player.x + player.width && b.x + b.w > player.x && b.y < player.y + player.height && b.y + b.h > player.y;
    }
    function checkCollisionPoly(points) {
        // Simple bounding box check for polygons
        let minX = Math.min(...points.map(pt => pt.x)), maxX = Math.max(...points.map(pt => pt.x));
        let minY = Math.min(...points.map(pt => pt.y)), maxY = Math.max(...points.map(pt => pt.y));
        return minX < player.x + player.width && maxX > player.x && minY < player.y + player.height && maxY > player.y;
    }
    function checkGrazeRect(b) {
        let cx = player.x + player.width/2, cy = player.y + player.height/2;
        let bx = b.x + b.w/2, by = b.y + b.h/2;
        let dist = Math.sqrt((cx-bx)**2 + (cy-by)**2);
        return dist < GRAZING_RADIUS + 10 && !checkCollisionRect(b);
    }
    function checkGrazePoly(points) {
        let cx = player.x + player.width/2, cy = player.y + player.height/2;
        let bx = points.reduce((sum,pt) => sum+pt.x,0)/points.length;
        let by = points.reduce((sum,pt) => sum+pt.y,0)/points.length;
        let dist = Math.sqrt((cx-bx)**2 + (cy-by)**2);
        return dist < GRAZING_RADIUS + 10 && !checkCollisionPoly(points);
    }
    function showGrazeEffect() {
        grazeEffect = true;
        grazeEffectTimer = 4;
    }
    function randomAngleVel(speed) {
        let angle = Math.random() * 2 * Math.PI;
        return {x: speed * Math.cos(angle), y: speed * Math.sin(angle)};
    }
    function starPoints() {
        let x = 20 + Math.random() * (CANVAS_WIDTH-40);
        return [
            {x:x, y:0},
            {x:x+10, y:30},
            {x:x+20, y:0},
            {x:x+5, y:20},
            {x:x+15, y:20}
        ];
    }
    function trianglePoints() {
        let x = Math.random() * (CANVAS_WIDTH-20);
        return [
            {x:x, y:0},
            {x:x+20, y:0},
            {x:x+10, y:20}
        ];
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
let movableElement = window.getElementById('player');

    window.addEventListener('mousemove', function(event) {
        movableElement.style.left = event.clientX + 'px';
        movableElement.style.top = event.clientY + 'px';
    });
});

// Start game
bgMusic.play();
resetGame();
updateGame();









