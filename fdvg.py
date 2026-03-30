<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لعبة التخمين السرية</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: white; text-align: center; padding: 20px; }
        .card { background: #1e1e1e; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); max-width: 400px; margin: auto; }
        button { background: #6200ee; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; font-size: 16px; margin: 10px 0; width: 100%; }
        button:hover { background: #3700b3; }
        input, select { width: 100%; padding: 10px; margin: 10px 0; border-radius: 8px; border: 1px solid #333; background: #2c2c2c; color: white; box-sizing: border-box; }
        .hidden { display: none; }
        .secret-number { font-size: 48px; color: #03dac6; font-weight: bold; margin: 20px 0; }
        .player-name { font-size: 24px; color: #bb86fc; }
    </style>
</head>
<body>

<div class="card">
    <h2>لعبة التخمين 📱</h2>
    
    <div id="setup-screen">
        <label>اختر نطاق الأرقام:</label>
        <select id="range-select">
            <option value="100">0 - 100</option>
            <option value="1000">0 - 1000</option>
            <option value="500-1000">500 - 1000</option>
        </select>
        
        <label>أدخل أسماء اللاعبين (افصل بينهم بفاصلة):</label>
        <input type="text" id="player-names" placeholder="عبود، فيصل، خالد">
        <button onclick="startGame()">ابدأ اللعب</button>
    </div>

    <div id="pass-screen" class="hidden">
        <p class="player-name" id="current-player-instruction"></p>
        <p>خذ الجوال واضغط الزر لعرض رقمك</p>
        <button onclick="showNumber()">عرض الرقم</button>
    </div>

    <div id="reveal-screen" class="hidden">
        <p>رقمك السري هو:</p>
        <div class="secret-number" id="display-number"></div>
        <p>لا تعلم أحد! احفظه ثم اضغط تم</p>
        <button onclick="nextPlayer()">تم (إخفاء)</button>
    </div>

    <div id="game-screen" class="hidden">
        <h3>بدأت اللعبة! 🕵️‍♂️</h3>
        <p id="turn-info"></p>
        <div id="players-list" style="text-align: right; margin-top: 15px;"></div>
        <button onclick="location.reload()" style="background: #cf6679;">إعادة اللعبة</button>
    </div>
</div>

<script>
    let players = [];
    let currentPlayerIndex = 0;
    let gameData = [];

    function startGame() {
        const namesInput = document.getElementById('player-names').value;
        if (!namesInput) return alert("سجل الأسماء أولاً يا وحش");
        
        players = namesInput.split(/[,،]/).map(n => n.trim()).filter(n => n !== "");
        const range = document.getElementById('range-select').value;
        
        let min = 0, max = 100;
        if(range === "1000") max = 1000;
        if(range === "500-1000") { min = 500; max = 1000; }

        gameData = players.map(name => ({
            name: name,
            number: Math.floor(Math.random() * (max - min + 1)) + min
        }));

        document.getElementById('setup-screen').classList.add('hidden');
        showPassScreen();
    }

    function showPassScreen() {
        if (currentPlayerIndex < gameData.length) {
            document.getElementById('pass-screen').classList.remove('hidden');
            document.getElementById('current-player-instruction').innerText = `عط الجوال لـ: ${gameData[currentPlayerIndex].name}`;
        } else {
            showFinalScreen();
        }
    }

    function showNumber() {
        document.getElementById('pass-screen').classList.add('hidden');
        document.getElementById('reveal-screen').classList.remove('hidden');
        document.getElementById('display-number').innerText = gameData[currentPlayerIndex].number;
    }

    function nextPlayer() {
        document.getElementById('reveal-screen').classList.add('hidden');
        currentPlayerIndex++;
        showPassScreen();
    }

    function showFinalScreen() {
        document.getElementById('pass-screen').classList.add('hidden');
        document.getElementById('game-screen').classList.remove('hidden');
        
        let listHtml = "<strong>اللاعبين في اللعبة:</strong><ul>";
        gameData.forEach(p => {
            listHtml += `<li>${p.name} (عنده رقم سري)</li>`;
        });
        listHtml += "</ul><p>الآن فلان يسأل علان.. حاولوا تعرفون الأرقام!</p>";
        document.getElementById('players-list').innerHTML = listHtml;
    }
</script>

</body>
</html>
