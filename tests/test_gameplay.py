"""Run real inline game logic with inert browser UI/timer adapters."""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NODE = shutil.which("node")
NODE_HARNESS = r"""
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const noop = () => {};
const drawing = new Proxy({}, {
  get(target, key) { return key in target ? target[key] : noop; }
});
const elements = new Map();
function element(selector) {
  if (!elements.has(selector)) {
    elements.set(selector, {
      textContent: '', hidden: false, disabled: false, value: '105',
      dataset: {}, style: {}, classList: { add: noop, remove: noop },
      addEventListener: noop, getContext: () => drawing
    });
  }
  return elements.get(selector);
}
const storage = new Map();
const context = vm.createContext({
  assert,
  document: {
    querySelector: element, querySelectorAll: () => [],
    addEventListener: noop, hidden: false
  },
  localStorage: {
    getItem: key => storage.get(key) ?? null,
    setItem: (key, value) => storage.set(key, String(value))
  },
  setInterval: () => 1, clearInterval: noop
});
vm.runInContext('Math.random = () => 0.125;', context);
vm.runInContext(input.script, context, { filename: input.filename, timeout: 1000 });
vm.runInContext(input.scenario, context, { filename: 'regression-scenario', timeout: 1000 });
"""


@unittest.skipUnless(NODE, "Node.js is required for inline JavaScript regression tests")
class GameplayRegressionTest(unittest.TestCase):
    def run_game(self, filename, scenario):
        assert NODE is not None
        html = (PROJECT_ROOT / filename).read_text(encoding="utf-8")
        scripts = re.findall(r"<script>([\s\S]*?)</script>", html)
        self.assertEqual(len(scripts), 1)
        result = subprocess.run(
            [NODE, "-e", NODE_HARNESS],
            input=json.dumps({"filename": filename, "script": scripts[0],
                              "scenario": scenario}),
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_first_hold_stays_disabled_until_the_active_piece_locks(self):
        self.run_game("tetris.html", """
          resetGame();
          start();
          assert.equal(canHold, true);
          hold();
          assert.equal(canHold, false, 'first hold must remain disabled');
          const before = JSON.stringify({current, currentPos, holdPiece, nextPiece});
          hold();
          assert.equal(JSON.stringify({current, currentPos, holdPiece, nextPiece}), before,
                       'a second hold before locking must do nothing');
          dropHard();
          assert.equal(state, 'playing');
          assert.equal(canHold, true, 'locking a piece must restore hold availability');
        """)

    def test_occupied_hold_spawn_ends_game_without_overwriting_landed_blocks(self):
        self.run_game("tetris.html", """
          resetGame();
          start();
          holdPiece = { type: 'O', matrix: SHAPES.O.matrix.map(row => [...row]),
                        color: SHAPES.O.color, glow: SHAPES.O.glow };
          grid[0][4] = '#occupied';
          const before = JSON.stringify(grid);
          hold();
          assert.equal(state, 'over', 'an overlapping held piece must end the game');
          assert.equal(canHold, false);
          assert.equal(pauseBtn.disabled, true);
          dropHard();
          dropSoft();
          moveLeft();
          assert.equal(JSON.stringify(grid), before, 'landed blocks must not be overwritten');
        """)

    def test_snake_eating_last_free_cell_finishes_without_freezing(self):
        self.run_game("snake.html", """
          snake = [{x: 0, y: 0}];
          for (let y = 0; y < cells; y++) {
            for (let x = 0; x < cells; x++) {
              if (!(y === 0 && (x === 0 || x === 1))) snake.push({x, y});
            }
          }
          assert.equal(snake.length, cells * cells - 1);
          direction = queued = dirs.right;
          food = {x: 1, y: 0};
          state = 'playing';
          pauseBtn.disabled = false;
          score = 0;
          tick();
          assert.equal(snake.length, cells * cells);
          assert.equal(score, 10);
          assert.equal(state, 'over', 'a full board must finish the game');
          assert.equal(food, null, 'no food can be placed on a full board');
          assert.equal(pauseBtn.disabled, true);
          assert.equal(overlay.hidden, false);
          assert.match(overlayTitle.textContent, /成功/);
          assert.equal(Number(lengthEl.textContent), cells * cells);
          tick();
          assert.equal(snake.length, cells * cells, 'finished games must not advance');
          start();
          assert.equal(state, 'playing', 'a completed game must remain restartable');
          assert.equal(snake.length, 3);
        """)

    def test_unblocked_hold_swap_still_allows_play_and_prevents_repeated_hold(self):
        self.run_game("tetris.html", """
          resetGame();
          start();
          const originalType = current.type;
          holdPiece = { type: 'O', matrix: SHAPES.O.matrix.map(row => [...row]),
                        color: SHAPES.O.color, glow: SHAPES.O.glow };
          hold();
          assert.equal(state, 'playing');
          assert.equal(current.type, 'O');
          assert.equal(holdPiece.type, originalType);
          assert.equal(canHold, false);
          hold();
          assert.equal(current.type, 'O');
          dropHard();
          assert.equal(state, 'playing');
          assert.equal(canHold, true);
        """)

    def test_snake_food_uses_the_only_remaining_free_cell(self):
        self.run_game("snake.html", """
          snake = [];
          for (let y = 0; y < cells; y++) {
            for (let x = 0; x < cells; x++) {
              if (x !== cells - 1 || y !== cells - 1) snake.push({x, y});
            }
          }
          assert.equal(placeFood(), true);
          assert.equal(food.x, cells - 1);
          assert.equal(food.y, cells - 1);
        """)

    def test_snake_normal_eating_and_wall_collision_are_preserved(self):
        self.run_game("snake.html", """
          reset();
          start();
          food = {x: 11, y: 10};
          tick();
          assert.equal(state, 'playing');
          assert.equal(score, 10);
          assert.equal(snake.length, 4);
          assert.equal(snake.some(p => p.x === food.x && p.y === food.y), false);
          snake = [{x: cells - 1, y: 10}, {x: cells - 2, y: 10}];
          direction = queued = dirs.right;
          tick();
          assert.equal(state, 'over');
          assert.equal(pauseBtn.disabled, true);
        """)


if __name__ == "__main__":
    unittest.main()
