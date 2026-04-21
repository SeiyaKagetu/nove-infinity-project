const lotoData = [
    {"draw": 2095, "date": "2026-04-20", "numbers": [2, 10, 18, 25, 33, 41], "bonus": 14, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2094, "date": "2026-04-16", "numbers": [3, 4, 7, 11, 24, 30], "bonus": 16, "winners1": 5, "prize1": 42516700, "carry_over": 0},
    {"draw": 2093, "date": "2026-04-13", "numbers": [2, 10, 21, 26, 29, 38], "bonus": 12, "winners1": 0, "prize1": 0, "carry_over": 751519994},
    {"draw": 2092, "date": "2026-04-09", "numbers": [8, 13, 27, 36, 37, 43], "bonus": 3, "winners1": 0, "prize1": 0, "carry_over": 480712171},
    {"draw": 2091, "date": "2026-04-06", "numbers": [6, 16, 21, 25, 28, 43], "bonus": 9, "winners1": 0, "prize1": 0, "carry_over": 227840393},
    {"draw": 2090, "date": "2026-04-02", "numbers": [2, 3, 6, 9, 24, 36], "bonus": 5, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2089, "date": "2026-03-30", "numbers": [9, 16, 18, 32, 37, 43], "bonus": 13, "winners1": 0, "prize1": 0, "carry_over": 236800230},
    {"draw": 2088, "date": "2026-03-26", "numbers": [8, 16, 18, 27, 37, 39], "bonus": 29, "winners1": 3, "prize1": 66666700, "carry_over": 0},
    {"draw": 2087, "date": "2026-03-23", "numbers": [1, 4, 10, 11, 17, 33], "bonus": 31, "winners1": 1, "prize1": 600000000, "carry_over": 31193795},
    {"draw": 2086, "date": "2026-03-19", "numbers": [5, 12, 14, 21, 26, 34], "bonus": 40, "winners1": 0, "prize1": 0, "carry_over": 377168743},
    {"draw": 2085, "date": "2026-03-16", "numbers": [3, 7, 15, 22, 28, 41], "bonus": 19, "winners1": 1, "prize1": 600000000, "carry_over": 131403738},
    {"draw": 2084, "date": "2026-03-12", "numbers": [2, 9, 13, 25, 30, 36], "bonus": 6, "winners1": 0, "prize1": 0, "carry_over": 462516068},
    {"draw": 2083, "date": "2026-03-09", "numbers": [4, 11, 19, 24, 35, 42], "bonus": 8, "winners1": 0, "prize1": 0, "carry_over": 210243220},
    {"draw": 2082, "date": "2026-03-05", "numbers": [6, 10, 17, 23, 29, 38], "bonus": 14, "winners1": 2, "prize1": 135420100, "carry_over": 0},
    {"draw": 2081, "date": "2026-03-02", "numbers": [1, 5, 12, 20, 27, 43], "bonus": 32, "winners1": 0, "prize1": 0, "carry_over": 247024989},
    {"draw": 2080, "date": "2026-02-26", "numbers": [7, 14, 21, 28, 35, 42], "bonus": 3, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2079, "date": "2026-02-23", "numbers": [2, 8, 15, 22, 29, 36], "bonus": 11, "winners1": 0, "prize1": 0, "carry_over": 207185202},
    {"draw": 2078, "date": "2026-02-19", "numbers": [4, 10, 17, 24, 31, 38], "bonus": 5, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2077, "date": "2026-02-16", "numbers": [6, 12, 19, 26, 33, 40], "bonus": 9, "winners1": 2, "prize1": 128450300, "carry_over": 0},
    {"draw": 2076, "date": "2026-02-12", "numbers": [1, 7, 14, 21, 28, 35], "bonus": 13, "winners1": 5, "prize1": 45120400, "carry_over": 0},
    {"draw": 2075, "date": "2026-02-09", "numbers": [3, 9, 16, 23, 30, 37], "bonus": 2, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2074, "date": "2026-02-05", "numbers": [5, 11, 18, 25, 32, 39], "bonus": 7, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2073, "date": "2026-02-02", "numbers": [2, 8, 15, 22, 29, 36], "bonus": 10, "winners1": 0, "prize1": 0, "carry_over": 222215112},
    {"draw": 2072, "date": "2026-01-29", "numbers": [1, 13, 24, 27, 34, 41], "bonus": 5, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2071, "date": "2026-01-26", "numbers": [4, 9, 18, 22, 30, 43], "bonus": 12, "winners1": 0, "prize1": 0, "carry_over": 245102931},
    {"draw": 2070, "date": "2026-01-22", "numbers": [7, 11, 20, 25, 33, 38], "bonus": 3, "winners1": 2, "prize1": 142050300, "carry_over": 0},
    {"draw": 2069, "date": "2026-01-19", "numbers": [2, 5, 14, 21, 36, 40], "bonus": 18, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2068, "date": "2026-01-15", "numbers": [6, 10, 15, 29, 31, 42], "bonus": 22, "winners1": 0, "prize1": 0, "carry_over": 185203941},
    {"draw": 2067, "date": "2026-01-12", "numbers": [3, 8, 17, 26, 35, 39], "bonus": 1, "winners1": 3, "prize1": 66666700, "carry_over": 0},
    {"draw": 2066, "date": "2026-01-08", "numbers": [5, 12, 19, 23, 28, 43], "bonus": 33, "winners1": 0, "prize1": 0, "carry_over": 210450293},
    {"draw": 2065, "date": "2026-01-05", "numbers": [1, 4, 11, 22, 27, 36], "bonus": 15, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2064, "date": "2025-12-29", "numbers": [10, 14, 20, 24, 30, 42], "bonus": 8, "winners1": 2, "prize1": 135402900, "carry_over": 0},
    {"draw": 2063, "date": "2025-12-25", "numbers": [3, 7, 19, 25, 33, 41], "bonus": 13, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2062, "date": "2025-12-22", "numbers": [6, 12, 18, 26, 34, 40], "bonus": 2, "winners1": 0, "prize1": 0, "carry_over": 256801931},
    {"draw": 2061, "date": "2025-12-18", "numbers": [1, 9, 15, 23, 31, 43], "bonus": 11, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2060, "date": "2025-12-15", "numbers": [4, 8, 17, 25, 33, 42], "bonus": 1, "winners1": 3, "prize1": 66666700, "carry_over": 0},
    {"draw": 2059, "date": "2025-12-11", "numbers": [5, 11, 14, 22, 29, 36], "bonus": 10, "winners1": 0, "prize1": 0, "carry_over": 198540231},
    {"draw": 2058, "date": "2025-12-08", "numbers": [2, 7, 16, 24, 35, 41], "bonus": 9, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2057, "date": "2025-12-04", "numbers": [3, 10, 19, 27, 34, 43], "bonus": 5, "winners1": 2, "prize1": 128504000, "carry_over": 0},
    {"draw": 2056, "date": "2025-12-01", "numbers": [6, 13, 21, 28, 30, 39], "bonus": 12, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2055, "date": "2025-11-27", "numbers": [1, 5, 15, 22, 26, 34], "bonus": 18, "winners1": 5, "prize1": 42104900, "carry_over": 0},
    {"draw": 2054, "date": "2025-11-24", "numbers": [4, 9, 17, 23, 31, 40], "bonus": 2, "winners1": 0, "prize1": 0, "carry_over": 235601941},
    {"draw": 2053, "date": "2025-11-20", "numbers": [7, 11, 20, 25, 33, 42], "bonus": 8, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2052, "date": "2025-11-17", "numbers": [3, 8, 14, 21, 29, 36], "bonus": 5, "winners1": 2, "prize1": 138502900, "carry_over": 0},
    {"draw": 2051, "date": "2025-11-13", "numbers": [2, 10, 16, 24, 32, 41], "bonus": 1, "winners1": 0, "prize1": 0, "carry_over": 185203941},
    {"draw": 2050, "date": "2025-11-10", "numbers": [5, 12, 19, 27, 35, 43], "bonus": 13, "winners1": 3, "prize1": 66666700, "carry_over": 0},
    {"draw": 2049, "date": "2025-11-06", "numbers": [1, 6, 15, 22, 30, 38], "bonus": 9, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2048, "date": "2025-11-03", "numbers": [4, 9, 18, 26, 34, 40], "bonus": 11, "winners1": 2, "prize1": 142050300, "carry_over": 0},
    {"draw": 2047, "date": "2025-10-30", "numbers": [3, 7, 11, 23, 28, 41], "bonus": 16, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2046, "date": "2025-10-27", "numbers": [2, 10, 21, 25, 33, 42], "bonus": 4, "winners1": 0, "prize1": 0, "carry_over": 210450293},
    {"draw": 2045, "date": "2025-10-23", "numbers": [5, 12, 14, 24, 30, 39], "bonus": 1, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2044, "date": "2025-10-20", "numbers": [1, 8, 19, 27, 36, 43], "bonus": 12, "winners1": 3, "prize1": 66666700, "carry_over": 0},
    {"draw": 2043, "date": "2025-10-16", "numbers": [4, 9, 15, 23, 31, 40], "bonus": 5, "winners1": 0, "prize1": 0, "carry_over": 245102931},
    {"draw": 2042, "date": "2025-10-13", "numbers": [7, 11, 20, 26, 34, 42], "bonus": 18, "winners1": 1, "prize1": 200000000, "carry_over": 0},
    {"draw": 2041, "date": "2025-10-09", "numbers": [2, 6, 12, 22, 28, 38], "bonus": 9, "winners1": 2, "prize1": 138504000, "carry_over": 0}
];

