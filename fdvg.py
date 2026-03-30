// الأسماء اللي يدخلها المستخدم
let players = ["عبود", "فيصل", "سارة"]; 

// النطاق المختار (مثلاً من 0 إلى 100)
let minRange = 0;
let maxRange = 100;

// توزيع الأرقام
let gameData = players.map(name => {
    return {
        name: name,
        number: Math.floor(Math.random() * (maxRange - minRange + 1)) + minRange
    };
});

// النتيجة بتطلع كذا: 
// [{name: "عبود", number: 42}, {name: "فيصل", number: 87}, ...]
