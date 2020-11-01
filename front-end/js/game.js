if (!/email/.test(document.cookie) || !/key/.test(document.cookie)) window.location = "./login";
var key = document.cookie.match(/(?<=key=)\S*/)[0].replace(";", "")
var email = document.cookie.match(/(?<=email=)\S*/)[0].replace(";", "")

var apiurl = "http://93dc8cc5696e.ngrok.io/"

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
var doFrameIncrement = false;
var isFrameForward = true;
var balance = 0;

var consumables = []
var upgrades = []
var name = ""
var maxHealth = 0
var currentHealth = 0
var imgPath = ""

//- TEST STUFF -//
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
        fetch(apiurl + "/attacktheboss", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "email": email,
                    "key": key
                })

            })
            .then(res => res.json())
            .then(data => {
                currentHealth = data.currenthealth
                maxHealth = data.health
                name = data.name
                balance += data.balance
            })
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

function drawMoney() {
    ctx.fillStyle = textColor;
    ctx.font = "" + canvas.height / 18 + "px Arial";
    ctx.textAlign = "end";
    var render_name = balance + " 🤑";
    ctx.fillText(render_name, canvas.width, canvas.height / 18 + 15, canvas.width / 2);
    ctx.strokeStyle = textOutlineColor;
    ctx.lineWidth = 1
    ctx.strokeText(render_name, canvas.width, canvas.height / 18 + 15, canvas.width / 2);
}

function updateHiddenImage(url) {
    document.getElementById("hiddenImagePreview").src = url
}

function populateShop(items, isConsumable) {
    let shop = document.getElementById("shopItems")
    while (shop.firstChild) {
        shop.removeChild(shop.firstChild)
    }
    for (let item of items) {
        let img = new Image()
        img.src = apiurl + item.imgpath
        let price = document.createElement("p")
        price.innerText = item.price + " 🤑"
        let name = document.createElement("p")
        name.innerText = item.name
        let itemDiv = document.createElement("div")
        itemDiv.classList.add("item")
        itemDiv.append(img);
        let namePriceDiv = document.createElement("div")
        namePriceDiv.classList.add('item-name')
        namePriceDiv.append(name, price)
        itemDiv.append(namePriceDiv)
        if (isConsumable) {
            itemDiv.addEventListener("click", function () {
                fetch(apiurl + "/buyconsumable", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            "email": email,
                            "key": key,
                            "itemname": item.name
                        })
                    }).then(res => res.json())
                    .then(data => {
                        balance -= item.price
                        for (var thing in data) {
                            if (data[thing].type === "consumable") {
                                consumables.push(data[thing])
                            } else if (data[thing].type === "upgrade") {
                                upgrades.push(data[thing])
                            }
                        }
                        console.log(consumables, upgrades)
                        setItemsCategory("itemConsumables")
                    })
            })
        }
        shop.append(itemDiv)
    }
}

function populateItems(items, isConsumable) {
    let itemsBox = document.getElementById("itemItems")
    while (itemsBox.firstChild) {
        itemsBox.removeChild(itemsBox.firstChild)
    }
    for (let item of items) {
        console.log(item)
        let img = new Image()
        img.src = apiurl + item.imgpath
        let amount = document.createElement("p")
        amount.innerText = "x" + item.value
        let itemDiv = document.createElement("div")
        itemDiv.classList.add("item")
        itemDiv.append(img);
        let namePriceDiv = document.createElement("div")
        namePriceDiv.classList.add('item-name')
        namePriceDiv.append(amount)
        itemDiv.append(namePriceDiv)
        itemsBox.append(itemDiv)
        if (isConsumable) {
            itemDiv.addEventListener("click", function () {
                fetch(apiurl + "/consume", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            "email": email,
                            "key": key,
                            "itemname": "bomb"
                        })
                    }).then(res => res.json())
                    .then(data => {
                        balance -= item.price
                        for (var thing in data) {
                            if (data[thing].type === "consumable") {
                                consumables.push(data[thing])
                            } else if (data[thing].type === "upgrade") {
                                upgrades.push(data[thing])
                            }
                        }
                        console.log(consumables, upgrades)
                        setItemsCategory("itemConsumables")
                    })
            })
        }
    }
}

function animate() {
    ctx.fillStyle = backgroundColor
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    drawHealthBar(currentHealth, maxHealth)
    drawMoney()
    drawName(name)
    renderEnemy("/pumpkin/pumpkin", 10)
    window.requestAnimationFrame(animate)
}

function setShopCategory(categoryName) {
    let categories = document.getElementsByClassName("shopCategory")
    for (let category of categories) {
        category.classList.remove("selected")
        if (category.id === categoryName) category.classList.add("selected");
    }
    if (categoryName === "shopConsumables") {
        fetch(apiurl + "/getconsumables", {
                method: "GET",
            }).then(res => res.json())
            .then(data => {
                populateShop(data, true)
            })
    } else {
        fetch(apiurl + "/getitems", {
                method: "GET",
            }).then(res => res.json())
            .then(data => {
                console.log(data)
                populateShop(data, false)
            })
    }
}

function setItemsCategory(categoryName) {
    let categories = document.getElementsByClassName("itemCategory")
    for (let category of categories) {
        category.classList.remove("selected")
        if (category.id === categoryName) category.classList.add("selected");
    }
    categoryName === "itemConsumables" ? populateItems(consumables, true) : populateItems(upgrades, false);
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

console.log(email, key)

fetch(apiurl + "/getplayerinventory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "email": email,
            "key": key
        })
    }).then(res => res.json())
    .then(data => {
        for (var thing in data) {
            if (data[thing].type === "consumable") {
                consumables.push(data[thing])
            } else if (data[thing].type === "upgrade") {
                upgrades.push(data[thing])
            }
        }
        console.log(consumables, upgrades)
        setItemsCategory("itemConsumables")
    })
fetch(apiurl + "/getplayerbalance", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "email": email,
            "key": key
        })
    }).then(res => res.json())
    .then(data => {

        balance = data.currentplayerbalance
    })
fetch(apiurl + "/getconsumables", {
        method: "GET",
    }).then(res => res.json())
    .then(data => {
        populateShop(data, true)
    })
fetch(apiurl + "/getcurrentboss", {
        method: "GET",
    }).then(res => res.json())
    .then(data => {
        name = data.name
        maxHealth = data.health
        currentHealth = data.currenthealth
        imgPath = data.imgpath
    })
animate();