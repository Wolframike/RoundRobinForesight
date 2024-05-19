# RoundRobinForesight

## About
RoundRobinForesight is a Python project designed to calculate the probability of final placements in a round-robin tournament. This tool is tailored specifically for VALORANT esports　and designed to fetch necessary data from Liquipedia, providing detailed probabilistic insights based on match outcomes.

![RRF](https://github.com/Wolframike/RoundRobinForesight/assets/145457464/baa2cf42-bd98-4393-b3cb-90ae01a34a81)
|:--:| 
| *Test run using Challengers North: Polaris* |

## Computation Flow

1. Enter match results for completed matches
2. Repeat the below a sufficient amount of times:
    1. For each future match:
        1. Assign a map to either team with equal probability
        2. Repeat until one team wins 2 maps
    2. Determine the standings based on simulated match outcomes
    3. Record the standings
3. Convert the recorded standings to probabilities

---

1. 既に終了している試合の結果を入力
2. 以下を十分大きい回数繰り返す
    1. 以下を未実施の試合すべてに対して行う
        1. 両チームに対して等確率でマップを分配
        2. どちらかが2マップ取得で終了
    2. 順位を判定
    3. 順位を記録
3. 記録した順位を確率に変換

## Reference

### VCT 2023 Americas Ruleset

As very few regions provide tiebreaker rules for ties between 4+ teams, I have decided to refer to the VCT Americas 2023 ruleset, assuming that the round-robin ruleset is unified across regions and leagues.

For detailed rules and policies, refer to the link below

---

4チーム以上対象のタイブレイカールールがほとんどのリージョンで存在しない為、やむおえずVCT・VALORANT Challengers内ではラウンドロビンのフォーマットは統一されているという仮定の下このルールを使用しています。

ルールの詳細については以下のリンクから

**[Americas Rules and Policies 2023](https://www.dropbox.com/sh/xfy0lbve0hdr0ju/AAB0_AhrZQmhr4_HDOBQKK8Qa/Rules%20and%20Policies%202023/Americas%20Rules%20and%20Policies%202023?e=1&preview=VCT+Americas+Event-Specific+Ruleset+(v23.2).pdf&subfolder_nav_tracking=1&dl=0)**
