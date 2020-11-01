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
var baseLaserColor = "#f00"

var floatingCount = 0;
var isFloatingUp = true;
var shouldFloatIncrement = true;
var canUserAttack = true;
var enemyFrame = 1;
var doFrameIncrement = false
var isFrameForward = true
var laserFrameCount = 5

//- TEST STUFF -//
var testHealth = 1000000
var testHealthRemaining = testHealth
var testName = "Candy Monster"
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
    var render_name = "🎃 " + name + " 🎃";
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

function renderEnemy(baseImageUrl, frames) {
    if (floatingCount >= 30) {
        isFloatingUp = false
    } else if (floatingCount <= 0) {
        isFloatingUp = true
    }
    let enemy_width = canvas.width / 4
    let enemy_height = canvas.height / 2
    updateHiddenImage(baseImageUrl + enemyFrame + ".png")
    ctx.drawImage(document.getElementById("hiddenImagePreview"), canvas.width / 2 - (enemy_width / 2), canvas.height / 2 - (enemy_height / 2) + floatingCount, enemy_width, enemy_height)
    if (doFrameIncrement) {
        isFloatingUp && shouldFloatIncrement ? floatingCount++ : floatingCount--;
        if (enemyFrame >= frames) {
            isFrameForward = false
        } else if (enemyFrame <= 1) {
            isFrameForward = true
        }
        isFrameForward ? enemyFrame++ : enemyFrame--;
        if (enemyFrame === 0) enemyFrame = 1;
    }
    doFrameIncrement = !doFrameIncrement
}

function updateHiddenImage(url) {
    document.getElementById("hiddenImagePreview").src = url
}

function populateShop(items) {
    let shop = document.getElementById("shopItems")
    while (shop.firstChild) {
        shop.removeChild(shop.firstChild)
    }
    for (let item of items) {
        let img = new Image()
        img.src = item.url
        let price = document.createElement("p")
        price.innerText = item.price + " 💰"
        let name = document.createElement("p")
        name.innerText = item.name
        let itemDiv = document.createElement("div")
        itemDiv.classList.add("item")
        itemDiv.append(img);
        let namePriceDiv = document.createElement("div")
        namePriceDiv.classList.add('item-name')
        namePriceDiv.append(name, price)
        itemDiv.append(namePriceDiv)
        shop.append(itemDiv)
    }
}

function populateItems(items) {
    let itemsBox = document.getElementById("itemItems")
    while (itemsBox.firstChild) {
        itemsBox.removeChild(itemsBox.firstChild)
    }
    for (let item of items) {
        let img = new Image()
        img.src = item.url
        let amount = document.createElement("p")
        amount.innerText = "x" + item.amount
        let itemDiv = document.createElement("div")
        itemDiv.classList.add("item")
        itemDiv.append(img);
        let namePriceDiv = document.createElement("div")
        namePriceDiv.classList.add('item-name')
        namePriceDiv.append(amount)
        itemDiv.append(namePriceDiv)
        itemsBox.append(itemDiv)
    }
}

function animate() {
    ctx.fillStyle = backgroundColor
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    drawHealthBar(testHealthRemaining, testHealth)
    drawName(testName)
    // renderEnemy("/candy/candy", 9)
    window.requestAnimationFrame(animate)
}

function setShopCategory(categoryName) {
    let categories = document.getElementsByClassName("shopCategory")
    for (let category of categories) {
        category.classList.remove("selected")
        if (category.id === categoryName) category.classList.add("selected");
    }
    populateShop([{
        url: "/bomb.png",
        price: 10,
        name: "Bomb"
    }])
}

function setItemsCategory(categoryName) {
    let categories = document.getElementsByClassName("itemCategory")
    for (let category of categories) {
        category.classList.remove("selected")
        if (category.id === categoryName) category.classList.add("selected");
    }
    populateItems([{
        url: "/bomb.png",
        amount: 3
    }])
}

canvas.height = canvas.parentElement.clientHeight
canvas.width = canvas.parentElement.clientWidth
canvas.addEventListener("click", function () {
    hurtEnemy(testAttackCooldown)
})
window.addEventListener("resize", resizeCanvas)
for (let category of document.getElementsByClassName("shopCategory")) {
    category.addEventListener("click", () => setShopCategory(category.id))
}
for (let category of document.getElementsByClassName("itemCategory")) {
    category.addEventListener("click", () => setItemsCategory(category.id))
}
populateShop([{
    url: "/bomb.png",
    price: 10,
    name: "Bomb"
}])
populateItems([{
    url: "/bomb.png",
    amount: 3
}])
animate();