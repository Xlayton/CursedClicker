var canvas = document.getElementById("gameCanvas");
var ctx = canvas.getContext("2d");
var backgroundColor = "#454545";
var healthStage1Color = "#00dd00";
var healthStage2Color = "#dddd00";
var healthStage3Color = "#ffa500";
var healthStage4Color = "#dd0000";
var healthBarBackgroundColor = "#000";
var textColor = "#fff";
var textOutlineColor = "#000";
var floatingCount = 0;
var isFloatingUp = true;
var shouldFloatIncrement = true;
var canUserAttack = true;

//- TEST STUFF -//
var testHealth = 1000000
var testHealthRemaining = testHealth
var testName = "Pumpkin King"
var shouldHealthDecrease = true
var testAttackCooldown = 500
//- TEST STUFF END -//

function resizeCanvas() {
    canvas.height = canvas.parentElement.clientHeight;
    canvas.width = canvas.parentElement.clientWidth;
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function drawHealthBar(healthValue, maxHealthValue) {
    ctx.fillStyle = healthBarBackgroundColor;
    ctx.fillRect(canvas.width / 12, canvas.height / 18 + 25, canvas.width / 1.25, canvas.height / 18);
    ctx.fillStyle = healthValue / maxHealthValue > .75 ? healthStage1Color : healthValue / maxHealthValue > .5 ? healthStage2Color : healthValue / maxHealthValue > .25 ? healthStage3Color : healthStage4Color
    ctx.fillRect(canvas.width / 12, canvas.height / 18 + 25, canvas.width / 1.25 * (healthValue / maxHealthValue), canvas.height / 18);
    ctx.fillStyle = textColor;
    ctx.font = "" + canvas.height / 18 + "px Arial";
    ctx.textAlign = "center";
    var healthString = healthValue.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    var maxHealthString = maxHealthValue.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    ctx.fillText("" + healthString + "/" + maxHealthString, canvas.width / 2, canvas.height / 9.75 + 25);
    ctx.strokeStyle = textOutlineColor;
    ctx.lineWidth = 2
    ctx.strokeText("" + healthString + "/" + maxHealthString, canvas.width / 2, canvas.height / 9.75 + 25);
}

function drawName(name) {
    ctx.fillStyle = textColor;
    ctx.font = "" + canvas.height / 18 + "px Arial";
    ctx.textAlign = "center";
    let render_name = "🎃 " + name + " 🎃";
    ctx.fillText(render_name, canvas.width / 2, canvas.height / 18 + 15, canvas.width / 2);
    ctx.strokeStyle = textOutlineColor;
    ctx.lineWidth = 1
    ctx.strokeText(render_name, canvas.width / 2, canvas.height / 18 + 15, canvas.width / 2);
}

function hurtEnemy(cooldownTime) {
    if (canUserAttack) {
        testHealthRemaining -= 10000;
        canUserAttack = false;
        setTimeout(function () {
            canUserAttack = true
        }, cooldownTime)
    }
}

function renderEnemy() {
    if (floatingCount >= 30) {
        isFloatingUp = false
    } else if (floatingCount <= 0) {
        isFloatingUp = true
    }
    let enemy_width = canvas.width / 4
    let enemy_height = canvas.height / 2
    // ctx.fillRect(canvas.width / 2 - (enemy_width / 2), canvas.height / 2 - (enemy_height / 2) + floatingCount, enemy_width, enemy_height)
    ctx.drawImage(document.getElementById("hiddenImagePreview"), canvas.width / 2 - (enemy_width / 2), canvas.height / 2 - (enemy_height / 2) + floatingCount, enemy_width, enemy_height)
    isFloatingUp && shouldFloatIncrement ? floatingCount++ : floatingCount--;
}

function updateHiddenImage(url) {
    document.getElementById("hiddenImagePreview").src = url
}

function animate() {
    ctx.fillStyle = backgroundColor
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    drawHealthBar(testHealthRemaining, testHealth)
    drawName(testName)
    renderEnemy()
    window.requestAnimationFrame(animate)
}

canvas.height = canvas.parentElement.clientHeight
canvas.width = canvas.parentElement.clientWidth
canvas.addEventListener("click", function () {
    hurtEnemy(testAttackCooldown)
})
window.addEventListener("resize", resizeCanvas)
animate();