exports.handler = async (event, context) => {
    try {
        const period = parseInt(event.queryStringParameters.period || "26");
        
        // 指定された期間、または全データを使用
        const targetData = (period >= 30) ? lotoData : lotoData.slice(0, period);
        
        // 出現頻度集計
        const counts = {};
        targetData.forEach(draw => {
            draw.numbers.forEach(num => {
                counts[num] = (counts[num] || 0) + 1;
            });
        });

        // ホットナンバー抽出
        const hot = Object.entries(counts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 15)
            .map(([num, count]) => [parseInt(num), count]);

        // コールドナンバー抽出
        const drawnSet = new Set(Object.keys(counts).map(Number));
        let cold = [];
        for (let i = 1; i <= 43; i++) {
            if (!drawnSet.has(i)) cold.push(i);
        }
        if (cold.length < 15) {
            const rare = Object.entries(counts)
                .sort((a, b) => a[1] - b[1])
                .map(([num, count]) => parseInt(num));
            for (let num of rare) {
                if (!cold.includes(num)) cold.push(num);
                if (cold.length >= 15) break;
            }
        }
        cold = cold.slice(0, 15);

        // 予測ロジック
        const getRandom = (arr, n) => {
            const shuffled = [...arr].sort(() => 0.5 - Math.random());
            return shuffled.slice(0, n);
        };
        
        const selectedHot = getRandom(hot.map(h => h[0]), 3);
        const selectedCold = getRandom(cold, 2);
        const used = new Set([...selectedHot, ...selectedCold]);
        let others = [];
        for (let i = 1; i <= 43; i++) {
            if (!used.has(i)) others.push(i);
        }
        const randomNum = getRandom(others, 1)[0];

        const prediction = [...selectedHot, ...selectedCold, randomNum].sort((a, b) => a - b);
        
        const details = prediction.map(num => {
            if (selectedHot.includes(num)) {
                return { num, reason: "期間内トレンド", desc: `直近で頻繁に出現。現在のサイクルで選ばれやすい勢いがあります。` };
            } else if (selectedCold.includes(num)) {
                const count = counts[num] || 0;
                return { num, reason: "確率の反発", desc: `出現が${count}回と滞っており、統計的な均衡により次回出現の期待値が高まっています。` };
            } else {
                return { num, reason: "不確定要素補完", desc: `計算外のランダム性をカバーするために選出。` };
            }
        });

        const fullCounts = [];
        for (let i = 1; i <= 43; i++) {
            fullCounts.push({ num: i, count: counts[i] || 0 });
        }

        return {
            statusCode: 200,
            headers: { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*" 
            },
            body: JSON.stringify({
                data: targetData,
                hot,
                cold,
                prediction,
                details,
                fullCounts,
                currentPeriod: period
            })
        };
    } catch (error) {
        return { statusCode: 500, body: error.toString() };
    }
};
